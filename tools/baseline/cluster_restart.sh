./create_cluster.sh stop
./create_cluster.sh start
./create_cluster.sh create

echo "Server created"
./loading.sh i
echo "Data loaded"
./running.sh i
