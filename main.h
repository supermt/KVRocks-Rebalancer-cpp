//
// Created by supermt on 11/4/22.
//

#ifndef UNTITLED_MAIN_H
#define UNTITLED_MAIN_H

//#include <redis/>
#include <sw/redis++/redis++.h>
#include <sw/redis++/redis.h>
#include <gflags/gflags.h>

using namespace sw::redis;
using namespace gflags;


Slot _parse_slot(redisReply *reply) {
 if (reply == nullptr) {
  throw ProtoError("null slot id");
 }

 auto slot = reply::parse<long long>(*reply);
 if (slot < 0) {
  throw ProtoError("negative slot id");
 }

 return static_cast<Slot>(slot);
}

Node _parse_node(redisReply *reply) {
 if (reply == nullptr
     || !reply::is_array(*reply)
     || reply->element == nullptr
     || reply->elements < 2) {
  throw ProtoError("invalid node info");
 }

 auto host = reply::parse<std::string>(*(reply->element[0]));
 auto port = static_cast<int>(reply::parse<long long>(*(reply->element[1])));

 return {host, port};
}

std::pair<SlotRange, Node>
_parse_slot_info(redisReply &reply) {
 // Slot info is an array reply: min slot, max slot, master node, [slave nodes]
 if (reply.elements < 3 || reply.element == nullptr) {
  throw ProtoError("Invalid slot info");
 }

 auto min_slot = _parse_slot(reply.element[0]);

 auto max_slot = _parse_slot(reply.element[1]);

 if (min_slot > max_slot) {
  throw ProtoError("Invalid slot range");
 }
 auto slot_range = SlotRange{min_slot, max_slot};
 return std::make_pair(slot_range, _parse_node(reply.element[2]));
// switch (_role) {
//  case Role::MASTER:
//   // Return master node, i.e. `reply.element[2]`.
//   return std::make_pair(slot_range, _parse_node(reply.element[2]));
//
//  case Role::SLAVE: {
//   auto size = reply.elements;
//   if (size <= 3) {
//    throw Error("no slave node available");
//   }
//   static thread_local std::default_random_engine engine;
//
//   std::uniform_int_distribution<std::size_t> uniform_dist(3, size - 1);
//
//   auto i = uniform_dist(engine);
//   // Randomly pick a slave node.
//   auto *slave_node_reply = reply.element[i];
//
//   return std::make_pair(slot_range, _parse_node(slave_node_reply));
//  }

// default:
//  throw Error("unknown role");
//}

}

#endif //UNTITLED_MAIN_H
