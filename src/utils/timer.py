#!/usr/bin/python3
# -!- encoding:utf8 -!-

# ------------------------------------------------------------------------------------------
#                                    IMPORTS & GLOBALS
# ------------------------------------------------------------------------------------------

import time

# ------------------------------------------------------------------------------------------
#                               EXTERN FUNCTIONS
# ------------------------------------------------------------------------------------------

def get_time():
    """
        Returns a timestamp in UNIX style
    """
    return time.time()

def get_date():
    """
        Returns a timestamp formated in a string
    """
    return str(time.strftime("(%d-%m-%Y %H:%M:%S)"))

def get_diff(start_time, end_time):
    """
        Computes a time delta
    """
    return end_time - start_time

# ------------------------------ TEST ZONE BELOW THIS LINE ---------------------------------

def test():
    """
        Module unit tests
    """
    print('TIMER TEST - get_time() returned {0}'.format(get_time()))
    print('TIMER TEST - get_date() returned {0}'.format(get_date()))
    print('TIMER TEST - get_diff(10, 35) returned {0}'.format(get_diff(10, 35)))