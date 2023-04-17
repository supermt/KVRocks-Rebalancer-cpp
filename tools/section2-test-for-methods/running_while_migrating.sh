#!/usr/bin/bash
export WORKLOAD="../ycsb/workload$1"
echo $WORKLOAD

nohup ./migrate.sh $2 > balance.log 
../../../YCSB-cpp-Redis/ycsb -run -db redis -P $WORKLOAD -p status.interval=1 -P ../ycsb/cluster.prop -s -threads 6
