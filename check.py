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
 
problem_matrix_left = [[38.016,0,0,0,0,0,29.04,36.3,0,0,0,0,0,0,0,0],[2.904,0,0,0,0,0,0,0,0,0,0,0,0,$
problem_matrix_right = [99.44,4.534,60,100,60,110.315,0,4.633,1.187,0.356,2.111,0.597,0.011,0,46.75,$
 
info, rep, rx = s.computeFertilizer(problem_matrix_left,problem_matrix_right)
 
print("\n//======================================================")
print(str('TEST FERTILIZER SOLVING:'))
print(str(info))
print("\n//======================================================")
print(str('TEST FERTILIZER SOLUTION:'))
print(str(rep))
