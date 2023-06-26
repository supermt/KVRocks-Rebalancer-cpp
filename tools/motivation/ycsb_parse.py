
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

    result = pd.DataFrame(result[5:250], columns=[
                          "timestamp", "elapsed time", "qps", "finished_ops"])

    return result


plt.rcParams['figure.figsize'] = (12, 6)  # 8 inches wide by 6 inches tall
plt.rcParams['font.size'] = 20  # 8 inches wide by 6 inches tall
plt.rcParams['font.family'] = 'Arial'


baseline_single_qps = get_qps_from_file("temp_single")
baseline_double_qps = get_qps_from_file("temp_double")
motivation_scale_qps = get_qps_from_file("temp_migrate")
motivation_scale_qps_slow = get_qps_from_file("temp_single_4_clients")

# plt.plot(qps,label="during scaling up")
plt.plot(baseline_single_qps["elapsed time"],
         baseline_single_qps["qps"], label="single instance")

plt.plot(motivation_scale_qps["elapsed time"],
         motivation_scale_qps["qps"], linestyle='dashed', label="double instances with migration")

plt.plot(baseline_double_qps["elapsed time"],
         baseline_double_qps["qps"], label="double instances")

important_lines = [20, 163, 238]

for important_x in important_lines:
    plt.axvline(important_x, ls=":", color="r", linewidth=4)

# plt.plot(motivation_scale_qps_slow["elapsed time"],
#          motivation_scale_qps_slow["qps"],linestyle='dotted', label="scaling up with limited speed")
plt.annotate('Migration start', xy=(20, 71000), xytext=(50, 71000),
             arrowprops=dict(facecolor='#FFFFFF', edgecolor='red', shrink=0.01, linewidth=1), color='r')
plt.annotate('End of send snapshot', xy=(163, 71000), xytext=(75, 77000),
             arrowprops=dict(facecolor='#FFFFFF', edgecolor='red', shrink=0.01, linewidth=1), color='r')

plt.annotate('End of migration', xy=(238, 71000), xytext=(170, 76000),
             arrowprops=dict(facecolor='#FFFFFF', edgecolor='red', shrink=0.01, linewidth=1), color='r')

plt.ylim((0, 83000))

plt.legend(loc='upper center', ncol=2, labelspacing=0.01,
           frameon=False, bbox_to_anchor=(0.5, 1.25))
# plt.show()

# ticks = plt.gca().get_yticks()
# new_ticks = [str(int(tick/1000)) + 'K' for tick in ticks]
# plt.gca().set_yticklabels(new_ticks)
plt.xlabel("Elapsed time (sec)")
plt.ylabel("Throughput (ops/sec)")
plt.tight_layout()

font = fm.FontProperties(fname='arial.ttf')
plt.savefig("motivation.pdf", bbox_inches='tight')


plt.plot()
