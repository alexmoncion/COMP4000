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

import os
import sys
import errno

import myfuse

import logging
import grpc
import account_pb2
import account_pb2_grpc

import os
import sys
import errno

class Greeter(account_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        print("Path recieved")
        mountpoint = "/home/student/Documents/fuse"
        myfuse.main(str(request), mountpoint)
        return account_pb2.FilesystemReply(message='Hello again, %s!.' % request.fsPath)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    account_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
