#!/usr/bin/bash
redis-cli -h 127.0.0.1 -p 40001 stats > rocks_stat/before_migration.node1.stat
redis-cli -h 127.0.0.1 -p 40002 stats > rocks_stat/before_migration.node2.stat
redis-cli -h 127.0.0.1 -p 40003 stats > rocks_stat/before_migration.node3.stat
nohup ../../build/cluster-balance --port=40001 > balance.log 2>&1 & 
../ycsb/ycsb -run -db redis -P ../ycsb/workloada -P ../ycsb/cluster.prop -s -threads 6
redis-cli -h 127.0.0.1 -p 40001 stats > rocks_stat/after_migration.node1.stat
redis-cli -h 127.0.0.1 -p 40002 stats > rocks_stat/after_migration.node2.stat
redis-cli -h 127.0.0.1 -p 40003 stats > rocks_stat/after_migration.node3.stat
