
import sys
import platform

if sys.version_info[0:2] == (2, 7):
    from Modules.tobii import _tetiopy27
    tetio = _tetiopy27
else:
    raise Exception("Unsupported python runtime version, tobii.eye_tracking_io requires python 2.7")

#
# Internal class
#
class BoundHandler(object):
    def __init__(self, callback, *args):
        self._callback = callback
        self._args = args
    
    def __call__(self, opcode, error, payload):
        try:
            self._callback(opcode, error, payload, *self._args)
        except Exception, ex:
            print "Exception during BoundHandler.__call__(): ", ex
