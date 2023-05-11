#!/usr/bin/python3

import os

DIR_ROCKS_STATES = "rocks_stat/"


def get_files_in_dir(DIR):
    result_file_lists = []
    for path in os.listdir(DIR):
        # check if current path is a file
        if os.path.isfile(os.path.join(DIR, path)):
            result_file_lists.append(path)

    return result_file_lists


def create_if_not_exist(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return


def change_config(input_file, output_file, config_name, config_value):
    lines = open(input_file, "r").readlines()
    out = open(output_file, "w")
    target_config = []
    for line in lines:
        if config_name in line:
            line = config_name + " " + str(config_value) + "\n"
            print("configure line changed:", config_name, config_value)
        target_config.append(line)
    # print(target_config)
    out.writelines(target_config)
    out.close()
    return


method_list = ["baseline", "parallel-baseline", "pull-non-expanded", "level"]

for migration_method in [1]:
    for workload in ['a']:  # ,'b','c','d','e','f']:
        DIR_workload = DIR_ROCKS_STATES + workload + "/"
        DIR_int = DIR_workload + "together/" + method_list[migration_method] + "/"
        # print("migration method", migration_method)
        change_config("back.conf", "iterate.conf", "migrate-method", migration_method)
        create_if_not_exist(DIR_int)

        RSLIST_int = get_files_in_dir(DIR_int)
        if len(RSLIST_int) == 0:
            print("Running workload" + workload)
            print("Target dir: " + DIR_int)
            # No result, run the experiment
            os.system("./create_cluster.sh stop")
            os.system("./create_cluster.sh start")
            os.system("./create_cluster.sh create")
            print("loading")
            os.system("./loading.sh > " + DIR_int + "load_result")

            print("migrating and running")
            os.system("redis-cli -h 127.0.0.1 -p 40001 stats >" + DIR_int + "/before_migration.node1.stat")
            os.system("redis-cli -h 127.0.0.1 -p 40002 stats >" + DIR_int + "/before_migration.node2.stat")
            os.system("./running_while_migrating.sh " + workload + " " + str(
                migration_method) + " > " + DIR_int + "run_result")
            os.system("redis-cli -h 127.0.0.1 -p 40001 stats >" + DIR_int + "/after_migration.node1.stat")
            os.system("redis-cli -h 127.0.0.1 -p 40002 stats >" + DIR_int + "/after_migration.node2.stat")
            print(">>>>>>>>>>>>>>>>>>>Cleaning<<<<<<<<<<<<<<<<<<<\n\n")

            os.system("mv load_* " + DIR_int + "/")
            os.system("mv run_* " + DIR_int + "/")
            create_if_not_exist(DIR_int + "/node_40001")
            create_if_not_exist(DIR_int + "/node_40002")
            os.system("mv node_40001/*.log.* " + DIR_int + "/node_40001/")
            os.system("mv node_40002/*.log.* " + DIR_int + "/node_40002/")
