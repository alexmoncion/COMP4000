from concurrent import futures
import logging

import grpc

import account_pb2
import account_pb2_grpc

import bcrypt
import sqlite3
import random
import time

# Connecting to DB
database = "accounts.db"
dbConnection = sqlite3.connect(database)
c = dbConnection.cursor()

# Creating Table (only if necessary)
c.execute('''CREATE TABLE if NOT EXISTS Accounts (username text, hash text, tokens text, expiry text, admin text)''')
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

def isAdmin(user):
    if(checkForAccount(user)):
        return ("Authentication failure, username does not exist.")
    dbConnection = sqlite3.connect(database)
    c = dbConnection.cursor()
    c.execute("SELECT admin FROM Accounts WHERE username = '%s'" % user)
    isAdmin = c.fetchone()[0]
    dbConnection.close()
    return isAdmin

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

def storeCredentials(user, phash, token, expiry, admin):
    token = ""
    expiry = ""
    dbConnection = sqlite3.connect(database)
    c = dbConnection.cursor()
    c.execute("INSERT INTO Accounts VALUES ('" + user + "', '" + phash.decode('utf8') + "', '" + token + "', '" + expiry + "', '" + admin + "')")
    dbConnection.commit()
    dbConnection.close()

class Reply(account_pb2_grpc.ReplyServicer):

    def Creation(self, request, context):
        print("Credentials Received.")
        name = request.name
        phash = hashCredentials(request.password)
        admin = request.admin
        print("Password Hash: %s" % phash)
        if checkForAccount(name):
            token = ""
            expiry = ""
            storeCredentials(name, phash, token, expiry, admin)
            return account_pb2.CreationReply(message='Hello again, %s! The server has received your credentials.' % name)
        else:
            return account_pb2.CreationReply(message='Sorry, that name is unavailable.')

    def Login(self, request, context):
        authToken = handleLogin(request.name, request.password)
        if(authToken == "Password does not match."):
            return (account_pb2.LoginReply(message='Authentication failure, %s' % authToken, token=None, isAdmin="False"))
        else:
            adminCheck = isAdmin(request.name)
            return (account_pb2.LoginReply(message='Login is Successful! Your authentication token is: %s.' % authToken, token=authToken, isAdmin=adminCheck))

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


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    account_pb2_grpc.add_ReplyServicer_to_server(Reply(), server)
    server.add_insecure_port('[::]:10001')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
