#!/usr/bin/bash
export WORKLOAD="../ycsb/workload$1"
echo $WORKLOAD

../ycsb/ycsb -run -db redis -P $WORKLOAD -P ../ycsb/cluster.prop -s -threads 6


