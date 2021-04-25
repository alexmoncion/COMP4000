# !/usr/bin/python

from __future__ import print_function

import myfuse
import os, sys

p = ("/home/student/Documents/test/test.txt")

print("os.access(\"" + p + "\", " + str(4) + ")")

exec("reply = os.access(\"" + p + "\", " + str(4) + ")")

print(reply)
