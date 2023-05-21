import gzip
from datetime import datetime

from tools.analyze.utils import get_result_file_map


def extract_migration_time(file_list, end_slot):
    start_time = ""
    end_time_line = ""
    for file in file_list:
        if "gz" in file:
            file_content = gzip.open(file, "rb")
        else:
            file_content = open(file, "r", encoding="ISO-8859-1", errors='ignore')

        line = "1"

        while line:
            if "gz" in file:
                line = str(file_content.readline(), "utf-8")
            line = str(file_content.readline())
            # print(line)
            if "Succeed to import slot " + str(end_slot) in line:
                end_time_line = line
            if "Start migrating" in line:
                start_time = line
                break
    start_time = start_time.split()
    end_time_line = end_time_line.split()
    if len(start_time) > 0:
        start_time = start_time[1]
    else:
        start_time = 0
    if len(end_time_line) > 0:
        end_time_line = end_time_line[1]
    else:
        end_time_line = 0
    print(start_time, end_time_line)

    return start_time, end_time_line


def plot_real_time_speed(input_file_list, workloads=['a', 'e'], last_slot=16384):
    label_map = {
        "seek-and-insert": "baseline",
        # "batch-seek-and-insert": "parallel-baseline",
        "compact-and-merge": "pull-non-expanded",
        "level-based-stat": "level"
    }
    for workload in workloads:
        i = 0
        for migration_method in label_map:
            i += 1
            target_dir = input_file_list + "/" + workload + "/together/" + str(
                label_map[migration_method])
            file_map = get_result_file_map(target_dir)
            log_files = file_map['log_file']
            info_log = ""
            for log in log_files:
                if "INFO" in log:
                    info_log = log
            print(info_log)
            if info_log:
                f = open(info_log, "r", encoding='unicode_escape')
                start_lines = []
                sst_compaction_line = []
                sst_filter_line = []
                WAL_migrate_line = []
                snapshot_finished_line = []
                for line in f.readlines():
                    if "Succeed to start migrating slot" in line:
                        start_lines.append(line)
                    if "SST compacted" in line:
                        sst_compaction_line.append(line)
                    if "filtered" in line:
                        sst_filter_line.append(line)
                    if "server was blocked for" in line:
                        WAL_migrate_line.append(line)
                    if "Succeed to migrate snapshot" in line:
                        snapshot_finished_line.append(line)
                time_format = '%H:%M:%S.%f'

                total_send_snap = 0
                print(len(start_lines), len(WAL_migrate_line))
                for i in range(len(start_lines)):
                    send_snap_start = start_lines[i].split()[1]
                    wal_migrate_start = WAL_migrate_line[i].split()[1]

                    send_snap_start = datetime.strptime(send_snap_start, time_format)
                    wal_migrate_start = datetime.strptime(wal_migrate_start, time_format)
                    send_snap_time = wal_migrate_start - send_snap_start
                    send_snap_time = send_snap_time.total_seconds() * 1000000

                    total_send_snap += send_snap_time

                print("send_snap_time (ms)", total_send_snap)

                WAL_migrate_time = 0
                for line in WAL_migrate_line:
                    WAL_migrate_time += int(line.split()[-1][:-2])
                print("WAL_migrate_time", WAL_migrate_time)
                sst_compaction_time = 0
                for line in sst_compaction_line:
                    sst_compaction_time += int(line.split()[-1])
                print("sst_compaction_time (ms):", sst_compaction_time)
                sst_filter_time = 0
                for line in sst_filter_line:
                    sst_filter_time += int(line.split()[-1])
                print("sst filter (ms):", sst_filter_time)
    pass


if __name__ == '__main__':
    # target_dir = "../section2-hotness-balance/rocks_stat"
    # workloads = ["m"]
    # plot_real_time_speed(target_dir, workloads)

    target_dir = "../section2-scale-up/54l_10m_sleep30/"
    workloads = ["a"]
    plot_real_time_speed(target_dir, workloads)
