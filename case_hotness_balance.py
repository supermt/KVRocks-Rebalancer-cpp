import sys

from utils.load_balance import allocate_slots_for_servers
from utils.utils import get_link_list_from_nodes, calculate_migration_plan, apply_migration_cmd

if __name__ == '__main__':
    # Example usage
    startup_nodes = [{"host": "127.0.0.1", "port": "40001"}, {"host": "127.0.0.1", "port": "40002"}]
    rc, server_links = get_link_list_from_nodes(startup_nodes)
    node_info = rc.cluster_nodes()
    print("Migration method:", sys.argv[1])
    migration_candidates = allocate_slots_for_servers(node_info)
    migrate_cmd_list = calculate_migration_plan(migration_candidates, rc, server_links, int(sys.argv[1]))
    # print(migrate_cmd_list)
    apply_migration_cmd(migrate_cmd_list, rc, server_links)
