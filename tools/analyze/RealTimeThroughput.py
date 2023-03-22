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
    mpl.rcParams["figure.figsize"] = (6, 2.5)
    for workload in ["a", "b", "c", "d", "e", "f"]:
        # fig,ax = plt.subplots(figsize=(10, 4))
        for migration_type in ["separate", "together"]:
            target_dir = result_dir + "/rocks_stat/" + workload + "/" + migration_type
            file_map = get_result_file_map(target_dir)
            if len(file_map["load_throughput"]) == 0:
                # print("no file")
                continue

            print("Plotting:", target_dir + file_map[kRUN_THROUGHPUT][0])
            throughput, operation_details, finished_op_list = extract_data_from_result_file(
                target_dir + "/" + file_map[kRUN_THROUGHPUT][0])
            plt.plot(finished_op_list["Finished Ops"][50:180], label=migration_type)
        plt.xlabel("Elapsed Time (Sec)")
        plt.ylabel("Throughput (Ops/Sec)")
        plt.tight_layout()
        plt.legend()
        plt.savefig(result_dir + "/Real-Time-Speed.pdf")
