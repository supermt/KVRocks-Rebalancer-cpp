import gzip

import matplotlib as mpl
import matplotlib.pyplot as plt

from utils import *
from utils import get_result_file_map


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


def plot_real_time_speed(input_file_list, workloads=['a', 'e'], last_slot=13684):
    rows = []
    throughput_rows = []
    label_map = {
        "seek-and-insert": "baseline",
        # "batch-seek-and-insert": "parallel-baseline",
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

    for workload in workloads:
        i = 0
        for migration_method in label_map:
            i += 1

            plt.cla()
            # plt.subplot(len(label_map), 1, i)
            target_dir = input_file_list + "/" + workload + "/together/" + str(
                label_map[migration_method])

            # print(target_dir)
            file_map = get_result_file_map(target_dir)
            # print(file_map)
            if len(file_map["load_throughput"]) == 0:
                print("no file")
                continue
            print("Plotting:", target_dir + "/" + file_map[kRUN_THROUGHPUT][0])
            # start, end = extract_migration_time(file_map["log_file"], last_slot)
            #
            # end_time = 0
            #
            # if start != 0 and end != 0:
            #     from datetime import datetime
            #
            #     time_format = '%H:%M:%S.%f'
            #     time = datetime.strptime(end, time_format) - datetime.strptime(start, time_format)
            #
            #     end_time = time.total_seconds()
            # throughput, operation_details, finished_op_list = extract_data_from_result_file(
            #     target_dir + "/" + file_map[kRUN_THROUGHPUT][0])
            #
            # # print(finished_op_list["Finished Ops"])
            # finished_op_list["Finished Ops"].to_csv(
            #     input_file_list + "/" + workload + "-" + label_map[migration_method] + "-ops.csv", sep="\t", index=False
            # )
            finished_op_list = pd.read_csv(
                input_file_list + "/" + workload + "-" + label_map[migration_method] + "-ops.csv", sep="\t")
            finished_op_list = pd.DataFrame(finished_op_list, columns=["Finished Ops"])
            start_time = 0

            # plt.axvline(x=start_time, color='b')
            # plt.axvline(x=start_time + end_time, color='b')
            plt.ylim(0, max(finished_op_list["Finished Ops"]))
            plt.plot(finished_op_list["Finished Ops"][start_time:int(0.9 * len(finished_op_list["Finished Ops"]))])
            plt.tight_layout()
            print("Save figure at workload: " + workload)
            # plt.savefig(result_dir + "/" + workload + "-Real-Time-Speed.png")
            plt.savefig(input_file_list + "/" + workload + migration_method + "-Real-Time-Speed.png")

            # target_plot_array = finished_op_list["Finished Ops"][0:start_time + int(end_time * 1.5) + 5]
            # plt.plot(target_plot_array, color=line_color_map[migration_method],
            #          linestyle=line_style_map[migration_method],
            #          label=label_map[migration_method])
            # plt.ylim((min(target_plot_array), max(target_plot_array)))
            #
            # plt.legend()
            # if i == 3:
            #     plt.xlabel("Elapsed Time (Sec)")
            # if i == 2:
            #     plt.ylabel("Throughput (Ops/Sec)")


if __name__ == '__main__':
    # target_dir = "../section2-hotness-balance/rocks_stat"
    # workloads = ["m"]
    # plot_real_time_speed(target_dir, workloads)

    target_dir = "../section2-scale-up/54l_10m_sleep30/"
    workloads = ["a"]
    plot_real_time_speed(target_dir, workloads)
