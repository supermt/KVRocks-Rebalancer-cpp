#!/usr/bin/bash
./create_cluster.sh stop
./create_cluster.sh start
./create_cluster.sh create
./migrate.sh
./batch_migrate.sh



