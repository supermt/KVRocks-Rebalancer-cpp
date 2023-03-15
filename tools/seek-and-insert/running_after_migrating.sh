#!/usr/bin/bash
export WORKLOAD="../ycsb/workload$1"
echo $WORKLOAD


redis-cli -h 127.0.0.1 -p 40001 stats > rocks_stat/$1/separate/before_migration.node1.stat
redis-cli -h 127.0.0.1 -p 40002 stats > rocks_stat/$1/separate/before_migration.node2.stat
redis-cli -h 127.0.0.1 -p 40003 stats > rocks_stat/$1/separate/before_migration.node3.stat

../../build/cluster-balance --port=40001
redis-cli -h 127.0.0.1 -p 40001 stats > rocks_stat/$1/separate/before_run.node1.stat
redis-cli -h 127.0.0.1 -p 40002 stats > rocks_stat/$1/separate/before_run.node2.stat
redis-cli -h 127.0.0.1 -p 40003 stats > rocks_stat/$1/separate/before_run.node3.stat

../../../YCSB-cpp-Redis/ycsb -run -db redis -P $WORKLOAD -P ../ycsb/cluster.prop -s -threads 6

redis-cli -h 127.0.0.1 -p 40001 stats > rocks_stat/$1/separate/after_run.node1.stat
redis-cli -h 127.0.0.1 -p 40002 stats > rocks_stat/$1/separate/after_run.node2.stat
redis-cli -h 127.0.0.1 -p 40003 stats > rocks_stat/$1/separate/after_run.node3.stat
