from __future__ import print_function
import logging

import grpc

import account_pb2
import account_pb2_grpc

ip = '192.168.46.27:10001'

def handleMountRequest():
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.ReplyStub(channel)
    response = stub.Mount(account_pb2.MountReq(ip=ip,path='/fuse'))
    print("Client received: " + response.msg)

def run():
    handleMountRequest();

if __name__ == '__main__':
    logging.basicConfig()
    run()
