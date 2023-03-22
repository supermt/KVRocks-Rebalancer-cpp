#!/usr/bin/bash
rm -rf /tmp/migration/*.sst
sleep(30)
../../build/cluster-balance --port=40001 --weights="kvrockskvrockskvrockskvrockskvrocksnode1:1.0,kvrockskvrockskvrockskvrockskvrocksnode2:1.0" --new_node_port=40002 --new_node_id="kvrockskvrockskvrockskvrockskvrocksnode2"
rm -rf /tmp/migration/*.sst
