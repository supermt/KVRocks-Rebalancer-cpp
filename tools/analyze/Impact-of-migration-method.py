import sys

import matplotlib as mpl
import matplotlib.pyplot as plt

from utils import *
from utils import extract_data_from_result_file
from utils import get_result_file_map

if __name__ == '__main__':
    result_dir = sys.argv[1]
    print("reading file from " + result_dir)
    rows = []
    throughput_rows = []
    label_map = {
        "seek-and-insert": "seek-and-insert-stat",
        "batch-seek-and-insert": "batch-seek-and-insert-stat",
        "compact-and-merge": "compact-and-merge-stat",
        "level-based-stat": "level-based-stat"
    }
    line_style_map = {
        "seek-and-insert": "dashed",
        "batch-seek-and-insert": "dotted",
        "compact-and-merge": "solid",
        "level-based-stat": "dashdot"
    }
    mpl.rcParams["figure.figsize"] = (6, 2.5)
    for migration_method in label_map:
        for workload in ["a"]:
            # fig,ax = plt.subplots(figsize=(10, 4))
            for migration_type in ["together"]:
                target_dir = result_dir + "/" + str(
                    label_map[migration_method]) + "/" + workload + "/" + migration_type

                print(target_dir)
                file_map = get_result_file_map(target_dir)
                # print(file_map)
                if len(file_map["load_throughput"]) == 0:
                    # print("no file")
                    continue
                print("Plotting:", target_dir + file_map[kRUN_THROUGHPUT][0])
                throughput, operation_details, finished_op_list = extract_data_from_result_file(
                    target_dir + "/" + file_map[kRUN_THROUGHPUT][0])
                plt.plot(finished_op_list["Finished Ops"], linestyle=line_style_map[migration_method],
                         label=migration_method)

    plt.xlabel("Elapsed Time (Sec)")
    plt.ylabel("Throughput (Ops/Sec)")
    plt.tight_layout()
    plt.legend()
    plt.savefig(result_dir + "/Real-Time-Speed.png")
