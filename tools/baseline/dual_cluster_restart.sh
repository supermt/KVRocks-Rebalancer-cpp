./dual_create_cluster.sh stop
./dual_create_cluster.sh start
./dual_create_cluster.sh create

echo "Server created"
./loading.sh i
echo "Data loaded"
./running.sh i
