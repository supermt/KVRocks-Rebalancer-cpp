#!/usr/bin/bash
#../../../YCSB-cpp-Redis/ycsb -load -db redis -P ../ycsb/workloadm -P ../ycsb/cluster.prop -s -threads 1
../../../YCSB-cpp-Redis/ycsb -load -db redis -P ../ycsb/workload$1 -P ../ycsb/cluster.prop -s -threads 1
#../../../YCSB-cpp-Redis/ycsb -run -db redis -P ../ycsb/workloadm -P ../ycsb/cluster.prop -s -threads 1
