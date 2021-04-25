from __future__ import print_function

import myfuse
import os

p = myfuse.Passthrough("/home/student/Documents/test/")

print(p._full_path('/admin/'))

print(type(p.access('/admin/admin.txt', os.O_WRONLY)))
