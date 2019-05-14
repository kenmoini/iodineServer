#!/usr/bin/env python3
from array import *
from subprocess import call
import os
import xalglib
from xmlrpclib import ServerProxy, Error

# AlgLib Module Test
os.system('python3 ./cpython/check.py')

s = ServerProxy('http://localhost:2082/iodineRPC2')

print(str('Iodine Server Host Uptime: ') + str(s.uptime()) + ' Hrs')
