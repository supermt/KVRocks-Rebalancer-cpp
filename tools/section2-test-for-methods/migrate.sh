#!/usr/bin/bash
rm -rf /tmp/migration/*.sst
echo "Start Migration"
../../build/cluster-balance --port=40001 --weights="kvrockskvrockskvrockskvrockskvrocksnode1:19.0,kvrockskvrockskvrockskvrockskvrocksnode2:1.0" --new_node_port=40002 --new_node_id="kvrockskvrockskvrockskvrockskvrocksnode2" --migration_method=$1 --operations="add-node,rebalance" 
rm -rf /tmp/migration/*.sst

# redis-cli -c -p 40001 clusterx migrate 0 8192 kvrockskvrockskvrockskvrockskvrocksnode2

# redis-cli -c -p 40001 clusterx migrate 0 8192 kvrockskvrockskvrockskvrockskvrocksnode2

#redis-cli -p 40001 clusterx migrate 0 8192 kvrockskvrockskvrockskvrockskvrocksnode2
