cat node_30001/kvrocks.INFO |grep -a slot > migration_info/migrate_while_reading/node1
cat node_30002/kvrocks.INFO |grep -a slot > migration_info/migrate_while_reading/node2
cat node_30003/kvrocks.INFO |grep -a slot > migration_info/migrate_while_reading/node3
