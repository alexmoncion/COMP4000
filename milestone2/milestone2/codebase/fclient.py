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

class Syscalls:
    def __init__(self,ls,opendir,getattr,stat,mkdir,fullPath,access,chmod,chown,readdir,readlink,mknod,rmdir,statfs,unlink,symlink,rename,link,utimens,open,create,read,write,truncate,flush,release,fsync):
        self.ls=ls
        self.opendir=opendir
        self.getattr=getattr
        self.stat=stat
        self.mkdir=mkdir
        self.fullPath=fullPath
        self.access=access
        self.chmod=chmod
        self.chown=chown
        self.readdir=readdir
        self.readlink=readlink
        self.mknod=mknod
        self.rmdir=rmdir
        self.statfs=statfs
        self.unlink=unlink
        self.symlink=symlink
        self.rename=rename
        self.link=link
        self.utimens=utimens
        self.open=open
        self.create=create
        self.read=read
        self.write=write
        self.truncate=truncate
        self.flush=flush
        self.release=release
        self.fsync=fsync

def getSysCallOptions():
    print("======= Available System Calls =======")
    print("Menu Options:")
    print("Type (ls) to list all directories.")
    print("Type (opendir) to open and read a directory.")
    print("Type (getattr) to retrieve the attribute of a specific object.")
    print("Type (stat) to return information about a file.")
    print("Type (mkdir) to make a new directory.")
    print("fullPath")
    print("access")
    print("chmod")
    print("chown")
    print("readdir")
    print("readlink")
    print("mknod")
    print("rmdir")
    print("statfs")
    print("Type (unlink) to delete a specific file.")
    print("symlink")
    print("rename")
    print("link")
    print("utimens")
    print("Type (open) to open a specific file.")
    print("Type (create) to create a new file.")
    print("Type (read) to read a specific file.")
    print("Type (write) to write into a specific file.")
    print("truncate")
    print("flush")
    print("release")
    print("fsync")
    print("Type (exit) to exit.")
    clientSysCallReq = input("Enter any of the above menu options to continue | Enter (exit) to exit: ")
    return(clientSysCallReq)

def handleFilesystemRequest():
    dir = getDirectory()
    directory = Filesystem(dir)
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.ReplyStub(channel)
    response = stub.MountFs(account_pb2.FilesystemRequest(fsPath=directory.fsPath))
    print("Client received: " + response.message)

def lsReq():
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.ReplyStub(channel)
    response = stub.ls(account_pb2.ClientSysCallRequest())
    print("Client received: " + response.message)

def opendirReq():
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.ReplyStub(channel)
    response = stub.opendir(account_pb2.ClientSysCallRequest())
    print("Client received: " + response.message)

def getattrReq():
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.ReplyStub(channel)
    response = stub.getattr(account_pb2.ClientSysCallRequest())
    print("Client received: " + response.message)

def statReq():
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.ReplyStub(channel)
    response = stub.stat(account_pb2.ClientSysCallRequest())
    print("Client received: " + response.message)

def mkdirReq():
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.ReplyStub(channel)
    response = stub.mkdir(account_pb2.ClientSysCallRequest())
    print("Client received: " + response.message)

def fullPathReq():
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.ReplyStub(channel)
    response = stub.fullPath(account_pb2.FullPathReq(partial="/test/"))
    print("Client received: " + response.path)

def accessReq():
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.ReplyStub(channel)
    response = stub.access(account_pb2.ClientSysCallRequest())
    print("Client received: " + response.message)

def chmodReq():
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.ReplyStub(channel)
    response = stub.chmod(account_pb2.ClientSysCallRequest())
    print("Client received: " + response.message)

def chownReq():
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.ReplyStub(channel)
    response = stub.chown(account_pb2.ClientSysCallRequest())
    print("Client received: " + response.message)

def readdirReq():
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.ReplyStub(channel)
    response = stub.readdir(account_pb2.ClientSysCallRequest())
    print("Client received: " + response.message)

def readlinkReq(self, path):
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.ReplyStub(channel)
    response = stub.readlink(account_pb2.ClientSysCallRequest())
    print("Client received: " + response.message)

def mknodReq():
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.ReplyStub(channel)
    response = stub.mknod(account_pb2.ClientSysCallRequest())
    print("Client received: " + response.message)

def rmdirReq():
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.ReplyStub(channel)
    response = stub.rmdir(account_pb2.ClientSysCallRequest())
    print("Client received: " + response.message)

def statfsReq():
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.ReplyStub(channel)
    response = stub.statfs(account_pb2.ClientSysCallRequest())
    print("Client received: " + response.message)

def unlinkReq():
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.ReplyStub(channel)
    response = stub.unlink(account_pb2.ClientSysCallRequest())
    print("Client received: " + response.message)

def symlinkReq():
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.ReplyStub(channel)
    response = stub.symlink(account_pb2.ClientSysCallRequest())
    print("Client received: " + response.message)

def renameReq():
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.ReplyStub(channel)
    response = stub.rename(account_pb2.ClientSysCallRequest())
    print("Client received: " + response.message)

def linkReq():
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.ReplyStub(channel)
    response = stub.link(account_pb2.ClientSysCallRequest())
    print("Client received: " + response.message)

def utimensReq():
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.ReplyStub(channel)
    response = stub.utimens(account_pb2.ClientSysCallRequest())
    print("Client received: " + response.message)

# File methods
# ============

def openReq():
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.ReplyStub(channel)
    response = stub.open(account_pb2.ClientSysCallRequest())
    print("Client received: " + response.message)

def createReq():
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.ReplyStub(channel)
    response = stub.create(account_pb2.ClientSysCallRequest())
    print("Client received: " + response.message)

def readReq():
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.ReplyStub(channel)
    response = stub.read(account_pb2.ClientSysCallRequest())
    print("Client received: " + response.message)

def writeReq():
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.ReplyStub(channel)
    response = stub.write(account_pb2.ClientSysCallRequest())
    print("Client received: " + response.message)

def truncateReq():
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.ReplyStub(channel)
    response = stub.truncate(account_pb2.ClientSysCallRequest())
    print("Client received: " + response.message)

def flushReq():
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.ReplyStub(channel)
    response = stub.flush(account_pb2.ClientSysCallRequest())
    print("Client received: " + response.message)

def releaseReq():
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.ReplyStub(channel)
    response = stub.release(account_pb2.ClientSysCallRequest())
    print("Client received: " + response.message)

def fsyncReq():
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.ReplyStub(channel)
    response = stub.fsync(account_pb2.ClientSysCallRequest())
    print("Client received: " + response.message)

def run(): #directory
	sysCallOptions = getSysCallOptions()
	if sysCallOptions == "ls":
	    print("Sending ls request to the server.")
	    lsReq()
	elif sysCallOptions == "opendir":
	    print("Sending an opendir request to the server.")
	    opendirReq()
	elif sysCallOptions == "getattr":
	    print("Sending a getattr request to the server.")
	    getattrReq()
	elif sysCallOptions == "stat":
	    print("Sending a stat request to the server.")
	    statReq()
	elif sysCallOptions == "mkdir":
	    print("Sending a mkdir request to the server.")
	    mkdirReq()
	elif sysCallOptions == "fullPath":
	    print("Sending an fullPath request to the server.")
	    fullPathReq()
	elif sysCallOptions == "access":
	    print("Sending an access request to the server.")
	    accessReq()
	elif sysCallOptions == "chmod":
	    print("Sending a chmod request to the server.")
	    chmodReq()
	elif sysCallOptions == "chown":
	    print("Sending a chown request to the server.")
	    chownReq()
	elif sysCallOptions == "readdir":
	    print("Sending a readdir request to the server.")
	    readdirReq()
	elif sysCallOptions == "readlink":
	    print("Sending a readlink request to the server.")
	    readlinkReq()
	elif sysCallOptions == "mknod":
	    print("Sending an mknod request to the server.")
	    mknodReq()
	elif sysCallOptions == "rmdir":
	    print("Sending an rmdir request to the server.")
	    rmdirReq()
	elif sysCallOptions == "statfs":
	    print("Sending a statfs request to the server.")
	    statfsReq()
	elif sysCallOptions == "unlink":
	    print("Sending an unlink request to the server.")
	    unlinkReq()
	elif sysCallOptions == "symlink":
	    print("Sending a symlink request to the server.")
	    symlinkReq()
	elif sysCallOptions == "rename":
	    print("Sending a rename request to the server.")
	    renameReq()
	elif sysCallOptions == "link":
	    print("Sending an link request to the server.")
	    linkReq()
	elif sysCallOptions == "utimens":
	    print("Sending a utimens request to the server.")
	    utimensReq()
	elif sysCallOptions == "open":
	    print("Sending an open request to the server.")
	    openReq()
	elif sysCallOptions == "create":
	    print("Sending a create request to the server.")
	    createReq()
	elif sysCallOptions == "read":
	    print("Sending a read request to the server.")
	    readReq()
	elif sysCallOptions == "write":
	    print("Sending a write request to the server.")
	    writeReq()
	elif sysCallOptions == "truncate":
	    print("Sending an truncate request to the server.")
	    truncateReq()
	elif sysCallOptions == "flush":
	    print("Sending a flush request to the server.")
	    flushReq()
	elif sysCallOptions == "release":
	    print("Sending a release request to the server.")
	    releaseReq()
	elif sysCallOptions == "fsync":
	    print("Sending an fsync request to the server.")
	    fsyncReq()
	elif sysCallOptions == "exit":
	    print("See you later.")
	else:
	    print("Read the instructions.")

if __name__ == '__main__':
    logging.basicConfig()
    run() #sys.argv[1]
