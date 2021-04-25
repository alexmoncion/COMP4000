from __future__ import print_function
import logging

import grpc

import account_pb2
import account_pb2_grpc

ip = '[::]:10001' #192.168.46.27:10001

class Credentials:
    def __init__(self,user,pword,admin="False"):
        self.user=user
        self.pword=pword
        self.admin=admin

class DeleteCredentials:
    def __init__(self,user,pword,authentication):
        self.user=user
        self.pword=pword
        self.authentication=authentication

class NewCredentials:
    def __init__(self,user,pword,newpword,authentication):
        self.user=user
        self.pword=pword
        self.newpword=newpword
        self.authentication=authentication

def getMenuOptions():
    print("=======COMP 4000 PROJECT | GROUP I =======")
    print("Menu Options:")
    print("Press (1) for Account Creation.")
    print("Press (2) for Account Login.")
    print("Press (3) for Account Deletion.")
    print("Press (4) for Account Password Update.")
    print("Press (5) to login to the Admin dashboard.")
    print("Press (0) to exit.")
    clientReq = input("Enter (1), (2), (3), or (4) to continue | Enter (0) to exit: ")
    return(clientReq)

def getCredentials():
    pword = 0
    pconfirm = 1
    adminpass = "gg"
    admin = "False"
    while (pword != pconfirm):
        user = input("Enter your username: ")
        pword = input("Enter your password: ")
        pconfirm = input("Confirm your password: ")
        if (pword == pconfirm):
            adminpass = input("Enter the password for admin creation: ")
            if(adminpass == "gg"):
                adminCheck = input("Type (YES) to give this account Admin privileges: ")
                if(adminCheck == "YES"):
                    admin = "True"
                    print("Password confirmed, sending credentials to server")
                    print("Admin user created.")
                else:
                    print("Password confirmed, sending credentials to server")
                    print("Basic user created.")
            else:
                print("Admin password is incorrect, Basic user created.")
        else:
            print("Password not confirmed, please re-enter password")
    return Credentials(user,pconfirm,admin)

def getLoginReq():
    user = input("Enter your username: ")
    pword = input("Enter your password: ")
    return Credentials(user,pword)

def getDeleteReq():
    user = input("Enter your username: ")
    pword = input("Enter your password: ")
    authentication = input("Enter your authentication token: ")
    return DeleteCredentials(user,pword,authentication)

def getUpdateReq():
    user = input("Enter your username: ")
    pword = input("Enter your password: ")
    newpword = input("Enter your new password: ")
    authentication = input("Enter your authentication token: ")
    return NewCredentials(user,pword,newpword,authentication)

def getAdminMenu(adminCreds):
    print("=======COMP 4000 PROJECT | GROUP I =======")
    print("Admin Menu Options:")
    print("Press (1) for Account Creation.")
    print("Press (2) for Account password update.")
    print("Press (3) for Account Deletion.")
    print("Press (0) to exit.")
    clientReq = input("Enter (1), (2), or (3) to continue | Enter (0) to exit: ")
    return(clientReq)

def handleCreationRequest():
    creds = getCredentials()
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.ReplyStub(channel)
    response = stub.Creation(account_pb2.CreationRequest(name=creds.user,password=creds.pword,admin=creds.admin))
    print("Client received: " + response.message)

def handleLoginRequest():
    loginReq = getLoginReq()
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.ReplyStub(channel)
    response = stub.Login(account_pb2.LoginRequest(name=loginReq.user,password=loginReq.pword, message="Login Attempt"))
    print("Client recieved: " + response.message)

def handleAdminLoginRequest():
    loginReq = getLoginReq()
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.ReplyStub(channel)
    response = stub.Login(account_pb2.LoginRequest(name=loginReq.user,password=loginReq.pword, message="Login Attempt"))
    print("Admin recieved: " + response.message)
    return response

def handleDeleteRequest():
    deleteReq = getDeleteReq()
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.ReplyStub(channel)
    response = stub.Delete(account_pb2.DeleteRequest(name=deleteReq.user,password=deleteReq.pword,authentication=deleteReq.authentication, message="Deletion Attempt"))
    print("Client recieved: " + response.message)

def handleUpdateRequest():
    updateReq = getUpdateReq()
    channel = grpc.insecure_channel(ip, options=(('grpc.enable_http_proxy', 0),))
    stub = account_pb2_grpc.ReplyStub(channel)
    response = stub.Update(account_pb2.UpdateRequest(name=updateReq.user,password=updateReq.pword,newPassword=updateReq.newpword,authentication=updateReq.authentication,message="Update Attempt"))
    print("Client recieved: " + response.message)

def run():
    menuOpt = getMenuOptions()
    if menuOpt == "1":
        handleCreationRequest()
    elif menuOpt == "2":
        handleLoginRequest()
    elif menuOpt == "3":
        handleDeleteRequest()
    elif menuOpt == "4":
        handleUpdateRequest()
    elif menuOpt == "5":
        adminCreds = handleAdminLoginRequest()
        if (adminCreds.isAdmin == "True"):
            adminOpt = getAdminMenu(adminCreds)
            if adminOpt == "1":
                handleCreationRequest() #WIP
            elif adminOpt == "2":
                handleUpdateRequest() #WIP
            elif adminOpt == "3":
                handleDeleteRequest() #WIP
    elif menuOpt == "0":
        print("See you later.")
    else:
        print("Read the instructions.")

if __name__ == '__main__':
    logging.basicConfig()
    run()
