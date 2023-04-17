./create_cluster.sh stop
./create_cluster.sh start
./create_cluster.sh create
#./loading.sh
./migrate.sh 0

#redis-cli -c -p 40001 clusterx migrate 2410 2518  kvrockskvrockskvrockskvrockskvrocksnode2
#redis-cli -p 40001 clusterx setslot 2515 node kvrockskvrockskvrockskvrockskvrocksnode2 3
#redis-cli -p 40002 clusterx setslot 2515 node kvrockskvrockskvrockskvrockskvrocksnode2 3

echo "40002 test"
redis-cli -c -p 40002 HMSET hello{hash_tag} field1 "Hello" field2 "World"
echo "40001 test"
redis-cli -c -p 40001 HMSET hello{hash_tag} field1 "Hello" field2 "World"
