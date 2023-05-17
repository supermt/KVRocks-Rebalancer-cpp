./create_cluster_hotness.sh stop
./create_cluster_hotness.sh start
./create_cluster_hotness.sh create

echo "Server created"
./loading.sh m
echo "Data loaded"
./migrate_hotness.sh 2

echo "40002 test"
redis-cli -c -p 40002 HMSET hello{hash_tag} field1 "Hello" field2 "World"
echo "40001 test"
redis-cli -c -p 40001 HMSET hello{hash_tag} field1 "Hello" field2 "World"
