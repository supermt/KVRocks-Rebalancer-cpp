./dual_create_cluster.sh stop
./dual_create_cluster.sh start
./dual_create_cluster.sh create

echo "Server created"
#./loading.sh i
../../../redis/src/redis-benchmark -p 40001 -t hset -n 40000000 -r 100000000 -d 1000 -q -P 100 --cluster -c 2
mv ./redis-benchamrk.result ./redis-benchamrk.result_dual_node
echo "Data loaded"
#./running.sh i
