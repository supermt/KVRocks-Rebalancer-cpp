./create_cluster.sh stop
./create_cluster.sh start
./create_cluster.sh create

echo "Server created"
date +"%H:%M:%S.%s"
../../../redis/src/redis-benchmark -p 40001 -t set -n 1000000 -r 100000000 -d 100 -q -P 1000 --cluster
mv ./redis-benchamrk.result ./redis-benchamrk.result_dual_node
#nohup ./migrate.sh 0 > balance.log & 
./migrate.sh 0
date +"%H:%M:%S.%s"
../../../redis/src/redis-benchmark -p 40001 -t set -n 400000000 -r 100000000 -d 100 -q -P 1000 --cluster
date +"%H:%M:%S.%s"
mv ./redis-benchamrk.result ./redis-benchamrk.result_triple_node
echo "Data loaded"
