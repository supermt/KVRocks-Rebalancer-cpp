cmake_minimum_required(VERSION 3.23)
project(kvrocks_balancer)


set(CMAKE_CXX_STANDARD 17)

add_executable(cluster-balance main.cpp)

find_library(HIREDIS_LIB hiredis)
target_link_libraries(cluster-balance ${HIREDIS_LIB})
find_library(REDIS_PLUS_PLUS_LIB redis++)
target_link_libraries(cluster-balance ${REDIS_PLUS_PLUS_LIB})

target_link_libraries(cluster-balance gflags)
