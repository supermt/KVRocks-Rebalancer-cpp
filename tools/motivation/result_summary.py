
# before_migration = open("../baseline/redis-benchamrk.result_single_node").readlines()
# after_migration = open("../baseline/redis-benchamrk.result_dual_node").readlines()

import matplotlib.pyplot as plt
import pandas as pd


def time_diff(timestamp1, timestamp2):
    from datetime import datetime

    # Define the two timestamp strings
    timestamp_format = '%H:%M:%S.%f'

    # Convert the timestamp strings to datetime objects
    dt1 = datetime.strptime(timestamp1, timestamp_format)
    dt2 = datetime.strptime(timestamp2, timestamp_format)
    return (dt1-dt2).total_seconds()


migration_stop = "00:50:14.310681"
double_node_start = "00:49:34.16874"

migration_finished_time = int(time_diff(migration_stop, double_node_start))


def get_qps_from_file(file_name, qps=[]):

    file_content = open(file_name, "r").readlines()[1:-2]
    start_timestamp = int(file_content[0].split(",")[0])
    for line in file_content:
        try:
            vec = line.split(",")
            if len(vec) == 2:
                qps.append(vec[0])
            elif len(vec) == 3:
                qps.append(
                    [(int(vec[0]) - start_timestamp)/1000.0, int(vec[1])])
            else:
                pass
            # qps.append(int(line.split(',')[0]))
        except:
            pass

    if isinstance(qps[0], list):
        qps = pd.DataFrame(qps, columns=["timestamp", "qps"])

    return qps


# main function
motivation_before_migrate = "redis-benchamrk.result_single_node"
motivation_after_migrate = "redis-benchamrk.result"

baseline_single = "../baseline/redis-benchamrk.result_single_node"
baseline_double = "../baseline/redis-benchamrk.result_dual_node"

# qps = []

# get_qps_from_file(motivation_before_migrate, qps)
# get_qps_from_file(motivation_after_migrate,qps)

baseline_single_qps = get_qps_from_file(baseline_single, [])
baseline_double_qps = get_qps_from_file(baseline_double, [])

# plt.plot(qps,label="during scaling up")
plt.plot(baseline_single_qps["timestamp"],
         baseline_single_qps["qps"], label="baseline: single node cluster")
plt.plot(baseline_double_qps["timestamp"],
         baseline_double_qps["qps"], label="baseline: double node cluster")
plt.legend()
# plt.show()


plt.savefig("motivation.png")


plt.plot()


plt.savefig("baseline_single.png")
plt.savefig("baseline_dual.png")
