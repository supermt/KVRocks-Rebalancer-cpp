#!/usr/bin/bash
./ycsb/ycsb -load -db redis -P ycsb/workloada -P ycsb/cluster.prop -s
