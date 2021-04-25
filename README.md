# COMP4000PROJ

## Required Packages
bcrypt : pip3 install bcrypt
random : pip3 install random

tree : sudo apt-get install tree

## Generate Proto file
python3 -m grpc_tools.protoc --proto_path=proto --python_out=. --grpc_python_out=. proto/account.proto

## Random Base64 Generation
import random

base64 = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','+','/']

token = ""
for (i = 0; i < 8; i++):
      token += base64[random.randint(0,64)]

## Adding Authorized User
User needs to be added to the SSL list, so that they are a trusted user. By default, that'll be no one?
Need to think of during development.
