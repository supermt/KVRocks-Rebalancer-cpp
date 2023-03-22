import json
import os
import sys
from pathlib import Path
from utils import get_result_file_map
from utils import extract_tail_latency
import pandas as pd


if __name__ == '__main__':
    result_dir = sys.argv[1]
    print("reading file from " + result_dir)
    rows = []
    throughput_rows = []
    for workload in ["a", "b", "c", "d", "e", "f"]:
        for migration_type in ["separate", "together"]:
            target_dir = result_dir + "rocks_stat/" + workload + "/" + migration_type
            file_map = get_result_file_map(target_dir)
            op_latency_map = extract_tail_latency(target_dir + "/", file_map["op_latency"])
            run_throughput_file = target_dir + "/" + file_map["run_throughput"][0]

            file_line = open(run_throughput_file, "r").readlines()

            latency_and_count_entries = file_line[-4].split("operations;")[1].split()
            avg_latency = {}
            for i in range(0, len(latency_and_count_entries), 5):
                op = latency_and_count_entries[i].replace("[", "").replace(":", "")
                max_latency = latency_and_count_entries[i + 2].split("=")[1]
                # print(max_latency)
                latency = latency_and_count_entries[i + 4].split("=")[1].replace("]", "")
                # print(latency)
                avg_latency[op] = {}
                avg_latency[op]["max"] = max_latency
                avg_latency[op]["avg"] = latency

            # mode, workload, op, throughput, avg, P99, P99.9, P99.99
            row_head = [migration_type, workload, file_line[-1].split()[-1]]
            throughput_rows.append(row_head)
            row_head = [migration_type, workload]
            for op in avg_latency:
                row = []
                row.extend(row_head)
                row.append(op)
                row.append(avg_latency[op]["avg"])
                row.append(op_latency_map[op]["P99"])
                row.append(op_latency_map[op]["P99.9"])
                row.append(op_latency_map[op]["P99.99"])
                row.append(avg_latency[op]["max"])
                rows.append(row)

    throughput_df = pd.DataFrame(throughput_rows, columns=["mode", "workload", "throughput"])
    row_df = pd.DataFrame(rows, columns=
    ["mode", "workload", "op", "avg", "P99", "P99.9", "P99.99", "max"])
    throughput_df.to_csv(result_dir + "/throughput.csv", index=False, sep="\t")
    row_df.to_csv(result_dir + "/op_latency.csv", index=False, sep="\t")
