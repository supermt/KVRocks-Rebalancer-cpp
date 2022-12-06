#!/usr/bin/bash
nohup /home/supermt/CLionProjects/kvrocks-rebalancer-cpp/cmake-build-debug/cluster-balance > balance.log 2>&1 & 
/home/supermt/CLionProjects/YCSB-cpp-Redis/ycsb -run -db redis -P ycsb/workloada -P ycsb/cluster.prop -s
redis-cli -h 127.0.0.1 -p 30001 stats > rocks_stat/with_migration.node1.stat
redis-cli -h 127.0.0.1 -p 30002 stats > rocks_stat/with_migration.node2.stat
redis-cli -h 127.0.0.1 -p 30003 stats > rocks_stat/with_migration.node3.stat
