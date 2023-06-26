import sys

from utils.load_balance import allocate_slots_for_servers
from utils.utils import *

if __name__ == '__main__':
    # Example usage
    startup_nodes = [{"host": "127.0.0.1", "port": "40001"}, {"host": "127.0.0.1", "port": "40002"},{"host": "127.0.0.1", "port": "40003"}]
    startup_nodes = [{"host": "127.0.0.1", "port": "40001"}, {"host": "127.0.0.1", "port": "40002"}]
    rc, server_links = get_link_list_from_nodes(startup_nodes)
    node_info = rc.cluster_nodes()
    print("Migration method:", sys.argv[1])
    migration_candidates = allocate_slots_for_servers(node_info)
    print(migration_candidates[0],migration_candidates[-1])
    migrate_cmd_list = calculate_migration_plan(migration_candidates, rc, server_links, int(sys.argv[1]))
    apply_migration_cmd_with_slots(migrate_cmd_list, rc, server_links)

#    imported = False
#    while True:
#        for server_id in LOG_FILE_MAP:
#            print(server_id,imported)
#            imported = import_success(LOG_FILE_MAP[server_id],migration_candidates[-1][0])
#            if imported:
#                break
#        time.sleep(1)

#    broadcast_topo_batched(migration_candidates,rc)
