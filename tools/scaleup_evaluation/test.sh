./create_cluster.sh stop 3
./create_cluster.sh start 3
./create_cluster.sh create 3

echo "Server created"
#nohup nethogs -a -t  > network.log & 
#./loading.sh $1 2
./loading.sh a 8

echo "Data loaded"
./test_migrate.sh 3
#nohup ./migrate.sh 1 > balance.log & 
#nohup ./rocks_stat.sh 40001 > server_40001.log & 
#nohup ./rocks_stat.sh 40002 > server_40002.log & 
#nohup ./migrate.sh 1 > balance.log & 

#./running.sh a 8
pkill -f "nethogs"
#pkill -f "./rocks_stat.sh "

redis-cli -p 40001 cluster NODES
