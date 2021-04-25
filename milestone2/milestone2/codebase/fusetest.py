from __future__ import print_function

import passthrough

p = passthrough.Passthrough("/home/student/Documents/test/")

print(p._full_path('/admin/'))
