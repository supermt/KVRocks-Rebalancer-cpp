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
        0: "Non-limited migration",
        4096: "Rate-limited migration",
        "None": "Separated migration"
    }
    line_style_map = {
        0: 'dashed',
        4096: 'dotted',
        "None": "solid"
    }
    mpl.rcParams["figure.figsize"] = (6, 2.5)
    for speed in [0, 4096, "None"]:
        for workload in ["a"]:
            # fig,ax = plt.subplots(figsize=(10, 4))
            for migration_type in ["together", "separate"]:
                target_dir = result_dir + "/rocks_stat/" + str(speed) + "/" + workload + "/" + migration_type

                # print(target_dir)
                file_map = get_result_file_map(target_dir)
                if len(file_map["load_throughput"]) == 0:
                    # print("no file")
                    continue
                print("Plotting:", target_dir + file_map[kRUN_THROUGHPUT][0])
                throughput, operation_details, finished_op_list = extract_data_from_result_file(
                    target_dir + "/" + file_map[kRUN_THROUGHPUT][0])
                plt.plot(finished_op_list["Finished Ops"][:160], linestyle=line_style_map[speed],
                         label=label_map[speed])

    plt.xlabel("Elapsed Time (Sec)")
    plt.ylabel("Throughput (Ops/Sec)")
    plt.tight_layout()
    plt.legend()
    plt.savefig(result_dir + "/Real-Time-Speed.pdf")
