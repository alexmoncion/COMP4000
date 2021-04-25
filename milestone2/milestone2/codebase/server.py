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

import bcrypt
import sqlite3
import random
import time

class Reply(account_pb2_grpc.ReplyServicer):

    #This function might need to be modified to work with the removal of the "directory" arg from the handleFilesystemRequest() and run() commands
    #Currently when prompted by the server to provide a path, after you do it hangs and terminates the client session
    def MountFs(self, request, context):
        print("Path recieved")
        mountpoint = "/home/student/Downloads/fuse/"
        myfuse.main(str(request.fsPath), mountpoint)
        return account_pb2.FilesystemReply(message='Filesystem has been mounted using: %s!.' % request.fsPath)

    def ls(self, request, context):
        print("ls Request recieved")
        return account_pb2.ClientSysCallReply(message='ls request is being processed. %s' % request.ls)

    def opendir(self, request, context):
        print("opendir Request recieved")
        return account_pb2.ClientSysCallReply(message='opendir request is being processed. %s' % request.opendir)

    def getattr(self, request, context):
        print("getattr Request recieved")
        return account_pb2.ClientSysCallReply(message='getattr request is being processed. %s' % request.getattr)

    def stat(self, request, context):
        print("stat Request recieved")
        return account_pb2.ClientSysCallReply(message='stat request is being processed. %s' % request.stat)

    def mkdir(self, request, context):
        print("mkdir Request recieved")
        return account_pb2.ClientSysCallReply(message='mkdir request is being processed. %s' % request.mkdir)

    def fullPath(self, request, context):
        print("fullPath Request recieved")
        return account_pb2.ClientSysCallReply(message='fullPath request is being processed. %s' % request.fullPath)

    def access(self, request, context):
        print("access Request recieved")
        return account_pb2.ClientSysCallReply(message='access request is being processed. %s' % request.access)

    def chmod(self, request, context):
        print("chmod Request recieved")
        return account_pb2.ClientSysCallReply(message='chmod request is being processed. %s' % request.chmod)

    def chown(self, request, context):
        print("chown Request recieved")
        return account_pb2.ClientSysCallReply(message='chown request is being processed. %s' % request.chown)

    def readdir(self, request, context):
        print("readdir Request recieved")
        return account_pb2.ClientSysCallReply(message='readdir request is being processed. %s' % request.readdir)

    def readlink(self, request, context):
        print("readlink Request recieved")
        return account_pb2.ClientSysCallReply(message='readlink request is being processed. %s' % request.readlink)

    def mknod(self, request, context):
        print("mknod Request recieved")
        return account_pb2.ClientSysCallReply(message='mknod request is being processed. %s' % request.mknod)

    def rmdir(self, request, context):
        print("rmdir Request recieved")
        return account_pb2.ClientSysCallReply(message='rmdir request is being processed. %s' % request.rmdir)

    def statfs(self, request, context):
        print("statfs Request recieved")
        return account_pb2.ClientSysCallReply(message='statfs request is being processed. %s' % request.statfs)

    def unlink(self, request, context):
        print("unlink Request recieved")
        return account_pb2.ClientSysCallReply(message='unlink request is being processed. %s' % request.unlink)

    def symlink(self, request, context):
        print("symlink Request recieved")
        return account_pb2.ClientSysCallReply(message='symlink request is being processed. %s' % request.symlink)

    def rename(self, request, context):
        print("rename Request recieved")
        return account_pb2.ClientSysCallReply(message='rename request is being processed. %s' % request.rename)

    def link(self, request, context):
        print("link Request recieved")
        return account_pb2.ClientSysCallReply(message='link request is being processed. %s' % request.link)

    def utimens(self, request, context):
        print("utimens Request recieved")
        return account_pb2.ClientSysCallReply(message='utimens request is being processed. %s' % request.utimens)

    def open(self, request, context):
        print("open Request recieved")
        return account_pb2.ClientSysCallReply(message='open request is being processed. %s' % request.open)

    def create(self, request, context):
        print("create Request recieved")
        return account_pb2.ClientSysCallReply(message='create request is being processed. %s' % request.create)

    def read(self, request, context):
        print("read Request recieved")
        return account_pb2.ClientSysCallReply(message='read request is being processed. %s' % request.read)

    def write(self, request, context):
        print("write Request recieved")
        return account_pb2.ClientSysCallReply(message='write request is being processed. %s' % request.write)

    def truncate(self, request, context):
        print("truncate Request recieved")
        return account_pb2.ClientSysCallReply(message='truncate request is being processed. %s' % request.truncate)

    def flush(self, request, context):
        print("flush Request recieved")
        return account_pb2.ClientSysCallReply(message='flush request is being processed. %s' % request.flush)

    def release(self, request, context):
        print("release Request recieved")
        return account_pb2.ClientSysCallReply(message='release request is being processed. %s' % request.release)

    def fsync(self, request, context):
        print("fsync Request recieved")
        return account_pb2.ClientSysCallReply(message='fsync request is being processed. %s' % request.fsync)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    account_pb2_grpc.add_ReplyServicer_to_server(Reply(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
