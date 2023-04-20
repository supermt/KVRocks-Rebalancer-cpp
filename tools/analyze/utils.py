import re
from pathlib import Path


def extract_op_list_from_line(test_str):
    op_regex = r"\[[A-Z]+: Count=[0-9]+ Max=[0-9]+.[0-9]* Min=[0-9]+.[0-9]* Avg=[0-9]+.[0-9]*\]"

    matches = re.findall(op_regex, test_str, re.MULTILINE)
    op_df_header = ["Op", "Max", "Min", "Avg"]
    op_list = []
    for match in matches:
        row = []
        if ":" in match:
            match = match.replace("[", "").replace("]", "")
            row.append(match.split(":")[0])
            for word in match.split()[1:]:
                row.append(float(word.split("=")[1]))

        op_list.append(row)  # op_list.append(row)
    # print(op_list)
    return op_list


kLOAD_THROUGHPUT = "load_throughput"
kRUN_THROUGHPUT = "run_throughput"
kOP_LATENCY = "op_latency"
kSTATS_BEFORE = "rocks_stat_before_run"
kSTATS_AFTER = "rocks_stat_after_run"


def get_result_file_map(target_dir):
    file_map = {"op_latency": [], "load_throughput": [], "run_throughput": [], "rocks_stat_before_run": [],
                "rocks_stat_after_run": [], "log_file": []}
    # print(target_dir)
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
    log_files = Path(target_dir).glob("node_*/*.INFO.*")

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

    for file in log_files:
        p = file.resolve()

        file_map["log_file"].append(str(p))

    return file_map


import pandas as pd


def extract_tail_latency(dir_prefix, file_list):
    op_latency_map = {"INSERT": {"P99": 0, "P99.9": 0, "P99.99": 0}, "UPDATE": {"P99": 0, "P99.9": 0, "P99.99": 0},
                      "SCAN": {"P99": 0, "P99.9": 0, "P99.99": 0}, "READ": {"P99": 0, "P99.9": 0, "P99.99": 0}}
    for file in file_list:
        target_file = dir_prefix + file
        # print(target_file)
        op = file.split("_")[1]
        # print(op)
        metrics_map = {99: "P99", 99.9: "P99.9", 99.99: "P99.99"}
        if "load_" in target_file:
            pass
        else:
            # print(target_file)
            result_df = pd.read_csv(target_file)
            for metrics in [99, 99.9, 99.99]:
                for row in result_df.iloc:
                    p = row["Percentile"] * 100
                    if p > metrics:
                        # print(Pmetrics)
                        op_latency_map[op][metrics_map[metrics]] = row["Value"]
                        break

    return op_latency_map


def extract_data_from_result_file(load_file):
    throughput_lines = []
    lines = open(load_file, "r").readlines()
    summary_lines = lines[-3:]
    throughput = float(summary_lines[-1].split()[-1])
    finished_op = []
    for line in lines:
        if "operations;" in line:
            op_line = line.split("operations;")[0]
            splits = op_line.split()
            if len(splits) != 5:
                continue
            op = splits[-1]
            time = splits[-3]
            finished_op.append([int(time), int(op)])
        # print(len(words))
        throughput_lines.extend(extract_op_list_from_line(line))  # throughput_lines.append()
    op_df = pd.DataFrame(throughput_lines, columns=["op", "count", "max", "min", "avg"])
    data_df = pd.DataFrame(finished_op, columns=["Time Elapsed (Sec)", "Finished Ops"])
    throughput_df = data_df.shift(periods=-1) - data_df
    # print(throughput_df)
    return throughput, op_df, throughput_df
