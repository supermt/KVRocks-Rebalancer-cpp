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




for workload in ['a']:#,'b','c','d','e','f']:
    DIR_workload = DIR_ROCKS_STATES + workload +"/";
    DIR_sep = DIR_workload + "separate/"
    DIR_int = DIR_workload + "together/"
    
    create_if_not_exist(DIR_sep)
    create_if_not_exist(DIR_int)

    RSLIST_sep = get_files_in_dir(DIR_sep)
    RSLIST_int = get_files_in_dir(DIR_int)
    print(DIR_sep)
    if len(RSLIST_sep)==0:
        # No result, run the experiment
        print("Running workload"+workload)
        os.system("./create_cluster.sh stop")
        os.system("./create_cluster.sh start")
        os.system("./create_cluster.sh create") 
        os.system("./loading.sh > "+DIR_sep+"load_result")
        os.system("./running_after_migrating.sh " + workload +" > " +DIR_sep+"run_result")
        os.system("mv load_* "+ DIR_sep +"/")
        os.system("mv run_* "+ DIR_sep +"/")

    if len(RSLIST_int)==0:

        print("Running workload"+workload)
        # No result, run the experiment
        os.system("./create_cluster.sh stop")
        os.system("./create_cluster.sh start")
        os.system("./create_cluster.sh create") 
        os.system("./loading.sh > " +DIR_int+"load_result" )
        os.system("./running_while_migrating.sh " + workload + " > " +DIR_int+"run_result")
        os.system("mv load_* "+ DIR_int +"/")
        os.system("mv run_* "+ DIR_int +"/")

