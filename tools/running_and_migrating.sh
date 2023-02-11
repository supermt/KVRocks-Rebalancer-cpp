#!/usr/bin/bash
nohup ../build/cluster-balance > balance.log 2>&1 & 
./ycsb/ycsb -run -db redis -P ycsb/workloada -P ycsb/cluster.prop -s
redis-cli -h 127.0.0.1 -p 30001 stats > rocks_stat/with_migration.node1.stat
redis-cli -h 127.0.0.1 -p 30002 stats > rocks_stat/with_migration.node2.stat
redis-cli -h 127.0.0.1 -p 30003 stats > rocks_stat/with_migration.node3.stat
