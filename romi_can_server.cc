/*
 *
 * Copyright 2015 gRPC authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */

#include <iostream>
#include <memory>
#include <string>

#include <grpcpp/ext/proto_server_reflection_plugin.h>
#include <grpcpp/grpcpp.h>
#include <grpcpp/health_check_service_interface.h>



#define Phoenix_No_WPI // remove WPI dependencies



#ifdef BAZEL_BUILD
#include "examples/protos/romi_can.grpc.pb.h"
#else
#include "romi_can.grpc.pb.h"
#endif

using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::Status;
using romi_can::GRPCTalonSRX;
using romi_can::SetRequest;
using romi_can::StatusReply;
using romi_can::CreateRequest;


#include "ctre/Phoenix.h"
#include "ctre/Phoenix.h"
#include "ctre/phoenix/platform/Platform.hpp"
#include "ctre/phoenix/unmanaged/Unmanaged.h"
#include "ctre/phoenix/cci/Unmanaged_CCI.h"
#include <memory>
using namespace ctre::phoenix;
using namespace ctre::phoenix::platform;
using namespace ctre::phoenix::motorcontrol;
using namespace ctre::phoenix::motorcontrol::can;

#include <map>

std::map <int, std::shared_ptr<ctre::phoenix::motorcontrol::can::TalonSRX>> talons;



/* make some talons for drive train */
std::string interface = "can0";
TalonSRX talLeft(1, interface); //Use the specified interface
TalonSRX talRight(0); //Use the default interface (can0)

// Logic and data behind the server's behavior.
class TalonServiceImpl final : public GRPCTalonSRX::Service {
  
  Status CreateTalon(ServerContext* context, const CreateRequest* request,
                  StatusReply* reply) override {
    int id = request->id();
    std::string response("Creating talon " + std::to_string(id));
    std::shared_ptr<TalonSRX> tal(new TalonSRX(id));
    talons[id] = tal;
    reply->set_status(response);
    return Status::OK;
  }

  Status SetTalon(ServerContext* context, const SetRequest* request,
                  StatusReply* reply) override {
    std::string response("Setting talon " + std::to_string(request->id()) + " to " + std::to_string(request->value()));
    reply->set_status(response);
    talons[request->id()]->Set(TalonSRXControlMode(static_cast<int>(request->mode())), request->value());
    return Status::OK;
  }
};

void RunServer() {


  std::string server_address("0.0.0.0:50051");
  TalonServiceImpl service;

  grpc::EnableDefaultHealthCheckService(true);
  grpc::reflection::InitProtoReflectionServerBuilderPlugin();
  ServerBuilder builder;
  // Listen on the given address without any authentication mechanism.
  builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
  // Register "service" as the instance through which we'll communicate with
  // clients. In this case it corresponds to an *synchronous* service.
  builder.RegisterService(&service);
  // Finally assemble the server.
  std::unique_ptr<Server> server(builder.BuildAndStart());
  std::cout << "Server listening on " << server_address << std::endl;

  // Wait for the server to shutdown. Note that some other thread must be
  // responsible for shutting down the server for this call to ever return.
  server->Wait();
}

int main(int argc, char** argv) {
  RunServer();

  return 0;
}
