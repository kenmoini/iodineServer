#!/usr/bin/python

#==============================================================
# Iodine Server - Computation Engine for Salt Smarts
# Description: Creates an XML RPC Server to process formulae
#              from Salt Smarts, returns computation
# Author: Ken Moini (ken@kenmoini.com)
# License: GPLv3
#==============================================================

from array import *
#from Numeric import *
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import os
import sys
import atexit
import xalglib

def check_file_writable(fnm):
	if os.path.exists(fnm):
		# path exists
		if os.path.isfile(fnm): # is it a file or a dir?
			# also works when file is a link and the target is writable
			return os.access(fnm, os.W_OK)
		else:
			return False # path is a dir, so cannot write as a file
	# target does not exist, check perms on parent dir
	pdir = os.path.dirname(fnm)
	if not pdir: pdir = '.'
	# target is creatable if parent dir is writable
	return os.access(pdir, os.W_OK)


try:
	# Check to see if we can write a PID file somewhere
	if check_file_writable('/var/run/iodineServer.pid'):
		pidFile = str('/var/run/iodineServer.pid')
	elif check_file_writable('~/.iodineServer.pid'):
		pidFile = str('~/.iodineServer.pid')
	elif check_file_writable('/var/tmp/iodineServer.pid'):
		pidFile = str('/var/tmp/iodineServer.pid')
	elif check_file_writable('/tmp/iodineServer.pid'):
		pidFile = str('/tmp/iodineServer.pid')
	elif check_file_writable('./.iodineServer.pid'):
		pidFile = str('./.iodineServer.pid')
	else:
		print >> sys.stderr, "[Iodine Server][ERROR] PID locations not writable!"
		sys.exit(1)


	# Define atexit function
	def all_done():
		os.remove(pidFile)

	# Restrict to a particular path.
	class RequestHandler(SimpleXMLRPCRequestHandler):
		rpc_paths = ('/iodineRPC2',)

	# Create server
	server = SimpleXMLRPCServer(("173.255.196.122", 2082),requestHandler=RequestHandler)
	server.register_introspection_functions()

	# Register a function under a different name
	#def compute_function(rNo3,rNh4,rP,rK,rMg,rCa,rS,rFe,rZn,rB,rMn,rCu,rMo,rNa,rSi,rCl,lAS,rAS):
	def compute_function(lAS,rAS):
		#info, rep, x = xalglib.rmatrixsolvels(a, nrows, ncols, b, threshold)
		#INPUT PARAMETERS
		#    A       -   array[0..NRows-1,0..NCols-1], system matrix
		#    NRows   -   vertical size of A
		#    NCols   -   horizontal size of A
		#    B       -   array[0..NCols-1], right part
		#    Threshold-  a number in [0,1]. Singular values  beyond  Threshold  are
		#                considered  zero.  Set  it to 0.0, if you don't understand
		#                what it means, so the solver will choose good value on its
		#                own.
		#                
		#OUTPUT PARAMETERS
		#    Info    -   return code:
		#                * -4    SVD subroutine failed
		#                * -1    if NRows<=0 or NCols<=0 or Threshold<0 was passed
		#                *  1    if task is solved
		#    Rep     -   solver report, see below for more info
		#    X       -   array[0..N-1,0..M-1], it contains:
		#                * solution of A*X=B if A is non-singular (well-conditioned
		#                  or ill-conditioned, but not very close to singular)
		#                * zeros,  if  A  is  singular  or  VERY  close to singular
		#                  (in this case Info=-3).
		# solve equations using the MatrixSoleLS function
		#IMPORTANT LINE FOUND
		#    RMatrixSolveLS(problem_matrix_left, varcount, arraysize, problem_matrix_right,
		#      0.0, answer,
		#      report, solutions);
		#problem_matrix_left = formulations
		#varcount = 16
		#arraysize = 16
		#problem_matrix_right = intended concentrations
		#Misc Vars...
		threshold = 0.0
		nrows = 16
		ncols = 16
		info, rep, rx = xalglib.rmatrixsolvels(lAS, nrows, ncols, rAS, threshold)
		return [info, rep, rx]


	server.register_function(compute_function, 'computeFertilizer')
	atexit.register(all_done)

	# Setup PID file
	def writePidFile():
	    pid = str(os.getpid())
	    f = open('saltServer.pid', 'w')
	    f.write(pid)
	    f.close()

	writePidFile()

	# Run the server's main loop
	server.serve_forever()

except KeyboardInterrupt:
    sys.exit(0)
