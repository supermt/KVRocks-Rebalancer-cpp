./create_cluster.sh stop
./create_cluster.sh start
./create_cluster.sh create

echo "Server created"
date +"%H:%M:%S.%s"
../../../redis/src/redis-benchmark -p 40001 -t hset -n 1000000 -r 100000000 -d 1000 -q -P 100 --cluster -c 2
mv ./redis-benchamrk.result ./redis-benchamrk.result_dual_node
#nohup ./migrate.sh 0 > balance.log & 
./migrate.sh 0
date +"%H:%M:%S.%s"
../../../redis/src/redis-benchmark -p 40001 -t hset -n 40000000 -r 100000000 -d 1000 -q -P 100 --cluster -c 2
d -c 2ate +"%H:%M:%S.%s"
mv ./redis-benchamrk.result ./redis-benchamrk.result_triple_node
echo "Data loaded"
