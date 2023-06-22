./create_cluster.sh stop
./create_cluster.sh start
./create_cluster.sh create

echo "Server created"
#./loading.sh i
../../../redis/src/redis-benchmark -p 40001 -t hset -n 10000000 -r 100000000 -d 1000 -q -P 100 --cluster -c 1
#../../../redis/src/redis-benchmark -p 40001 -t set -n 10000000 -r 100000000 -d 1000 -q -P 1000 --cluster
mv ./redis-benchamrk.result ./redis-benchamrk.result_single_node
echo "Data loaded"
#./running.sh i
