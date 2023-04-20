import gzip
import sys

import matplotlib as mpl
import matplotlib.pyplot as plt

from utils import *
from utils import extract_data_from_result_file
from utils import get_result_file_map


def extract_migration_time(file_list, end_slot):
    start_time = ""
    end_time = ""
    for file in file_list:
        if "gz" in file:
            file_content = gzip.open(file, "rb", encoding="ISO-8859-1", errors='ignore')
        else:
            file_content = open(file, "r", encoding="ISO-8859-1", errors='ignore')
            line = "1"
            while line:
                line = file_content.readline()
                # print(line)
                if "Succeed to import slot " + str(end_slot) in line:
                    end_time = line
                if "Start migrating slots" in line:
                    start_time = line
                    break
    start_time = start_time.split()
    end_time = end_time.split()
    if len(start_time) > 0:
        start_time = start_time[1]
    else:
        start_time = 0
    if len(end_time) > 0:
        end_time = end_time[1]
    else:
        end_time = 0
    # print(start_time, end_time)

    return start_time, end_time


if __name__ == '__main__':
    result_dir = sys.argv[1]
    print("reading file from " + result_dir)
    rows = []
    throughput_rows = []
    label_map = {
        # "seek-and-insert": "baseline",
        "batch-seek-and-insert": "parallel-baseline",
        "compact-and-merge": "pull-non-expanded",
        "level-based-stat": "level"
    }
    line_style_map = {
        "seek-and-insert": "dashed",
        "batch-seek-and-insert": "dotted",
        "compact-and-merge": "solid",
        "level-based-stat": "dashdot"
    }
    line_color_map = {
        "seek-and-insert": "green",
        "batch-seek-and-insert": "red",
        "compact-and-merge": "cyan",
        "level-based-stat": "black"
    }
    mpl.rcParams["figure.figsize"] = (6, 4)

    for workload in ["a"]:
        plt.cla()
        i = 0
        for migration_method in label_map:
            i += 1

            plt.subplot(len(label_map), 1, i)
            target_dir = result_dir + "/" + workload + "/together/" + str(
                label_map[migration_method])

            # print(target_dir)
            file_map = get_result_file_map(target_dir)
            # print(file_map)
            if len(file_map["load_throughput"]) == 0:
                print("no file")
                continue
            print("Plotting:", target_dir + "/" + file_map[kRUN_THROUGHPUT][0])
            start, end = extract_migration_time(file_map["log_file"], 8190)

            end_time = 0

            if start != 0 and end != 0:
                from datetime import datetime

                format = '%H:%M:%S.%f'
                time = datetime.strptime(end, format) - datetime.strptime(start, format)

                end_time = time.total_seconds()
            throughput, operation_details, finished_op_list = extract_data_from_result_file(
                target_dir + "/" + file_map[kRUN_THROUGHPUT][0])
            # print(finished_op_list["Finished Ops"])
            finished_op_list["Finished Ops"].to_csv(
                result_dir + "/" + workload + "-" + label_map[migration_method] + "-ops.csv", sep="\t", index=False
            )
            target_plot_array = finished_op_list["Finished Ops"][0:int(end_time)+5]
            plt.plot(target_plot_array, color=line_color_map[migration_method],
                     linestyle=line_style_map[migration_method],
                     label=label_map[migration_method])
            plt.ylim((min(target_plot_array), max(target_plot_array)))

            plt.axvline(x=0, color='b')
            plt.axvline(x=end_time, color='b')
            plt.legend()
            if i == 3:
                plt.xlabel("Elapsed Time (Sec)")
            if i == 2:
                plt.ylabel("Throughput (Ops/Sec)")

        plt.tight_layout()
        print("Save figure at workload: " + workload)
        # plt.savefig(result_dir + "/" + workload + "-Real-Time-Speed.png")
        plt.savefig(result_dir + "/" + workload + "-Real-Time-Speed.png")
