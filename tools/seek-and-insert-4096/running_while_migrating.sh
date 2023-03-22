#!/usr/bin/bash
export WORKLOAD="../ycsb/workload$1"
echo $WORKLOAD

mkdir -p result/stats/

redis-cli -h 127.0.0.1 -p 40001 stats > result/stats/before_migration.node1.stat
redis-cli -h 127.0.0.1 -p 40002 stats > result/stats/before_migration.node2.stat

nohup ./migrate.sh > balance.log 2>&1 & 
../../../YCSB-cpp-Redis/ycsb -run -db redis -P $WORKLOAD -p status.interval=1 -P ../ycsb/cluster.prop -s -threads 6

redis-cli -h 127.0.0.1 -p 40001 stats > result/stats/after_migration.node1.stat
redis-cli -h 127.0.0.1 -p 40002 stats > result/stats/after_migration.node2.stat

