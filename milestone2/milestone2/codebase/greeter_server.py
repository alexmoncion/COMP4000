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

# Connecting to DB
database = "accounts.db"
dbConnection = sqlite3.connect(database)
c = dbConnection.cursor()

# Creating Table (only if necessary)
c.execute('''CREATE TABLE if NOT EXISTS Accounts (username text, hash text, tokens text, expiry text)''')
dbConnection.commit()
dbConnection.close()

def hashCredentials(pword):
    hpass = bcrypt.hashpw(pword.encode("utf-8"), bcrypt.gensalt())
    return hpass

def checkForAccount(user):
    dbConnection = sqlite3.connect(database)
    c = dbConnection.cursor()
    c.execute("SELECT * FROM Accounts WHERE username = '%s'" % user)
    if (c.fetchone() == None):
        dbConnection.close()
        return True
    dbConnection.close()
    return False

def handleLogin(user, pword):
    if(checkForAccount(user)):
        return ("Authentication failure, username does not exist.")
    dbConnection = sqlite3.connect(database)
    c = dbConnection.cursor()
    c.execute("SELECT hash FROM Accounts WHERE username = '%s'" % user)
    dbhash = c.fetchone()[0]
    try:
        dbhash = dbhash.encode("utf-8")
    except (AttributeError):
        pass
    if (bcrypt.hashpw(pword.encode("utf-8"), dbhash) == dbhash):
        base64Arr = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','+','/']
        token = ""
        for x in range(64):
            token += base64Arr[random.randint(0,63)]
        print("Password matches, Your Authentication token is: " + token)
        storeToken(user, token)
        dateNow = time.time()
        expiry = dateNow + 3600
        storeExpiry(token, expiry)
        return token
    else:
        pwordinvalid = "Password does not match."
        print(pwordinvalid)
        return pwordinvalid

def handleDelete(user, pword, authentication):
    returnMessage = ""
    if(checkForAccount(user)):
        print("Authentication failure, username does not exist.")
        returnMessage = "Authentication failure, username does not exist."
        return (False, returnMessage)
    dbConnection = sqlite3.connect(database)
    c = dbConnection.cursor()
    c.execute("SELECT hash FROM Accounts WHERE username = '%s'" % user)
    dbhash = c.fetchone()[0]
    try:
        dbhash = dbhash.encode("utf-8")
    except (AttributeError):
        pass
    if (bcrypt.hashpw(pword.encode("utf-8"), dbhash) != dbhash):
        print("Incorrect Password")
        dbConnection.close()
        returnMessage = "Incorrect Password"
        return (False, returnMessage)
    c.execute("SELECT expiry FROM Accounts WHERE username = '%s'" % user)
    expiry = c.fetchone()[0]
    if (expiry == ""):
        print("User %s is not logged in!" % user)
        dbConnection.close()
        returnMessage = "Your are not logged in!"
        return (False, returnMessage)
    expiry = float(expiry)
    c.execute("SELECT tokens FROM Accounts WHERE username = '%s'" % user)
    token = c.fetchone()[0]
    if (token != authentication):
        print("Incorrect authentication token")
        c.close()
        dbConnection.close()
        returnMessage = "Incorrect authentication token"
        return (False, returnMessage)
    if (expiry <= (time.time() + 3600)):
        c.execute("DELETE FROM Accounts WHERE username = (?) ", (user,))
        print("User %s was Successfully removed" % user)
        dbConnection.commit()
        c.close()
        dbConnection.close()
        returnMessage = "User was successfully removed!"
        return (True, returnMessage)
    else:
        print("Token expiried. Please login again.")
        c.close()
        dbConnection.close()
        returnMessage = "Token expiried. Please login again."
        return (False, returnMessage)

def handleUpdate(user, pword, newpword, authentication):
    errorMessage = ""
    if(checkForAccount(user)):
        print("Authentication failure, username does not exist.")
        errorMessage = "Authentication failure, username does not exist."
        return (False, errorMessage)
    dbConnection = sqlite3.connect(database)
    c = dbConnection.cursor()
    c.execute("SELECT hash FROM Accounts WHERE username = '%s'" % user)
    dbhash = c.fetchone()[0]
    try:
        dbhash = dbhash.encode("utf-8")
    except (AttributeError):
        pass
    if (bcrypt.hashpw(pword.encode("utf-8"), dbhash) != dbhash):
        print("Incorrect Password")
        dbConnection.close()
        errorMessage = "Incorrect Password"
        return (False, errorMessage)
    c.execute("SELECT expiry FROM Accounts WHERE username = '%s'" % user)
    expiry = c.fetchone()[0]
    if (expiry == ""):
        print("User %s is not logged in!" % user)
        dbConnection.close()
        errorMessage = "You are not logged in!"
        return (False, errorMessage)
    expiry = float(expiry)
    c.execute("SELECT tokens FROM Accounts WHERE username = '%s'" % user)
    token = c.fetchone()[0]
    if (token != authentication):
        print("Incorrect authentication token")
        c.close()
        dbConnection.close()
        errorMessage = "Incorrect authentication token"
        return (False, errorMessage)
    if (expiry <= (time.time() + 3600)):
        newHash = hashCredentials(newpword)
        values = (newHash, user)
        c.execute("UPDATE Accounts SET hash = (?) WHERE username = (?)", values)
        print("User %s password was successfully updated" % user)
        dbConnection.commit()
        c.close()
        dbConnection.close()
        errorMessage = "Users password was successfully updated!"
        return (True, errorMessage)
    else:
        print("Token expiried. Please login again.")
        c.close()
        dbConnection.close()
        errorMessage = "Token expiried. Please login again."
        return (False, errorMessage)

def storeToken(user, token):
    dbConnection = sqlite3.connect(database)
    c = dbConnection.cursor()
    values = (token, user)
    c.execute("UPDATE Accounts SET tokens = (?) WHERE username = (?) ", values)
    dbConnection.commit()
    dbConnection.close()

def storeExpiry(token, expiry):
    dbConnection = sqlite3.connect(database)
    c = dbConnection.cursor()
    values = (expiry, token)
    c.execute("UPDATE Accounts SET expiry = (?) WHERE tokens = (?) ", values)
    dbConnection.commit()
    dbConnection.close()

def storeCredentials(user, phash, token, expiry):
    token = ""
    expiry = ""
    dbConnection = sqlite3.connect(database)
    c = dbConnection.cursor()
    c.execute("INSERT INTO Accounts VALUES ('" + user + "', '" + phash.decode('utf8') + "', '" + token + "', '" + expiry + "')")
    dbConnection.commit()
    dbConnection.close()

class Reply(account_pb2_grpc.ReplyServicer):

    def Creation(self, request, context):
        print("Credentials Received.")
        name = request.name
        phash = hashCredentials(request.password)
        print("Password Hash: %s" % phash)
        if checkForAccount(name):
            token = ""
            expiry = ""
            storeCredentials(name, phash, token, expiry)
            return account_pb2.CreationReply(message='Hello again, %s! The server has received your credentials.' % name)
        else:
            return account_pb2.CreationReply(message='Sorry, that name is unavailable.')

    def Login(self, request, context):
        authToken = handleLogin(request.name, request.password)
        if(authToken == "Password does not match."):
            return (account_pb2.LoginReply(message='Authentication failure, %s' % authToken, token=None))
        else:
            return (account_pb2.LoginReply(message='Login is Successful! Your authentication token is: %s.' % authToken, token=authToken))

    def Delete(self, request, context):
        isDeleted = handleDelete(request.name, request.password, request.authentication)
        if (isDeleted[0]):
            return (account_pb2.LoginReply(message='Deletion Successful! %s' % isDeleted[1]))
        return (account_pb2.LoginReply(message='Deletion Unsuccessful. %s' % isDeleted[1]))

    def Update(self, request, context):
        isUpdated = handleUpdate(request.name, request.password, request.newPassword, request.authentication)
        if (isUpdated[0]):
            return (account_pb2.LoginReply(message='Password Update Successful! %s' % isUpdated[1]))
        return (account_pb2.LoginReply(message='Password Update Unsuccessful. %s' % isUpdated[1]))

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
