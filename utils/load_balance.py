import json
import sys

import redis
from rediscluster import RedisCluster


def allocate_slots_for_servers(node_info):
    key_ranges = []
    for node in node_info:
        redis_client = redis.StrictRedis(node["host"], int(node["port"]))
        data = redis_client.execute_command("hotness").decode('utf-8')
        data = json.loads(data)
        for slot_num in data:
            key_ranges.append((slot_num, data[slot_num]))

    server_assignments = load_balance(key_ranges, len(node_info))
    print(server_assignments)
    rebalanced_slots = []
    for i in range(len(key_ranges)):
        slot_num = int(key_ranges[i][0])
        target_server = node_info[server_assignments[i]]
        rebalanced_slots.append([slot_num, target_server, server_assignments[i]])

    migration_candidates = []
    for slot in rebalanced_slots:
        server_info = slot[1]
        slot_num = slot[0]
        if slot_num not in server_info["slots"]:
            migration_candidates.append((slot_num, server_info["id"]))
    # print(migration_candidates[0], migration_candidates[-1])
    return migration_candidates


def load_balance(slots, num_servers):
    # Calculate the total access time for all slots
    total_access_time = sum(slot[1] for slot in slots)

    # Calculate the target access time per server
    target_access_time = total_access_time / num_servers

    # Initialize the current access time for each server to 0
    current_access_time = [0] * num_servers

    # Initialize the server assignments for each slot to -1
    server_assignments = [-1] * len(slots)

    # Sort the slots by access time in descending order
    sorted_slots = sorted(slots, key=lambda x: x[1], reverse=True)

    # Iterate through each slot and assign it to the least loaded server
    for slot in sorted_slots:
        least_loaded_server = current_access_time.index(min(current_access_time))
        server_assignments[slots.index(slot)] = least_loaded_server
        current_access_time[least_loaded_server] += slot[1]

    return server_assignments


if __name__ == '__main__':
    # Example usage

    #
    startup_nodes = [{"host": "127.0.0.1", "port": "40001"}, {"host": "127.0.0.1", "port": "40002"}]
    server_links = []
    for start_server in startup_nodes:
        server_links.append(redis.Redis(start_server["host"], start_server["port"]))

    rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)
    node_info = rc.cluster_nodes()

    migration_candidates = allocate_slots_for_servers(node_info)

    migrate_cmd_list = []

    if int(sys.argv[1]) >= 1:
        slot_str_map = {x["id"]: "" for x in node_info}  # {id:"1,2,3,4",id2:"5,6,7,8"}

        for candidate in migration_candidates:
            server_id = candidate[1]
            slot_id = candidate[0]
            slot_str_map[server_id] += (str(slot_id) + ",")
        for server in slot_str_map:
            if slot_str_map[server] != "":
                migrate_cmd_list.append("clusterx migrate " + slot_str_map[server] + " " + server)
    else:
        migrate_cmd_list = ["clusterx migrate " + str(x[0]) + " " + x[1] for x in migration_candidates]

    version = rc.execute_command("CLUSTERX", "VERSION")
    version = int(version)

    # Send Migration Commands to cluster servers

    for cmd in migrate_cmd_list:
        migrate_reply = rc.execute_command(*cmd.split())
        slots = cmd.split()[2].split(",")
        for slot in slots:
            if slot != "":
                version += 1
                # CLUSTERX SETSLOT $SLOT_ID NODE $NODE_ID $VERSION
                set_slot_cmd = "CLUSTERX SETSLOT " + slot + " NODE " + cmd.split()[-1] + " " + str(version)
                for server_link in server_links:
                    set_slot_reply = server_link.execute_command(set_slot_cmd)
                if version % 100 == 0:
                    print("Cluster version:", version, "Setting Response:", set_slot_reply)
