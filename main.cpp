#include <iostream>
#include "main.h"

DEFINE_int32(port, 30001, "The cluster entry port");

DEFINE_string(host, "127.0.0.1", "The cluster entry ip");

DEFINE_bool(include_empty_nodes, true,
            "Whether the Rebalance operation include empty nodes?");

DEFINE_string(operation, "add-node,rebalance", "choose the operation");

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

void GetNodeInfoList(std::vector<NodeInfo> *infos) {
 RedisCluster *cluster_ptr = nullptr;
 CreateConnection(&cluster_ptr);

 auto reply = cluster_ptr->command<OptionalString>("CLUSTER",
                                                   "NODES");

 std::stringstream ss(reply.value());

 std::string line;
 while (std::getline(ss, line, '\n')) {

  infos->emplace_back(line);
 }

// for (auto node: nodes) {
//  if (!node.GetSlotNumberList().empty())
//   std::cout << node.GetSlotNumberList()[1] << std::endl;
// }
}

int GetMaxVersion(const std::vector<NodeInfo> &info_list) {
 int max_version = 0;
 for (auto info: info_list) {
  auto current = info.GetNewestVersion();
  if (max_version < current) max_version = current;
 }
 return max_version;
}

int main(int argc, char **argv) {
 google::ParseCommandLineFlags(&argc, &argv, true);

 std::stringstream operations(FLAGS_operation);
 std::string current_operation;
 while (getline(operations, current_operation, ',')) {
  if (current_operation == "add-node") {
   std::string cluster_info_string = GetNodeInfoString();
//   std::cout << cluster_info_string << std::endl;
   std::vector<NodeInfo> node_list;
   GetNodeInfoList(&node_list);
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

//   redis-cli -h 127.0.0.1 -p $PORT clusterx setnodes "${cluster_nodes}" 1
//   redis-cli -h 127.0.0.1 -p $PORT clusterx setnodeid ${node_id[$index]}

  } else if (current_operation == "rebalance") {

  }
 }

 return 0;
}
