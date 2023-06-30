import os

import redis

from utils.utils import get_link_list_from_nodes, detect_ranges, get_cluster_version

if __name__ == '__main__':
    # Example usage
    # CLUSTERX SETNODES "kvrockskvrockskvrockskvrockskvrocksnode1 10.32.68.251 6666 master - 0-5460 \n
    # kvrockskvrockskvrockskvrockskvrocksnode2 10.32.68.250 6667 master - 5461-10992 \n
    # kvrockskvrockskvrockskvrockskvrocksnode3 10.32.68.249 6666 master - 10993-16383" 1
    # get the link and topo first
    startup_nodes = [{"host": "127.0.0.1", "port": "40001"},{"host": "127.0.0.1", "port": "40002"}]
    expended_nodes = [{"host": "127.0.0.1", "port": "40003", "master": None}]

    startup_nodes = [{"host": "127.0.0.1", "port": "40001"}]
    expended_nodes = [{"host": "127.0.0.1", "port": "40002", "master": None}]



    added_nodes = []

    rc, old_server_links = get_link_list_from_nodes(startup_nodes)
    node_info = rc.cluster_nodes()

    # Get old topo from node info
    old_topo = ""
    for node in node_info:
        print(node['id'], node['host'], node['port'])
        # for each server, list the info
        master_id = ""
        role = ""
        if node["master"]:
            master_id = node["master"]
            role = "slave"
        else:
            master_id = "-"
            role = "master"

        slot_str = ""
        ranges = detect_ranges(node["slots"])
        for slot_range in ranges:
            if slot_range[0] == slot_range[1]:
                # (1,1)
                slot_str += (str(slot_range[0]) + " ")
            else:
                slot_str += (str(slot_range[0]) + "-" + str(slot_range[1]) + " ")

        # $node_id $ip $port $role $master_node_id $slot_range
        server_info = "%s %s %s %s %s %s" % (node["id"], node["host"], node["port"], role, master_id, slot_str)
        old_topo += (server_info + "\n")

    for expended_node in expended_nodes:
        exists = False
        for node in node_info:
            if expended_node["host"] == node["host"] and int(expended_node["port"]) == int(node["port"]):
                exists = True
        if not exists:
            added_nodes.append(expended_node)
    #print("Adding nodes:", added_nodes)
    #print("Old topo:", old_topo)
    new_topo = old_topo
    # now, get the new topo, and create the command list for CLUSTERX SETNODEID $NODE_ID
    new_server_links = []
    set_node_id_cmd_list = []
    #
    i = len(node_info)
    for server in added_nodes:
        i += 1
        new_server_links.append(redis.Redis(server["host"], int(server["port"])))
        server_id = "kvrockskvrockskvrockskvrockskvrocksnode" + str(i)
        master_id = server["master"]
        role = "slave"
        if not master_id:
            role = "master"
            master_id = "-"
        slot_str = ""  # don't allocate slots for new servers
        server_info = "%s %s %s %s %s %s" % (server_id, server["host"], server["port"], role, master_id, slot_str)
        new_topo += (server_info + "\n")
        set_node_id_cmd = "CLUSTERX SETNODEID %s" % server_id
        set_node_id_cmd_list.append(set_node_id_cmd)
    new_topo = '\"' + new_topo[:-1] + '\"'
    # publish the new cluster version into all servers

    all_server = []
    all_server.extend(startup_nodes)
    all_server.extend(added_nodes)

    # all_server_list = []
    # for server in all_server:
    #     all_server_list.append(redis.Redis(server["host"], server["port"]))
    #
    if len(added_nodes) > 0:
        version = get_cluster_version(rc)
        version += 1
        for server in all_server:
            # It can only be finished in os.sys
            target_command = "redis-cli -h %s -p %s CLUSTERX SETNODES %s %d" % (
                server["host"], server["port"], new_topo, version)
            # target_command = "CLUSTERX SETNODES %s %d" % (new_topo, version)
            # print(target_command)
            # reply = server.execute_command(*target_command.split())
            # print(reply)
            os.system(target_command)
        node_info = rc.cluster_nodes()

        print("Finished updating topo, version number:", get_cluster_version(rc))

        # for each new nodes, set node id for them
        index = 0
        for new_server in new_server_links:
            reply = new_server.execute_command(set_node_id_cmd_list[index])
            print(reply)
            index += 1
        print("Finished")
    else:
        print("No need for adding server")
