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
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function
import logging
import sys
import grpc

import account_pb2
import account_pb2_grpc

ip = '[::]:50051' #sams ip 192.168.46.27:10001

class Filesystem:
    def __init__(self,fsPath):
        self.fsPath=fsPath


def handleFilesystemRequest(directory):
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello(account_pb2.FilesystemRequest(fsPath=directory))
    print("Greeter client received: " + response.message)

def run(directory):
    handleFilesystemRequest(directory)


if __name__ == '__main__':
    logging.basicConfig()
    run(sys.argv[1])
