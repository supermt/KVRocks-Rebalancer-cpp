import json
import os
import sys
from pathlib import Path
import matplotlib.pyplot as plt


def get_result_file_map(target_dir):
    file_map = {
        "op_latency": [],
        "load_throughput": [],
        "run_throughput": [],
        "rocks_stat_before_run": [],
        "rocks_stat_after_run": []
    }
    print(target_dir)
    # for dir, subdir, file in os.walk(target_dir):
    #     print(file)
    stat_list = Path(target_dir).glob('*.stat')
    # fild all stat
    for file in stat_list:
        file = file.name
        if "after_" in file:
            file_map["rocks_stat_after_run"].append(file)
        if "separate" in target_dir:
            if "before_run" in file:
                file_map["rocks_stat_before_run"].append(file)
        else:
            if "before_migration" in file:
                file_map["rocks_stat_before_run"].append(file)

    load_list = Path(target_dir).glob("load*")

    for file in load_list:
        file = file.name
        if "_result" in file:
            file_map["load_throughput"].append(file)
        else:
            file_map["op_latency"].append(file)

    load_list = Path(target_dir).glob("run*")

    for file in load_list:
        file = file.name
        if "_result" in file:
            file_map["run_throughput"].append(file)
        else:
            file_map["op_latency"].append(file)

    return file_map


import json


def file_to_cache_data(dir_prefix, file_list):
    cache_info = {"hit": 0, "add": 0, "miss": 0}
    for file in file_list:
        with open(dir_prefix + "/" + file, "r") as f:
            data = json.load(f)

        # print(data["rocksdb.block.cache"])

        for key in cache_info:
            prefix = "rocksdb.block.cache."
            total_key = prefix + key
            cache_info[key] += data[total_key]
    return cache_info


import csv
import pandas as pd

if __name__ == '__main__':
    result_dir = sys.argv[1]
    # result_dir = os.path.abspath(result_dir)
    print("reading file from " + result_dir)
    rows = []
    for workload in ["a", "b", "c", "d", "e", "f"]:
        for migration_type in ["separate", "together"]:
            target_dir = result_dir + "rocks_stat/" + workload + "/" + migration_type
            file_map = get_result_file_map(target_dir)
            stats_before = file_map["rocks_stat_before_run"]
            cache_b = file_to_cache_data(target_dir, stats_before)
            stats_after = file_map["rocks_stat_after_run"]
            cache_a = file_to_cache_data(target_dir, stats_after)

            cache_change = {}
            row = [migration_type, workload]
            for key in cache_a:
                print(key)
                row.append(cache_a[key] - cache_b[key])
            rows.append(row)

    cache_df = pd.DataFrame(rows, columns=["mode", "workload", "hit", "add", "miss"])
    cache_df.to_csv(result_dir + "/cache.csv", index=False, sep="\t")
    # throughput_df = pd.DataFrame(throughput_rows, columns=["mode", "workload", "throughput"])
    # row_df = pd.DataFrame(rows, columns=
    # ["mode", "workload", "op", "avg", "P99", "P99.9", "P99.99", "max"])
    # throughput_df.to_csv(result_dir + "/throughput.csv", index=False, sep="\t")
