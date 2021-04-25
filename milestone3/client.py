from __future__ import with_statement

import os
import sys
import errno
import cmd

from fuse import FUSE, FuseOSError, Operations
import logging

import grpc
import myfuse

import account_pb2
import account_pb2_grpc

ip = '192.168.46.27:10001' #sams ip 192.168.46.27:10001 #localhost is [::]:50051

class Passthrough(Operations):
    def __init__(self, root):
        self.root = root

    # Helpers
    # =======

    def _full_path(self, partial):
        partial = partial.lstrip("/")
        path = os.path.join(self.root, partial)
        return path

    # Filesystem methods
    # ==================

    def access(self, path, mode):
        full_path = self._full_path(path)
        channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
        stub = account_pb2_grpc.GreeterStub(channel)
        request = "os.access('" + full_path + "', " + str(mode) + ")"
        response = stub.RunTerminalCommand(account_pb2.HelloRequest(name=request))
        if not (response.message == "True"):
            raise FuseOSError(errno.EACCES)

    def chmod(self, path, mode):
        full_path = self._full_path(path)
        return os.chmod(full_path, mode)

    def chown(self, path, uid, gid):
        full_path = self._full_path(path)
        return os.chown(full_path, uid, gid)

    def readdir(self, path, fh):
        full_path = self._full_path(path)

        dirents = ['.', '..']
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))
        for r in dirents:
            yield r

    def readlink(self, path):
        pathname = os.readlink(self._full_path(path))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    def mknod(self, path, mode, dev):
        return os.mknod(self._full_path(path), mode, dev)

    def rmdir(self, path):
        full_path = self._full_path(path)
        channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
        stub = account_pb2_grpc.GreeterStub(channel)
        request = "os.rmdir('" + full_path + "')"
        response = stub.RunTerminalCommand(account_pb2.HelloRequest(name=request))
        return response.message

    def mkdir(self, path, mode):
        full_path = self._full_path(path)
        channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
        stub = account_pb2_grpc.GreeterStub(channel)
        request = "os.mkdir('" + full_path + "', " + str(mode) + ")"
        response = stub.RunTerminalCommand(account_pb2.HelloRequest(name=request))
        return response.message

    def statfs(self, path):
        full_path = self._full_path(path)
        stv = os.statvfs(full_path)
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))

    def unlink(self, path):
        channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
        stub = account_pb2_grpc.GreeterStub(channel)
        full_path = self._full_path(path)
        request = "os.unlink('" + full_path + "')"
        response = stub.RunTerminalCommand(account_pb2.HelloRequest(name=request))
        return response.message

    def symlink(self, name, target):
        channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
        stub = account_pb2_grpc.GreeterStub(channel)
        full_path = self._full_path(name)
        request = "os.symlink('" + target + "', " + full_path + ")"
        response = stub.RunTerminalCommand(account_pb2.HelloRequest(name=request))
        return response.message

    def rename(self, old, new):
        return os.rename(self._full_path(old), self._full_path(new))

    def link(self, target, name):
        return os.link(self._full_path(target), self._full_path(name))

    def utimens(self, path, times=None):
        return os.utime(self._full_path(path), times)

    # File methods
    # ============

    def open(self, path, flags):
        full_path = self._full_path(path)
        channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
        stub = account_pb2_grpc.GreeterStub(channel)
        fl = str(flags)
        print(fl)
        request = ("os.open('" + full_path + "', " + str(fl) +")")
        print(request)
        response = stub.RunTerminalCommand(account_pb2.HelloRequest(name=request))
        return int(response.message)

    def create(self, path, mode, fi=None):
        full_path = self._full_path(path)
        channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
        stub = account_pb2_grpc.GreeterStub(channel)
        arguments = int(mode)
        request = ("os.open('" + full_path + "', os.O_WRONLY | os.O_CREAT, %d)" % arguments)
        response = stub.RunTerminalCommand(account_pb2.HelloRequest(name=request))
        return response.message

    def read(self, path, length, offset, fh):
        channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
        stub = account_pb2_grpc.GreeterStub(channel)
        request = (fh, offset, length)
        response = stub.RunTerminalCommand(account_pb2.HelloRequest(fh=request[0], offset=request[1], length=request[2]))
        return response.message

    def write(self, path, buf, offset, fh):
        channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
        stub = account_pb2_grpc.GreeterStub(channel)
        request = "myfuse.write('" + path + "', " + str(buf) + ", " + str(offset) + ", " + str(fh) + ")"
        response = stub.RunTerminalCommand(account_pb2.HelloRequest(request))

    def truncate(self, path, length, fh=None):
        full_path = self._full_path(path)
        with open(full_path, 'r+') as f:
            f.truncate(length)

    def flush(self, path, fh):
        channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
        stub = account_pb2_grpc.GreeterStub(channel)
        request = "os.fsync(" + str(fh) + ")"
        response = stub.RunTerminalCommand2(account_pb2.HelloRequest(name=request))
        return response.message2

    def release(self, path, fh):
        channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
        stub = account_pb2_grpc.GreeterStub(channel)
        request = "os.close(" + str(fh) + ")"
        response = stub.RunTerminalCommand2(account_pb2.HelloRequest(name=request))
        return response.message2

    def fsync(self, path, fdatasync, fh):
        return self.flush(path, fh)
        channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
        stub = account_pb2_grpc.GreeterStub(channel)
        request = "os.flush(" + path + ", " + str(fh) + ")"
        response = stub.RunTerminalCommand2(account_pb2.HelloRequest(name=request))
        return response.message2



    def getattr(self, path, fh=None):
        full_path = self._full_path(path)
        st = os.lstat(full_path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                     'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid',
                     'st_dev', 'st_ino', 'st_mode'))

    def stat(self, path):
        full_path = self._full_path(path)
        stv = os.stat(full_path)
        return dict((key, getattr(stv, key)) for key in ('st_atime', 'st_ctime',
                     'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid',
                     'st_dev', 'st_ino', 'st_mode', 'st_blocks', 'st_rdev', 'st_flags'))

    def opendir(self, path):
        full_path = self._full_path(path)
        return os.open(full_path, os.O_RDONLY)

def run(path):
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello(account_pb2.HelloRequest(name=path))
    print("Greeter client received: " + response.message)
    mountpoint = "/home/student/Documents/fuse/"
    formatPath = path.replace(' ', '\ ')
    FUSE(Passthrough(path), mountpoint, nothreads=True, foreground=True)


if __name__ == '__main__':
    logging.basicConfig()
    run(sys.argv[1])
