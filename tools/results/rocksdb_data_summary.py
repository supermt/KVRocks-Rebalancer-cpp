import matplotlib.pyplot as plt
import pandas as pd
import json


plt.rcParams['figure.figsize'] = (12, 6)  # 8 inches wide by 6 inches tall
plt.rcParams['font.size'] = 20  # 8 inches wide by 6 inches tall
plt.rcParams['font.family'] = 'Arial'


def get_qps(input_col):

    qps = input_col - input_col.shift(1)

    return qps[1:]


def read_df_from_file(node_log):

    stat_row = []

    for line in node_log:
        data = {}
        try:
            data = json.loads(line)
        except:
            print("non-json line: ", line)
            continue

        wal_writes = data["rocksdb.write.wal"]
        total_read = data["rocksdb.non.last.level.read.count"] + \
            data["rocksdb.last.level.read.count"]

        total_cache = data["rocksdb.block.cache.data.miss"] + \
            data["rocksdb.block.cache.data.hit"] + 1
        hit_count = data["rocksdb.block.cache.data.hit"]
        print("total, hit count", total_cache, hit_count)

        hit_ratio = hit_count/total_cache
        seek_next_found = float(
            data["rocksdb.number.db.next.found"]) / float(data["rocksdb.number.db.next"] + 1)
        stat_row.append([wal_writes, total_read, hit_ratio, seek_next_found])

    node_stat = pd.DataFrame(stat_row, columns=[
        "WAL_writes", "Total Reads", "hit ratio", "Seek found ratio"])

    return node_stat


node1_logs = open("migration_result_log/server_40001.log", "r").readlines()
node2_logs = open("migration_result_log/server_40002.log", "r").readlines()

single_node_logs = open(
    "single_result_log/server_40001.log", "r").readlines()
double_node1_logs = open(
    "double_result_log/server_40001.log", "r").readlines()
double_node2_logs = open(
    "double_result_log/server_40002.log", "r").readlines()


node_1_stat = read_df_from_file(node1_logs)
node_2_stat = read_df_from_file(node2_logs)

single_baseline_node_1_stat = read_df_from_file(single_node_logs)

double_baseline_node_1_stat = read_df_from_file(double_node1_logs)
double_baseline_node_2_stat = read_df_from_file(double_node2_logs)


node1_qps_w = get_qps(node_1_stat["WAL_writes"])
node2_qps_w = get_qps(node_2_stat["WAL_writes"])
double_node1_qps_w = get_qps(double_baseline_node_1_stat["WAL_writes"])
double_node2_qps_w = get_qps(double_baseline_node_2_stat["WAL_writes"])
single_node_qps_w = get_qps(single_baseline_node_1_stat["WAL_writes"])


node1_qps_r = get_qps(node_1_stat["Total Reads"])
node2_qps_r = get_qps(node_2_stat["Total Reads"])
double_node1_qps_r = get_qps(double_baseline_node_1_stat["Total Reads"])
double_node2_qps_r = get_qps(double_baseline_node_2_stat["Total Reads"])
single_node_qps_r = get_qps(single_baseline_node_1_stat["Total Reads"])

node1_hit_r = node_1_stat["hit ratio"]
node2_hit_r = node_2_stat["hit ratio"]
double_node1_hit_r = double_baseline_node_1_stat["hit ratio"]
double_node2_hit_r = double_baseline_node_2_stat["hit ratio"]
single_node_hit_r = single_baseline_node_1_stat["hit ratio"]



plt.plot(double_node1_qps_w[10:310], linestyle="--", label="Node 1 (Baseline Sever 1)")
plt.plot(double_node2_qps_w[10:310], linestyle="--",  label="Node 2 (Baseline Server 2)")

plt.plot(node1_qps_w[10:310], label="Node 1 (Migation Source)")
plt.plot(node2_qps_w[10:310], label="Node 2 (Migration Destination)")

# plt.plot(single_node_qps_w,linestyle=":",  label="Write throughput of Node 1 (single baseline)")

# annotations
important_lines = [20, 223, 298]
for important_x in important_lines:
    plt.axvline(important_x, ls=":", color="r", linewidth=4)

plt.annotate('Migration start', xy=(20, 35000), xytext=(50, 32000),
             arrowprops=dict(facecolor='#FFFFFF', edgecolor='red', shrink=0.01, linewidth=1), color='r')
plt.annotate('End of send snapshot', xy=(223, 35000), xytext=(75, 36000),
             arrowprops=dict(facecolor='#FFFFFF', edgecolor='red', shrink=0.01, linewidth=1), color='r')

plt.annotate('End of migration', xy=(298, 35000), xytext=(225, 36000),
             arrowprops=dict(facecolor='#FFFFFF', edgecolor='red', shrink=0.01, linewidth=1), color='r')


plt.ylim((0, 42000))

plt.legend(loc='upper center', ncol=2, labelspacing=0.01,
           frameon=False, bbox_to_anchor=(0.5, 1.25))

plt.xlabel("Elapsed time (sec)")
plt.ylabel("Throughput (ops/sec)")

plt.tight_layout()
plt.savefig("qps.pdf", bbox_inches='tight')