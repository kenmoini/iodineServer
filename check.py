#!/usr/bin/env python3
from array import *
from subprocess import call
import os
import xalglib
import xmlrpc.client

# AlgLib Module Test
os.system('python3 ./cpython/check.py')

s = xmlrpc.client.ServerProxy('http://localhost:2082/iodineRPC2')

print(str('Iodine Server Host Uptime: ') + str(s.uptime()) + ' Hrs')
