
import matplotlib.font_manager as fm
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


def get_qps_from_file(file_name):
    result = []

    file_content = open(file_name, "r").readlines()[1:-2]
    line_count = 0
    for line in file_content:
        line_count += 1
        try:
            vec = line.split()
            time_stamp = vec[1]
            elased_time = int(vec[2])
            finished = int(vec[4])
            if line_count == 1:
                qps = int(vec[4])
            else:
                qps = int(vec[4]) - result[-1][-1]

            result.append([time_stamp, elased_time, qps, finished])
        except:
            pass

    result = pd.DataFrame(result[5:310], columns=[
                          "timestamp", "elapsed time", "qps", "finished_ops"])

    return result


plt.rcParams['figure.figsize'] = (24, 5)  # 8 inches wide by 6 inches tall
plt.rcParams['font.size'] = 20  # 8 inches wide by 6 inches tall
plt.rcParams['font.family'] = 'Arial'

fig, axs = plt.subplots(1, 4, sharex=True, sharey=True)


baseline_migration_qps = get_qps_from_file("temp_1k_migration_test")
baseline_double_qps = get_qps_from_file("temp_1k_double")
baseline_pull_qps = get_qps_from_file("temp_1k_pull")
level_migration_qps = get_qps_from_file("temp_1k_level_test")

# Double baseline
axs[0].plot(baseline_double_qps["elapsed time"],
               baseline_double_qps["qps"], label="Baseline")

axs[0].set_title("Balanced dual server")

# Seek-and-Insert
axs[1].plot(baseline_migration_qps["elapsed time"],
               baseline_migration_qps["qps"], label="Seek-and-Insert")
axs[1].set_title("Seek-and-Insert")
important_lines = [20, 298]
for important_x in important_lines:
    axs[1].axvline(important_x, ls=":", color="r", linewidth=4)

# Compact-and-Merge
axs[2].plot(baseline_pull_qps["elapsed time"],
               baseline_pull_qps["qps"], label="Compact-and-Merge")
axs[2].set_title("Compact-and-Merge")
important_lines = [20, 98]
for important_x in important_lines:
    axs[2].axvline(important_x, ls=":", color="r", linewidth=4)

# Level migration
axs[3].plot(level_migration_qps["elapsed time"],
               level_migration_qps["qps"], label="Proposed Method")
important_lines = [20, 37]
for important_x in important_lines:
    axs[3].axvline(important_x, ls=":", color="r", linewidth=4)
axs[3].set_title("Proposed Method")


# plt.plot(motivation_scale_qps_slow["elapsed time"],
#          motivation_scale_qps_slow["qps"],linestyle='dotted', label="scaling up with limited speed")
# plt.annotate('Migration start', xy=(20, 71000), xytext=(50, 71000),
#              arrowprops=dict(facecolor='#FFFFFF', edgecolor='red', shrink=0.01, linewidth=1), color='r')
# plt.annotate('End of migration', xy=(59, 71000), xytext=(75, 77000),
#              arrowprops=dict(facecolor='#FFFFFF', edgecolor='red', shrink=0.01, linewidth=1), color='r')

# plt.ylim((0, 73000))


plt.tight_layout()


fig.text(0.5, -0.01, 'Elapsed time (sec)', ha='center')
fig.text(-0.01, 0.5, 'Throughput (ops/sec)', va='center', rotation='vertical')


font = fm.FontProperties(fname='arial.ttf')
plt.savefig("motivation.pdf", bbox_inches='tight')


plt.plot()
