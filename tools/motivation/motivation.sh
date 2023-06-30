./create_cluster.sh stop
./create_cluster.sh start
./create_cluster.sh create

echo "Server created"
nohup nethogs -a -t  > network.log & 
./loading.sh a 6

echo "Data loaded"
nohup ./migrate.sh 1 > balance.log & 
nohup ./rocks_stat.sh 40001 > server_40001.log & 
nohup ./rocks_stat.sh 40002 > server_40002.log & 
#nohup ./migrate.sh 1 > balance.log & 

./running.sh a 12
pkill -f "nethogs"
pkill -f "./rocks_stat.sh "

mkdir result_log
mv *.stat result_log/
mv balance.log result_log/
mv server*.log result_log/
