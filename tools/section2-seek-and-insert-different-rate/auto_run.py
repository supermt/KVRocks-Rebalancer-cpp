#!/usr/bin/python3

import os

DIR_ROCKS_STATES = "rocks_stat/"
MIG_SPEED_TUPLE = "migrate-speed"


def update_config(back_name, load_name, migrate_speed):
    lines = open(back_name, "r").readlines()
    for i in range(len(lines)):
        if MIG_SPEED_TUPLE in lines[i]:
            lines[i] = MIG_SPEED_TUPLE + " " + str(migrate_speed) + "\n"

    out_file = open(load_name, "w")
    out_file.writelines(lines)
    return


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


for speed in [2048, 4096, 20480, 40960, 0]:
    for workload in ['a']:  # ,'b','c','d','e','f']:
        DIR_workload = DIR_ROCKS_STATES + "/" + str(speed) + "/" + workload + "/"
        update_config("back.conf", "iterate.conf", speed)
        DIR_int = DIR_workload + "together/"

        create_if_not_exist(DIR_int)

        RSLIST_int = get_files_in_dir(DIR_int)

        if len(RSLIST_int) == 0:
            print("Running workload" + workload)
            # No result, run the experiment
            os.system("./create_cluster.sh stop")
            os.system("./create_cluster.sh start")
            os.system("./create_cluster.sh create")
            os.system("./loading.sh > " + DIR_int + "load_result")
            os.system("./running_while_migrating.sh " + workload + " > " + DIR_int + "run_result")
            os.system("mv result/stats/* " + DIR_int + "/")
            os.system("mv load_* " + DIR_int + "/")
            os.system("mv run_* " + DIR_int + "/")
            os.system("./copy_log_stat.sh")
            os.system("mv logs " + DIR_int + "/")
