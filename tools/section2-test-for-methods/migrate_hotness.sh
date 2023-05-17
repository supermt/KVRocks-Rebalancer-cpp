#!/usr/bin/bash
rm -rf /tmp/migration/*.sst
echo "Start Migration"
echo $1
export PYTHONPATH=$PYTHONPATH:../../
echo ">>>>>>>>>>>>>>>>>>>>>>>>>>Add Server<<<<<<<<<<<<<<<<<<<<<<<<<<<"
#python3 ../../case_scaleup.py

#sleep 10

echo ">>>>>>>>>>>>>>>>>>>>>>>>>>Load Balance<<<<<<<<<<<<<<<<<<<<<<<<<"
python3 ../../case_hotness_balance.py $1
echo "Migration Finished"
rm -rf /tmp/migration/*.sst

# redis-cli -c -p 40001 clusterx migrate 0 8192 kvrockskvrockskvrockskvrockskvrocksnode2

# redis-cli -c -p 40001 clusterx migrate 0 8192 kvrockskvrockskvrockskvrockskvrocksnode2

#redis-cli -p 40001 clusterx migrate 0 8192 kvrockskvrockskvrockskvrockskvrocksnode2
