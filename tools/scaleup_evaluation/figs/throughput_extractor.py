import pandas as pd
import json
migration_methods = ["push", "pull", "level"]
method_name = {"push": "seek-and-insert",
               "pull": "comapct-and-merge", "level": "level migration"}
workloads = ["a"]  # , "b", "c", "d", "e", "f"]

dir_pattern = "../result_log_%s_%s"


def time_diff(timestamp1, timestamp2):
    from datetime import datetime

    # Define the two timestamp strings
    timestamp_format = '%H:%M:%S.%f'

    # Convert the timestamp strings to datetime objects
    dt1 = datetime.strptime(timestamp1, timestamp_format)
    dt2 = datetime.strptime(timestamp2, timestamp_format)
    return (dt1-dt2).total_seconds()


def get_hit_ratio_from_lines(lines):
    min_hit = 1.0
    max_hit = 0.0
    avg_hit = 0.0

    last_hit = 0
    last_total = 0
    for line in lines:
        try:
            data = json.loads(line)
        except:
            # print("non-json line: ", line)
            continue

        wal_writes = data["rocksdb.write.wal"]
        total_read = data["rocksdb.non.last.level.read.count"] + \
            data["rocksdb.last.level.read.count"]

        total_cache = data["rocksdb.block.cache.data.miss"] + \
            data["rocksdb.block.cache.data.hit"] + 1
        hit_count = data["rocksdb.block.cache.data.hit"]

        current_hit = hit_count - last_hit
        current_total = total_cache - last_total

        current_ratio = current_hit/(current_total+1.0)
        if (current_ratio < min_hit):
            min_hit = current_ratio
        if current_ratio > max_hit:
            max_hit = current_ratio

        last_hit = hit_count
        last_total = total_cache

    avg_hit = last_hit/(last_total+1.0)

    return min_hit*100, max_hit*100, avg_hit*100


result_rows = []
for method in migration_methods:
    for workload in workloads:
        dir_name = dir_pattern % (method, workload)
        print(dir_name)

        row = [method_name[method], workload]
        # Get migration time cost
        start_migration_time = ""
        end_migration_time = ""
        src_log_lines = open(dir_name+"/node1_info.log").readlines()
        for line in src_log_lines:
            if "Start migrating slots" in line:
                start_migration_time = line.split()[1]
            if "Clean resources of migrating slot " in line:
                end_migration_time = line.split()[1]

        migration_secs = 0
        if start_migration_time != "" and end_migration_time != "":
            migration_secs = time_diff(
                end_migration_time, start_migration_time)

        row.append(time_diff(end_migration_time, start_migration_time))

        # Get the throughput
        throughput = 0
        qps_log_lines = open(dir_name+"/qps.log").readlines()
        for line in qps_log_lines[-5:]:
            if "Run throughput(ops/sec):" in line:
                throughput = line.split()[2]
                throughput = float(throughput)

        row.append(throughput)

        # Get the cache hit ratio
        rocks_stat_log_lines_src = open(dir_name+"/server_40001.log")
        min_hit, max_hit, avg_hit = get_hit_ratio_from_lines(
            rocks_stat_log_lines_src)
        # row.extend([min_hit,max_hit,avg_hit])
        row.extend([max_hit, avg_hit])

        rocks_stat_log_lines_dst = open(dir_name+"/server_40002.log")
        min_hit, max_hit, avg_hit = get_hit_ratio_from_lines(
            rocks_stat_log_lines_dst)
        row.extend([max_hit, avg_hit])

        result_rows.append(row)

result_df = pd.DataFrame(result_rows, columns=["method", "workload", "migration time (sec)",
                         "throughput (ops/sec)", "src_max_hit", "src_avg_hit", "dst_max_hit", "dst_avg_hit"])


result_df = result_df.round(1)
print(result_df)
result_df.to_csv("stat_info.csv",index=None,sep="\t")