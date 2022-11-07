#include <iostream>
#include "main.h"

DEFINE_int32(port, 30001, "The cluster entry port");

DEFINE_string(host, "127.0.0.1", "The cluster entry ip");
DEFINE_double(balance_threshold, 0.02, "The balancing threshold");
DEFINE_int64(contributer_threshold, 0,
             "The threshold of contributor, rebalance will not be performed when the "
             "number of contributor is lower than this value");

DEFINE_bool(include_empty_nodes, true,
            "Whether the Rebalance operation include empty nodes?");

DEFINE_string(operations, "add-node,rebalance", "choose the operation");
DEFINE_string(weights,
              "kvrockskvrockskvrockskvrockskvrocksnode1:1.0,"
              "kvrockskvrockskvrockskvrockskvrocksnode2:1.0,"
              "kvrockskvrockskvrockskvrockskvrocksnode3:1.0",
              "the weight pairs, it should be like the following format, \'ididididididid:score,dididididididi:score,dididididi:score\'");
DEFINE_string(new_node_host, "127.0.0.1", "new server's host");
DEFINE_string(new_node_port, "30004", "new server's host");
DEFINE_string(new_node_id, "kvrockskvrockskvrockskvrockskvrocksnode3",
              "new server's host");


class NodeInfo {
public:
  explicit NodeInfo(const std::string &node_info_line) {
   std::stringstream ss(node_info_line);
   std::string entry;
   while (getline(ss, entry, ' ')) {
    information_list.push_back(entry);
   }
   id = information_list[0];
   location = information_list[1];
   is_master = information_list[3] == "-";
   master = information_list[3];
   config_epoch = information_list[6];
   assert(information_list[7] == "connected");
   for (int i = 8; i < information_list.size(); i++) {
    slot_ranges.push_back(information_list[i]);
    std::stringstream stream_slots(information_list[i]);
    std::string slot;
    int num = 0;
    while (getline(stream_slots, slot, '-')) {
     slots.push_back(std::stoi(slot));
     num++;
    }
    if (num == 2) {
     auto min = slots.at(slots.size() - 2);
     auto max = slots.at(slots.size() - 1);
     for (int j = min + 1; j < max; j++) {
      slots.push_back(j);
     }
    }
   }
   std::sort(slots.begin(), slots.end());
  }

  std::string GetNodeId() { return id; }

  std::string GetMaster() { return master; }

  std::string GetLocation() { return location; }

  std::vector<std::string> GetSlotRangeList() { return slot_ranges; }

  std::pair<std::string, std::string> GetIPandPort() {
   std::pair<std::string, std::string> result;
   int reach_comma = 0;
   for (char c: location) {
    if (c == ':' || c == '@') {
     reach_comma++;
     continue;
    }

    if (reach_comma == 0) {
     result.first.push_back(c);
    } else if (reach_comma == 1) {
     result.second.push_back(c);
    } else if (reach_comma == 2) {
     return result;
    }
   }
   return result;
  }

  bool IsMaster() { return is_master; }

  std::vector<int> GetSlotNumberList() { return slots; }

  int GetNewestVersion() { return std::stoi(config_epoch); }

private:
  bool is_master = false;
  std::vector<int> slots;
  std::vector<std::string> information_list;
  std::string id; // 0
  std::string location; // 1
  std::string flags; // 2
  std::string master; // 3
  std::string ping_sent; // 4
  std::string pong_recv; // 5
  std::string config_epoch; // 6
  std::string link_stat; // 7
  std::vector<std::string> slot_ranges; // 8
};

std::vector<std::string> StringSplitting(const std::string &input, char delim) {
 std::vector<std::string> results;
 std::string line;
 std::stringstream ss(input);
 while (std::getline(ss, line, delim)) {
  results.emplace_back(line);
 }
 return results;
}


std::unordered_map<std::string, float> ParseWeightPairString() {

 auto pairs = StringSplitting(FLAGS_weights, ',');
 std::unordered_map<std::string, float> result;

 for (auto pair: pairs) {
  auto entry = StringSplitting(pair, ':');
  assert(entry.size() == 2);
  result.emplace(entry[0], std::stof(entry[1]));
 }
 return result;
}

void CreateConnection(RedisCluster **target_link) {
 std::string target_link_posi =
     "tcp://" + FLAGS_host + ":" + std::to_string(FLAGS_port);
 *target_link = new RedisCluster(target_link_posi);
}

std::string GetNodeInfoString() {
 RedisCluster *cluster_ptr = nullptr;
 CreateConnection(&cluster_ptr);
 auto reply = cluster_ptr->command<OptionalString>("CLUSTER",
                                                   "NODES");
 return reply.value();
}

std::vector<NodeInfo> GetNodeInfoList() {
 RedisCluster *cluster_ptr = nullptr;
 CreateConnection(&cluster_ptr);

 auto reply = cluster_ptr->command<OptionalString>("CLUSTER",
                                                   "NODES");

 std::stringstream ss(reply.value());

 std::string line;
 std::vector<NodeInfo> infos;
 while (std::getline(ss, line, '\n')) {
  infos.emplace_back(line);
 }

// for (auto node: nodes) {
//  if (!node.GetSlotNumberList().empty())
//   std::cout << node.GetSlotNumberList()[1] << std::endl;
// }
 return infos;
}

int GetMaxVersion(const std::vector<NodeInfo> &info_list) {
 int max_version = 0;
 for (auto info: info_list) {
  auto current = info.GetNewestVersion();
  if (max_version < current) max_version = current;
 }
 return max_version;
}

inline std::string redis_cli_connection_head(NodeInfo &target) {
 std::string result = "redis-cli";
 auto loaction = target.GetIPandPort();
 result.append(" -h ").append(loaction.first);
 result.append(" -p ").append(loaction.second);
 return result;
}

struct MigrateCmd {
  MigrateCmd(int slot, NodeInfo &source, NodeInfo &target) : slot_(slot),
                                                             target_id_(
                                                                 target.GetNodeId()) {
   redis_cli_command = redis_cli_connection_head(source);
   redis_cli_command.append(" clusterx migrate ");
   redis_cli_command.append(std::to_string(slot));
   redis_cli_command.append(" ").append(target_id_);
  }

  int slot_;
  std::string target_id_;
  std::string redis_cli_command;
};

class MigrationOrder {
public:
  NodeInfo src_node_;
  NodeInfo dst_node_;
  uint32_t num_migrate_slots_;

  explicit MigrationOrder(const NodeInfo &src, const NodeInfo &dst,
                          int num_migrate_slots) :
      src_node_(src),
      dst_node_(dst), num_migrate_slots_(num_migrate_slots) {

  }


  std::vector<MigrateCmd> ComposeCommand() {
   std::vector<MigrateCmd> result;
   for (int i = 0; i < num_migrate_slots_; i++) {
    result.emplace_back(src_node_.GetSlotNumberList()[i], src_node_, dst_node_);
   }
   return result;
  }

};

std::unordered_map<std::string, int> GetNewTopology(int total_slot) {
 // calculate slot map
 float total_weight = 0;
 auto weight_map = ParseWeightPairString();
 std::cout << "weight map parsed: " << std::endl;
 for (auto wei: weight_map) {
  std::cout << "node: " << wei.first << ", weight: " << wei.second
            << std::endl;
  total_weight += wei.second;
 }
 int nodes_involved = weight_map.size();
 std::unordered_map<std::string, int> slot_number_map;
 int allocated_slots = 0;
 for (auto wei: weight_map) {
  int slot_num = total_slot * wei.second / total_weight;
  allocated_slots += slot_num;
  slot_number_map.emplace(wei.first, slot_num);
 }

 assert(slot_number_map.size() == weight_map.size());

 if (allocated_slots < total_slot) {
  slot_number_map.begin()->second += (total_slot - allocated_slots);
 }
 return slot_number_map;
}

int main(int argc, char **argv) {
 google::ParseCommandLineFlags(&argc, &argv, true);
 RedisCluster *cluster;
 CreateConnection(&cluster);
 std::stringstream operations(FLAGS_operations);
 std::string current_operation;
 while (getline(operations, current_operation, ',')) {
  if (current_operation == "add-node") {
   std::string cluster_info_string = GetNodeInfoString();
//   std::cout << cluster_info_string << std::endl;
   std::vector<NodeInfo> node_list = GetNodeInfoList();
   int max_version = GetMaxVersion(node_list);
   std::cout << "Current max version: " << max_version << std::endl;

   std::string new_host_string = "";
   new_host_string.append(FLAGS_new_node_id).append(" ");
   new_host_string.append(FLAGS_new_node_host).append(" ");
   new_host_string.append(FLAGS_new_node_port).append(" master - ");

   std::string old_topology = "";
   for (auto node_info: node_list) {
    old_topology.append(node_info.GetNodeId()).append(" ");
    auto ip_and_port = node_info.GetIPandPort();
    old_topology.append(ip_and_port.first).append(" ").append(
        ip_and_port.second).append(" ");
    old_topology.append(node_info.IsMaster() ? "master" : "slave").append(" ");
    old_topology.append(node_info.GetMaster()).append(" ");
    for (auto slot_range: node_info.GetSlotRangeList()) {
     old_topology.append(slot_range).append(" ");
    }
    old_topology.push_back('\n');
   }

   std::string new_topology = old_topology + new_host_string;
   for (auto node: node_list) {
    auto ip_and_port = node.GetIPandPort();
    auto set_slot_cmd =
        "redis-cli -h " + ip_and_port.first + " -p " + ip_and_port.second +
        " clusterx setnodes " + "\"" + new_topology + "\" " +
        std::to_string(max_version + 1);

    auto set_node_id_cmd =
        "redis-cli -h " + ip_and_port.first + " -p " + ip_and_port.second +
        " clusterx setnodeid " + node.GetNodeId();
    system(set_slot_cmd.c_str());
    system(set_node_id_cmd.c_str());
   }
   std::cout << "new nodes added" << std::endl;
//   redis-cli -h 127.0.0.1 -p $PORT clusterx setnodes "${cluster_nodes}" 1
//   redis-cli -h 127.0.0.1 -p $PORT clusterx setnodeid ${node_id[$index]}

  } else if (current_operation == "rebalance") {
   // get current topology
   auto node_list = GetNodeInfoList();
   int total_slot = 0;
   for (auto node: node_list) {
    total_slot += node.GetSlotNumberList().size();
   }
   int newest_version = GetMaxVersion(node_list);

   auto new_topo = GetNewTopology(total_slot);

   std::cout << "\n>>>> current slot mapping is as follow <<<<\n" << std::endl;
   for (auto node: node_list) {
    std::cout << node.GetNodeId() << " slots in node: "
              << node.GetSlotNumberList().size() << std::endl;
   }

   std::cout << "\n>>>> target slot mapping is as follow <<<<\n" << std::endl;
   for (auto slot_entry: new_topo) {
    std::cout << slot_entry.first << " slots in node: " << slot_entry.second
              << std::endl;
   }

   std::unordered_map<std::string, int> string;
   int num_moved_out_slots = 0; // how many slots will be moved outside
   int num_moved_in_slots = 0; // how many slots will be moved into
   std::vector<std::pair<NodeInfo, int>> contributor_list; // how many nodes will contribute there slots
   std::vector<std::pair<NodeInfo, int>> acceptor_list; // how many nodes will accept other slots
   // calculate how many slots should be migrated from each node

   int unbalanced_nodes = 0;

   for (auto node: node_list) {
    int contributed_slots =
        static_cast<int>(node.GetSlotNumberList().size()) -
        new_topo[node.GetNodeId()];
    if (contributed_slots > 0 && contributed_slots > FLAGS_balance_threshold *
                                                     node.GetSlotNumberList().size()) {
     contributor_list.emplace_back(node, contributed_slots);
     num_moved_out_slots += contributed_slots;
     unbalanced_nodes++;
    } else if (contributed_slots < 0 &&
               -contributed_slots > FLAGS_balance_threshold *
                                    node.GetSlotNumberList().size()) {
     acceptor_list.emplace_back(node, -contributed_slots);
     num_moved_in_slots -= contributed_slots;
     unbalanced_nodes++;
    }
   }

   if (unbalanced_nodes < FLAGS_contributer_threshold) {
    std::cout << "No enough contributor, skip the migration" << std::endl;
   }

   std::vector<std::vector<MigrateCmd>> cmd_lists;

   // calculate how many slots will be moved to the acceptors
   for (int i = 0; i < acceptor_list.size(); i++) {
    for (int j = 0; j < contributor_list.size(); j++) {
     int num_migrate_slots = acceptor_list[i].second *
                             ((float) contributor_list[j].second /
                              num_moved_out_slots);

     MigrationOrder order(contributor_list[j].first, acceptor_list[i].first,
                          num_migrate_slots);
     auto cmd_set = order.ComposeCommand();

     std::cout << "rule: " << contributor_list[j].first.GetNodeId() << " to "
               << acceptor_list[i].first.GetNodeId() << " number of slots: "
               << cmd_set.size() << std::endl;

     cmd_lists.push_back(cmd_set);
    }
   }

   for (const auto &cmd_list_for_each_node: cmd_lists) {
    for (const auto &cmd_args: cmd_list_for_each_node) {
     std::string migrate_cmd = cmd_args.redis_cli_command;
//     std::cout << migrate_cmd << std::endl;
     system(migrate_cmd.c_str());
     for (auto node: node_list) {
      std::string version_update_cmd = redis_cli_connection_head(node);
      version_update_cmd.append(" clusterx setslot ");
      version_update_cmd.append(std::to_string(cmd_args.slot_))
          .append(" NODE ").append(cmd_args.target_id_)
          .append(" ").append(std::to_string(newest_version));
//      std::cout << version_update_cmd << std::endl;
      system(version_update_cmd.c_str());
     }
     newest_version++;
    }

   }
  }


 }

 return 0;
}
