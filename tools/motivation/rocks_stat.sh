
rm node_$1_stat

while true
do
  redis-cli -p $1 stats
  sleep 1
done
