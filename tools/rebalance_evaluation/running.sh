#!/usr/bin/bash
export WORKLOAD="../mixgraph/workload$1"
echo $WORKLOAD

../../../YCSB-cpp-Redis/ycsb -run -db redis -P $WORKLOAD -p status.interval=1 -P ../ycsb/cluster.prop -s -threads $2
