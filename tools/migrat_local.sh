#!/usr/bin/bash
rm -rf /tmp/migration/*.sst
../build/cluster-balance --port=40001
cat node_30001/kvrocks.INFO | grep -a slot >migration_info/node1
cat node_30002/kvrocks.INFO | grep -a slot >migration_info/node2
cat node_30003/kvrocks.INFO | grep -a slot >migration_info/node3
rm -rf /tmp/migration/*.sst