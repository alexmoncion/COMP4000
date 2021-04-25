# Copyright 2015 gRPC authors.
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
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging

import grpc

import os
import sys
import errno

import account_pb2
import account_pb2_grpc


class Greeter(account_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        print("path received")
        formatPath = request.name.replace(' ', '\ ')
        reply = os.popen("tree %s" % formatPath).read()
        return account_pb2.HelloReply(message='Here are the files.\n %s' % reply)

    def RunTerminalCommand(self, request, context):
        print(request.name + " command received")
        print(type(request.name))
        reply = exec(request.name)
        print(reply)
        return account_pb2.HelloReply(message=reply)

    def RunTerminalCommand2(self, request, context):
        print(request.name + " command received")
        print(type(request.name))
        reply = exec(request.name)
        print(reply)
        return account_pb2.HelloReply(message2=reply)

    def RunTerminalCommand3(self, request, context):
        fh = request.fh
        offset = request.offset
        length = request.length
        print(request.name + " command received")
        print(type(request.name))
        exec(os.lseek(fh, offset, os.SEEK_SET))
        reply = exec(os.read(fh, length))
        print(reply)
        return account_pb2.HelloReply(message2=reply)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    account_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
