#!/usr/bin/python3
# -!- encoding:utf8 -!-

# ------------------------------------------------------------------------------------------
#                                    IMPORTS & GLOBALS
# ------------------------------------------------------------------------------------------

import os
import traceback
from src.utils import timer

_LOGS_ = None
_LOG_PERF_ = None
_LOG_DIR_ = None

# ------------------------------------------------------------------------------------------
#                               INTERNAL FUNCTIONS 
# ------------------------------------------------------------------------------------------

def _create_log(logfile):
    if _LOG_DIR_:
        if not os.path.exists(_LOG_DIR_):
            os.makedirs(_LOG_DIR_)
        with open(_LOG_DIR_+logfile, 'w+') as f:
            f.write("""
# ---------------------------------------------------
#    MapIf log file : {0}
#    Created at : {1}
# ---------------------------------------------------

""".format(logfile, timer.get_date()))

def _log(logfile, content):
    if _LOG_DIR_:
        with open(_LOG_DIR_+logfile, 'a') as f:
            f.write("{0} - {1}\n".format(timer.get_date(), content))

# ------------------------------------------------------------------------------------------
#                               EXTERN FUNCTIONS
# ------------------------------------------------------------------------------------------

# TODO : use a decorator instead, it will be more developer friendly that way.
def log_perf(start_time, end_time, params):
    if _LOG_PERF_:
        delta = timer.get_diff(start_time, end_time)
        _log("execution time = {0} sec {1}".format(str(delta), params))
    
def log_error(msg=None, ex=None):
    if _LOGS_:
        if msg:
            _log(_LOGS_['stderr'], msg)
        if ex:
            _log(_LOGS_['stderr'], "python traceback below :\n{0}".format(traceback.format_exc()))

def log_trace(msg):
    if _LOGS_:
        _log(_LOGS_['stdout'], msg)

def mprint(msg):
    logline = "{0}[mapif] > {1}".format(timer.get_date(), msg)
    log_trace(logline)
    print(logline)

def init_logs():
    global _LOGS_
    global _LOG_PERF_
    global _LOG_DIR_
    try:
        _LOG_DIR_ = ini.config('LOGGER', 'log_dir', default='logs/')
        _LOGS_ = {
            'stdout': ini.config('LOGGER', 'std_log', default='mapif.log'),
            'perfout': ini.config('LOGGER', 'perf_log', default='mapif.perf.log'),
            'stderr': ini.config('LOGGER', 'err_log', default='mapif.err.log')
        }
        _LOG_PERF_ = ini.config('LOGGER','log_perf', default=False, boolean=True)
        for logfile in _LOGS_.values():
            _create_log(logfile)
        mprint("Logging module successfully initialized.")
    except Exception as e:
        log_error("Logging module initialization failed.", e)
    


# ------------------------------ TEST ZONE BELOW THIS LINE ---------------------------------

if __name__ == '__main__':
    mprint('TESTS NOT IMPLEMENTED')