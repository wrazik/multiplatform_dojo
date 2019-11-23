cmake_minimum_required(VERSION 3.6)
project(cpp_tank_client)

set(CMAKE_CXX_STANDARD 17)

add_executable(cpp_tank_client
  main.cpp)
target_link_libraries(cpp_tank_client PUBLIC
  zmq
  zmqpp
  pthread)

