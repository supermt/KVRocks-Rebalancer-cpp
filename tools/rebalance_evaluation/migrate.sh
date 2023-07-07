#!/usr/bin/bash
rm -rf /tmp/migration/*.sst
echo "Start Migration"
echo $1
export PYTHONPATH=$PYTHONPATH:../../
redis-cli -h 127.0.0.1 -p 40001 stats > ./before_migration.node1.stat
redis-cli -h 127.0.0.1 -p 40002 stats > ./before_migration.node2.stat


#sleep 20
echo ">>>>>>>>>>>>>>>>>>>>>>>>>>Add Server<<<<<<<<<<<<<<<<<<<<<<<<<<<"
#python3 ../../case_scaleup.py


echo ">>>>>>>>>>>>>>>>>>>>>>>>>>Load Balance<<<<<<<<<<<<<<<<<<<<<<<<<"
python3 ../../case_hotness_balance.py $1

redis-cli -h 127.0.0.1 -p 40001 stats > ./before_migration.node1.stat
redis-cli -h 127.0.0.1 -p 40002 stats > ./before_migration.node2.stat

date +"%H:%M:%S.%s"


echo "Migration Finished"
rm -rf /tmp/migration/*.sst

# redis-cli -c -p 40001 clusterx migrate 0 8192 kvrockskvrockskvrockskvrockskvrocksnode2

# redis-cli -c -p 40001 clusterx migrate 0 8192 kvrockskvrockskvrockskvrockskvrocksnode2

#redis-cli -p 40001 clusterx migrate 0 8192 kvrockskvrockskvrockskvrockskvrocksnode2
