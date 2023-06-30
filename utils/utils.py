import subprocess

import time
import redis
from rediscluster import RedisCluster

LOG_FILE_MAP = {"kvrockskvrockskvrockskvrockskvrocksnode1": "node_40001/kvrocks.INFO",
                "kvrockskvrockskvrockskvrockskvrocksnode2": "node_40002/kvrocks.INFO",
                "kvrockskvrockskvrockskvrockskvrocksnode3": "node_40003/kvrocks.INFO", }


def import_success(path, waiting_slot, lines=100, sleep_micros=10):
    try:
        output = subprocess.check_output("tail " + path + " -n " + str(lines), shell=True)
    except:
        return False

    return_str = output.decode("utf-8", "ignore")

    waiting_sentence = "Succeed to import slot " + str(waiting_slot)
    #waiting_sentence = "Clean resources of migrating slot " + str(waiting_slot)
    # time.sleep(10 * 0.000001)
    result = waiting_sentence in return_str
#    print("waiting on:", waiting_sentence, result)
    
    return result  # return False


def detect_ranges(lst):
    ranges = []
    i = 0
    while i < len(lst):
        j = i
        while j < len(lst) - 1 and lst[j + 1] == lst[j] + 1:
            j += 1
        if j > i:
            ranges.append((lst[i], lst[j]))
        elif j == i:
            ranges.append((lst[i], lst[i]))
        i = j + 1
    return ranges


def get_cluster_version(cluster_link):
    version = cluster_link.execute_command("CLUSTERX", "VERSION")
    return int(version)


def get_link_list_from_nodes(startup_nodes):
    server_links = []
    for start_server in startup_nodes:
        server_links.append(redis.Redis(start_server["host"], start_server["port"]))

    rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)
    return rc, server_links


def calculate_migration_plan(migration_candidates, cluster_link, server_links, migration_method=0):
    node_info = cluster_link.cluster_nodes()

    # We need to find the server that contains the slot, otherwise, it will report error
    # 1. create slot:server map
    old_topo = {}
    for node in node_info:
        for slot in node["slots"]:
            old_topo[slot] = node["id"]

    # 2. filter the migration candidates
    #    if the target server is the slot it belongs to, skip it.
    # {src: []}
    slots_need_move = {x["id"]: [] for x in node_info}

    slot_moving_count = 0
    for candidate in migration_candidates:
        # candidate = (slot_id, node_id)
        slot_id = candidate[0]
        server_id = candidate[1]
        src_server = old_topo[slot_id]
        if src_server != server_id:
            slot_moving_count += 1
            slots_need_move[src_server].append(candidate)

    # print("Filtered slots:", slots_need_move, "# of removed slots:", len(migration_candidates) - slot_moving_count)

    migrate_cmd_map = {x["id"]: [] for x in node_info}

    if int(migration_method) >= 1:
        # { "server_id" : [(slot_id,server_id),(slot_id,server_id)] }
        for src_server in slots_need_move:

            slot_str_map = {x["id"]: "" for x in node_info}  # {id:"1,2,3,4",id2:"5,6,7,8"}

            slots_in_this_server = slots_need_move[src_server]
            for candidate in slots_in_this_server:
                server_id = candidate[1]
                slot_id = candidate[0]
                slot_str_map[server_id] += (str(slot_id) + ",")
            for server in slot_str_map:
                if slot_str_map[server] != "":
                    migrate_cmd_map[src_server].append("clusterx migrate " + slot_str_map[server] + " " + server)
    else:
        for src_server in slots_need_move:
            migrate_cmd_map[src_server] = ["clusterx migrate " + str(x[0]) + " " + x[1] for x in
                                           slots_need_move[src_server]]

    return migrate_cmd_map


def apply_migration_cmd(migrate_cmd_map, cluster_link, server_links):
    node_info = cluster_link.cluster_nodes()

#    server_link_map = {x["id"]: redis.Redis(x["host"], x["port"]) for x in node_info}

    server_link_map = {x["id"]: (x["host"], x["port"]) for x in node_info}
    version = get_cluster_version(cluster_link)
    cmd_count = 0
    for server_id in migrate_cmd_map:
        for cmd in migrate_cmd_map[server_id]:
            success = False
            cmd_count +=1
            retry = 0
            server_info = server_link_map[server_id]
            system_command = "redis-cli -h %s -p %d " % (server_info[0],server_info[1])
            system_command += cmd
            output = subprocess.check_output(system_command.split())
            if cmd_count % 100 ==0:
                print("slot migrated:",cmd_count)

            slots = cmd.split()[2].split(",")
            target_server = cmd.split()[3]
            # print(target_server)
            # for slot in slots:
            retry=0

def apply_migration_cmd_with_slots(migrate_cmd_map, cluster_link, server_links):
    node_info = cluster_link.cluster_nodes()
    server_link_map = {x["id"]: (x["host"], x["port"]) for x in node_info}
    version = get_cluster_version(cluster_link)
    cmd_count = 0
    for server_id in migrate_cmd_map:
        for cmd in migrate_cmd_map[server_id]:
            success = False
            cmd_count +=1
            retry = 0
            server_info = server_link_map[server_id]
            system_command = "redis-cli -h %s -p %d " % (server_info[0],server_info[1])
            system_command += cmd
            output = subprocess.check_output(system_command.split())
#            while ("OK" not in str(output)):
#                time.sleep(0.00001)
#                output = subprocess.check_output(system_command.split())
#                print(output)
            if cmd_count % 100 ==0:
                print("slot migrat cmd sent:",cmd_count)

            slots = cmd.split()[2].split(",")
            target_server = cmd.split()[3]
            # print(target_server)
            # for slot in slots:
            retry=0

            slot_str=""
            for slot in slots:
                if slot != "":
                    slot_str+=(slot+",")
            slot_str = slot_str[:-1]
            print(slot_str[-50:])
            # CLUSTERX SETSLOT $SLOT_ID NODE $NODE_ID $VERSION
            version+=1
            set_slot_cmd = "CLUSTERX SETSLOT " + slot_str + " NODE " + target_server + " " + str(version)
            for server_id in server_link_map:
                server_info = server_link_map[server_id]
                system_command = "redis-cli -h %s -p %d " % (server_info[0],server_info[1])
                system_command += set_slot_cmd
                output = subprocess.check_output(system_command.split())
                print(output)

def broadcast_topo(migration_candidates, cluster_link):
    node_info = cluster_link.cluster_nodes()
    server_id_slots_map={x["id"]: [] for x in node_info}
    for slot_id_tuple in migration_candidates:
        new_server_id = slot_id_tuple[1]
        server_id_slots_map[new_server_id].append(slot_id_tuple[0])

    print(server_id_slots_map[new_server_id])

    version = get_cluster_version(cluster_link)
    server_id_address_map = {x["id"]: (x["host"], x["port"]) for x in node_info}

    for server_id in server_id_slots_map:
        slots =  server_id_slots_map[server_id]
        target_server = server_id
        # for each slot
        for slot in slots:
            # broad cast this slot to all server
            version = get_cluster_version(cluster_link)

            for server_id in server_id_address_map:
                server_info = server_id_address_map[server_id]
                system_command = "redis-cli -h %s -p %d " % (server_info[0],server_info[1])
                # CLUSTERX SETSLOT $SLOT_ID NODE $NODE_ID $VERSION
                target_cmd  = system_command + " CLUSTERX SETSLOT %d NODE %s %d" % (slot,target_server,version+1)
                output = subprocess.check_output(target_cmd.split())
                if version%1000 == 0:
                    print("Slot setting:",target_cmd,output)



def broadcast_topo_batched(migration_candidates, cluster_link):
    node_info = cluster_link.cluster_nodes()
    server_id_slots_map = {x["id"]: "" for x in node_info}
    for slot_id_tuple in migration_candidates:
        new_server_id = slot_id_tuple[1]
        server_id_slots_map[new_server_id] += (str(slot_id_tuple[0])+",")

    version = get_cluster_version(cluster_link)
    working_servers = {x["id"]: (x["host"], x["port"]) for x in node_info}

    for server_id in server_id_slots_map:
        slots = server_id_slots_map[server_id]
        if len(slots) > 0:

            target_server = server_id
            for server_id in working_servers:
                server_info = working_servers[server_id]
                system_command = "redis-cli -h %s -p %d " % (
                    server_info[0], server_info[1])
                # CLUSTERX SETSLOT $SLOT_ID NODE $NODE_ID $VERSION
                target_cmd = system_command + \
                    " CLUSTERX SETSLOT %s NODE %s %d" % (
                        slots, target_server, version+1)
                output = subprocess.check_output(target_cmd.split())
                print("Slot setting:", target_cmd[:20],"...",target_cmd[-20:],output)

    pass
