./create_cluster.sh stop 1
./create_cluster.sh start 1
./create_cluster.sh create 1

echo "Server created"
nohup nethogs -a -t  > network.log & 
./loading.sh $1 8

echo "Data loaded"
nohup ./migrate.sh 1 > balance.log & 
nohup ./rocks_stat.sh 40001 > server_40001.log & 
nohup ./rocks_stat.sh 40002 > server_40002.log & 

#./running.sh $1 16 > qps.log
./running.sh $1 16
pkill -f "nethogs"
pkill -f "./rocks_stat.sh "

mkdir result_log
mv *.stat result_log/
mv *.log result_log/
mv load_* result_log/
mv run_* result_log/

mv result_log result_log_push_$1
cp /nvme/jinghuan/node_40001/kvrocks.*.INFO* result_log_push_$1/node1_info.log
cp /nvme/jinghuan/node_40002/kvrocks.*.INFO* result_log_push_$1/node2_info.log
