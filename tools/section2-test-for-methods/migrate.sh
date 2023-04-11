#!/usr/bin/bash
rm -rf /tmp/migration/*.sst
../../build/cluster-balance --port=40001 --weights="kvrockskvrockskvrockskvrockskvrocksnode1:1.0,kvrockskvrockskvrockskvrockskvrocksnode2:1.0" --new_node_port=40002 --new_node_id="kvrockskvrockskvrockskvrockskvrocksnode2" --migration_method=1
rm -rf /tmp/migration/*.sst

# redis-cli -p 40001 clusterx migrate 8192 16383 kvrockskvrockskvrockskvrockskvrocksnode2
