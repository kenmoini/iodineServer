#!/usr/bin/env python3
from array import *
from subprocess import call
import os
import xalglib
from xmlrpclib import ServerProxy, Error
#from SimpleXMLRPCServer import SimpleXMLRPCServer
#from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
 
# AlgLib Module Test
print("\n//======================================================")
os.system('python3 ./cpython/check.py')
 
s = ServerProxy('http://localhost:2082/iodineRPC2')
 
print("\n//======================================================")
print(str('Iodine Server Host Uptime: ') + str(s.uptime()) + ' Hrs')
 
problem_matrix_left = [[38.016,0,0,0,0,0,29.04,36.3,0,0,0,0,0,0,0,0],[2.904,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,69.12576,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,52.8,0,0,0,70.126848,0,121.44,0,0,0,0,0,0,0,0],[0,0,25.08,0,0,0,25.344,0,0,0,0,0,0,0,0,0],[50.16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,26.4,19.8,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,11.88,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,3.564,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,21.12,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,6.072,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0.1056,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,65.16576,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
problem_matrix_right = [99.44,4.534,60,100,60,110.315,0,4.633,1.187,0.356,2.111,0.597,0.011,0,46.75,0]
 
info, rep, rx = s.computeFertilizer(problem_matrix_left,problem_matrix_right)
 
print("\n//======================================================")
print(str('TEST FERTILIZER SOLVING:'))
print(str(info))
print("\n//======================================================")
print(str('TEST FERTILIZER SOLUTION:'))
print(str(rep))
