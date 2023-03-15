#!/usr/bin/bash
../../../YCSB-cpp-Redis/ycsb -load -db redis -P ../ycsb/workloada -P ../ycsb/cluster.prop -s -threads 6
