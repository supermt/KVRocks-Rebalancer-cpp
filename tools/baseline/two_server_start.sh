# kvrockskvrockskvrockskvrockskvrocksnode1 10.218.109.65 40001 master - 0-8191 kvrockskvrockskvrockskvrockskvrocksnode2 10.218.110.135 40001 master - 8192-16383
redis-cli -h 10.218.109.65 -p 40001 clusterx setnodes "kvrockskvrockskvrockskvrockskvrocksnode1 10.218.109.65 40001 master - 0-8191 kvrockskvrockskvrockskvrockskvrocksnode2 10.218.110.135 40001 master - 8192-16383" 1
redis-cli -h 10.218.109.65 -p 40001 clusterx setnodeid kvrockskvrockskvrockskvrockskvrocksnode1

redis-cli -h 10.218.110.135 -p 40001 clusterx setnodes "kvrockskvrockskvrockskvrockskvrocksnode1 10.218.109.65 40001 master - 0-8191 kvrockskvrockskvrockskvrockskvrocksnode2 10.218.110.135 40001 master - 8192-16383" 1
redis-cli -h 10.218.110.135 -p 40001 clusterx setnodeid kvrockskvrockskvrockskvrockskvrocksnode2
