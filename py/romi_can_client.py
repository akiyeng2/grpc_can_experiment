
from __future__ import print_function

import logging
import random

import grpc
import romi_can_pb2
import romi_can_pb2_grpc




def run():
    channel = grpc.insecure_channel("localhost:50051")
    req = romi_can_pb2.SetRequest(id=1, value=0.5, mode=romi_can_pb2.TalonSRXControlMode.PercentOutput)
    stub=romi_can_pb2_grpc.GRPCTalonSRXStub(channel)

    print(stub.SetTalon(req))


if __name__ == '__main__':
    logging.basicConfig()
    run()