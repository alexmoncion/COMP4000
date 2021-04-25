# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import account_pb2 as account__pb2


class ReplyStub(object):
    """The Account service definition
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Mount = channel.unary_unary(
                '/Reply/Mount',
                request_serializer=account__pb2.MountReq.SerializeToString,
                response_deserializer=account__pb2.MountRep.FromString,
                )


class ReplyServicer(object):
    """The Account service definition
    """

    def Mount(self, request, context):
        """Sends a confirmation
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ReplyServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Mount': grpc.unary_unary_rpc_method_handler(
                    servicer.Mount,
                    request_deserializer=account__pb2.MountReq.FromString,
                    response_serializer=account__pb2.MountRep.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Reply', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Reply(object):
    """The Account service definition
    """

    @staticmethod
    def Mount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Reply/Mount',
            account__pb2.MountReq.SerializeToString,
            account__pb2.MountRep.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
