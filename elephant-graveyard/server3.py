# vim: tabstop=4 shiftwidth=4 softtabstop=4
#!/usr/bin/env python3
import os
import sys
import time
import logging
import atexit
import xalglib
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from daemon import runner
from array import *

# Functions Listed here
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

# Function: findBasePath
def findBasePath():
    # Check to see if we can write a PID file somewhere
    if check_file_writable('/var/run/iodineServer.pid'):
        basePath = str('/var/run/')
    elif check_file_writable('~/.iodineServer.pid'):
        basePath = str('~/')
    elif check_file_writable('/var/tmp/iodineServer.pid'):
        basePath = str('/var/tmp/')
    elif check_file_writable('/tmp/iodineServer.pid'):
        basePath = str('/tmp/')
    elif check_file_writable('./.iodineServer.pid'):
        basePath = str('./')
    else:
        print >> sys.stderr, "[Iodine Server][ERROR] PID locations not writable!"
        logging.info('[Iodine Server][ERROR] PID locations not writable!')
        sys.exit(1)
    #sys.stdout.write(str('[Iodine Server][INFO] Base Path: ' + basePath) + '\n')
    logging.info('[Iodine Server][INFO] Base Path: ' + basePath)
    return basePath

# Function: uptime - Returns system uptime
def uptime():
    uptime_seconds = open('/proc/uptime').read()
    return float(uptime_seconds.split()[0])/3600.0

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

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/iodineRPC2',)

class Server():
    def __init__(self):
        basePath = findBasePath()
        self.stdin_path = '/dev/null'
        self.stdout_path = basePath + 'iodine_daemon-stdout.log'
        self.stderr_path = basePath + 'iodine_daemon-stderr.log'
        self.pidfile_path = basePath + 'iodine_daemon.pid'
        self.pidfile_timeout = 5
        self.log_file = basePath + 'iodine_daemon.log'
        self.foreground = False
    def run(self):
        if not self.foreground:
            logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(message)s',
                            filename=self.log_file,
                            filemode='a')
        while True:
            # the main loop code.
            try:
		        # If this script is run as an individual command
                if self.foreground:
                    print('Running as stand-alone, please run as service daemon')
                else:
                    logging.info('[Iodine Server][INFO] Starting Server at port 2082')

                    self.server = SimpleXMLRPCServer(("localhost", 2082), requestHandler=RequestHandler)
                    self.server.register_introspection_functions()
                    # Register functions
                    self.server.register_function(uptime)
                    logging.info('[Iodine Server][INFO] Registered Uptime function')
                    self.server.register_function(compute_function, 'computeFertilizer')
                    logging.info('[Iodine Server][INFO] Registered computeFertilizer function')
                    #self.server.register_function(users)
                    #self.server.register_function(processes)
                    self.server.serve_forever()

            except:
                logging.info(sys.exc_info())
                logging.info('[Iodine Server][INFO] Terminating.')
                sys.exit(1)


#
# An example extension of runner.DaemonRunner class of python-daemon.
# Improvement points are:
#   - Natual unix getopt style option.
class MyDaemonRunner(runner.DaemonRunner):
    def __init__(self, app):
        # workaround... :(
        self.app_save = app

        self.detach_process = True
        runner.DaemonRunner.__init__(self, app)

    def parse_args(self, argv=None):
        # Note that DaemonRunner implements its own parse_args(), and
        # it is called in __init__ of the class.
        # Here, we override it following unix getopt style syntax.
        import getopt

        try:
            opts, args = getopt.getopt(sys.argv[1:],
                                        'skrl:p:fvh',
                                       ['start', 'kill', 'log_file=',
                                        'pid_file=', 'foreground'])
        except getopt.GetoptError:
            print(sys.exc_info())
            print('getopt error...')
            sys.exit(2)

        self.action = ''
        for opt, arg in opts:
            #print 'opt / arg :', opt, arg
            if opt in ('-s'):
                self.action = 'start'

            elif opt in ('-k'):
                self.action = 'stop'

            elif opt in ('-r'):
                self.action = 'restart'

            elif opt in ('-l', '--log_file'):
                # log_file is stored in the App object. But, here it's
                # pointed by 'app_save' attribute of MyDaemonRunner,
                # not by 'app'. This is because __init__ of DaemonRunner
                # calls parse_args() BEFORE recording app reference... :(
                self.app_save.log_file = arg
                # print 'setting log_file :' , self.app_save.log_file

            elif opt in ('-p', '--pidfile'):
                self.app_save.pidfile_path = arg
                #print('arg is :', arg)

            elif opt in ('-f', '--foreground'):
                self.detach_process = False
                self.app_save.stdout_path = '/dev/tty'
                self.app_save.stderr_path = '/dev/tty'
                self.app_save.foreground = True

            elif opt in ('-v'):
                self.verbose = True

            elif opt in ('-h', '--help'):
                print('show usage...')
                sys.exit(2)

            else:
                print('show usage')
                sys.exit(2)

        if not self.action:
            print(sys.argv[0] + ' (-s|-k|-r) [options]')
            sys.exit(1)
    #
    # FYI: The original parse_args() in runner.DaemonRunner class.
    #
    def original_parse_args(self, argv=None):
        """ Parse command-line arguments.
            """
        if argv is None:
            argv = sys.argv

        min_args = 2
        if len(argv) < min_args:
            self._usage_exit(argv)

        self.action = argv[1]
        if self.action not in self.action_funcs:
            self._usage_exit(argv)
#
#
#
if __name__ == '__main__':
    #app = App()
    app = Server()
    daemon_runner = MyDaemonRunner(app)
    if not app.foreground:
        daemon_runner.do_action()
    else:
        app.run()
