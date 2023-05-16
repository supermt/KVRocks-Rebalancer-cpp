import redis
from rediscluster import RedisCluster

def detect_ranges(lst):
    ranges = []
    i = 0
    while i < len(lst):
        j = i
        while j < len(lst) - 1 and lst[j+1] == lst[j]+1:
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


def apply_migration_plan(migration_candidates, cluster_link, server_links, migration_method=0):
    migrate_cmd_list = []
    node_info = cluster_link.cluster_nodes()
    if int(migration_method) >= 1:
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

    version = get_cluster_version(cluster_link)
    # Send Migration Commands to cluster servers
    success = False

    for cmd in migrate_cmd_list:
        migrate_reply = cluster_link.execute_command(*cmd.split())
        # migrate_reply = migrate_reply.decode("utf-8")
        if migrate_reply != "OK":
            print("Get unexpected results:", migrate_reply)
            return False
        slots = cmd.split()[2].split(",")
        for slot in slots:
            if slot != "":
                version += 1
                # CLUSTERX SETSLOT $SLOT_ID NODE $NODE_ID $VERSION
                set_slot_cmd = "CLUSTERX SETSLOT " + slot + " NODE " + cmd.split()[-1] + " " + str(version)
                for server_link in server_links:
                    set_slot_reply = server_link.execute_command(set_slot_cmd)
                    set_slot_reply = set_slot_reply.decode("utf-8")
                    if set_slot_reply != "OK":
                        print("Get unexpected results:", migrate_reply)
                        return False
                    if version % 100 == 0:
                        print("Cluster version:", version, "Setting Response:", set_slot_reply, "\t Client ID:",
                              server_link.client_id())

# if __name__ == '__main__':
# Example usage

#
# startup_nodes = [{"host": "127.0.0.1", "port": "40001"}, {"host": "127.0.0.1", "port": "40002"}]
# rc, server_links = get_link_list_from_nodes(startup_nodes)
# node_info = rc.cluster_nodes()
#
# migration_candidates = allocate_slots_for_servers(node_info)
# success_send = apply_migration_plan(migration_candidates, int(sys.argv[1]))
