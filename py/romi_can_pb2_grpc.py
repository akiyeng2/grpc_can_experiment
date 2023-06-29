# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import romi_can_pb2 as romi__can__pb2


class GRPCTalonSRXStub(object):
    """The greeting service definition.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SetTalon = channel.unary_unary(
                '/romi_can.GRPCTalonSRX/SetTalon',
                request_serializer=romi__can__pb2.SetRequest.SerializeToString,
                response_deserializer=romi__can__pb2.SetReply.FromString,
                )


class GRPCTalonSRXServicer(object):
    """The greeting service definition.
    """

    def SetTalon(self, request, context):
        """Sends a greeting
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_GRPCTalonSRXServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SetTalon': grpc.unary_unary_rpc_method_handler(
                    servicer.SetTalon,
                    request_deserializer=romi__can__pb2.SetRequest.FromString,
                    response_serializer=romi__can__pb2.SetReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'romi_can.GRPCTalonSRX', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class GRPCTalonSRX(object):
    """The greeting service definition.
    """

    @staticmethod
    def SetTalon(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/romi_can.GRPCTalonSRX/SetTalon',
            romi__can__pb2.SetRequest.SerializeToString,
            romi__can__pb2.SetReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)