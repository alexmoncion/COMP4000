from concurrent import futures
import logging

import grpc

import account_pb2
import account_pb2_grpc

class Reply(account_pb2_grpc.ReplyServicer):

    def Mount(self, request, context):
        return (account_pb2.MountRep(msg="Message sent successfully"))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    account_pb2_grpc.add_ReplyServicer_to_server(Reply(), server)
    server.add_insecure_port('[::]:10001')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
