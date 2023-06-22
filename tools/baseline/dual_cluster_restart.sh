./dual_create_cluster.sh stop
./dual_create_cluster.sh start
./dual_create_cluster.sh create

echo "Server created"
#./loading.sh i
../../../redis/src/redis-benchmark -p 40001 -t set -n 10000000 -r 100000000 -d 1000 -q -P 1000  --cluster 
mv ./redis-benchamrk.result ./redis-benchamrk.result_dual_node
echo "Data loaded"
#./running.sh i
