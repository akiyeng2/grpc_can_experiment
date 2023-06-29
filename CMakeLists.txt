# Copyright 2018 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# cmake build file for C++ helloworld example.
# Assumes protobuf and gRPC have been installed using cmake.
# See cmake_externalproject/CMakeLists.txt for all-in-one cmake build
# that automatically builds all the dependencies before building helloworld.

cmake_minimum_required(VERSION 3.5.1)

project(RomiCan C CXX)
add_definitions(-std=c++20)



option(protobuf_MODULE_COMPATIBLE TRUE)
find_package(Protobuf CONFIG REQUIRED)
message(STATUS "Using protobuf ${Protobuf_VERSION}")


set(_PROTOBUF_LIBPROTOBUF protobuf::libprotobuf)
set(_REFLECTION gRPC::grpc++_reflection)
if(CMAKE_CROSSCOMPILING)
  find_program(_PROTOBUF_PROTOC protoc)
else()
  set(_PROTOBUF_PROTOC $<TARGET_FILE:protobuf::protoc>)
endif()

# Find gRPC installation
# Looks for gRPCConfig.cmake file installed by gRPC's cmake installation.
find_package(gRPC CONFIG REQUIRED)
message(STATUS "Using gRPC ${gRPC_VERSION}")

set(_GRPC_GRPCPP gRPC::grpc++)
if(CMAKE_CROSSCOMPILING)
  find_program(_GRPC_CPP_PLUGIN_EXECUTABLE grpc_cpp_plugin)
else()
  set(_GRPC_CPP_PLUGIN_EXECUTABLE $<TARGET_FILE:gRPC::grpc_cpp_plugin>)
endif()

# Proto file
get_filename_component(romi_can_proto "romi_can.proto" ABSOLUTE)
get_filename_component(romi_can_proto_path "${romi_can_proto}" PATH)

# Phoenix part
set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package (Threads REQUIRED)

set(PHOENIX_SOURCE_DIR "${PROJECT_SOURCE_DIR}/Phoenix-Linux-SocketCAN-Example")
include_directories("${PHOENIX_SOURCE_DIR}/include")



if (${CMAKE_LIBRARY_ARCHITECTURE} STREQUAL "arm-linux-gnueabihf") # Jetson TK1 / Pi
    set(PHOENIX_LIBS_DIR ${PHOENIX_SOURCE_DIR}/lib/arm32)
elseif (${CMAKE_LIBRARY_ARCHITECTURE} STREQUAL "aarch64-linux-gnu") # Jetson TX2
    set(PHOENIX_LIBS_DIR ${PHOENIX_SOURCE_DIR}/lib/arm64)
else()
    set(PHOENIX_LIBS_DIR ${PHOENIX_SOURCE_DIR}/lib/x86-64)
endif()

set(CMAKE_INSTALL_RPATH "${PHOENIX_LIBS_DIR}")
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

# Generated sources
set(romi_can_proto_srcs "${CMAKE_CURRENT_BINARY_DIR}/romi_can.pb.cc")
set(romi_can_proto_hdrs "${CMAKE_CURRENT_BINARY_DIR}/romi_can.pb.h")
set(romi_can_grpc_srcs "${CMAKE_CURRENT_BINARY_DIR}/romi_can.grpc.pb.cc")
set(romi_can_grpc_hdrs "${CMAKE_CURRENT_BINARY_DIR}/romi_can.grpc.pb.h")
add_custom_command(
      OUTPUT "${romi_can_proto_srcs}" "${romi_can_proto_hdrs}" "${romi_can_grpc_srcs}" "${romi_can_grpc_hdrs}"
      COMMAND ${_PROTOBUF_PROTOC}
      ARGS --grpc_out "${CMAKE_CURRENT_BINARY_DIR}"
        --cpp_out "${CMAKE_CURRENT_BINARY_DIR}"
        -I "${romi_can_proto_path}"
        --plugin=protoc-gen-grpc="${_GRPC_CPP_PLUGIN_EXECUTABLE}"
        "${romi_can_proto}"
      DEPENDS "${romi_can_proto}")

# Include generated *.pb.h files
include_directories("${CMAKE_CURRENT_BINARY_DIR}")

# romi_can_grpc_proto
add_library(romi_can_grpc_proto
  ${romi_can_grpc_srcs}
  ${romi_can_grpc_hdrs}
  ${romi_can_proto_srcs}
  ${romi_can_proto_hdrs})
target_link_libraries(romi_can_grpc_proto
  ${_REFLECTION}
  ${_GRPC_GRPCPP}
  ${_PROTOBUF_LIBPROTOBUF})

message(PHOENIX_LIBS_DIR="${PHOENIX_LIBS_DIR}")
 
# Targets greeter_[async_](client|server)
foreach(_target
   romi_can_server )
  add_executable(${_target} "${_target}.cc")
  target_link_libraries(${_target}
    romi_can_grpc_proto
    ${_REFLECTION}
    ${_GRPC_GRPCPP}
    ${_PROTOBUF_LIBPROTOBUF}
    ${PHOENIX_LIBS_DIR}/libCTRE_Phoenix.so
    ${PHOENIX_LIBS_DIR}/libCTRE_PhoenixCCI.so
    ${PHOENIX_LIBS_DIR}/libCTRE_PhoenixTools.so
    Threads::Threads)
endforeach()
