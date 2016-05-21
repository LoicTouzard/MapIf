#!/usr/bin/python3
# -!- encoding:utf8 -!-

# ------------------------------------------------------------------------------------------
#                                    IMPORTS & GLOBALS
# ------------------------------------------------------------------------------------------

import json
from src.utils import logger

# ------------------------------------------------------------------------------------------
#                                     RESPONSE CLASS
# ------------------------------------------------------------------------------------------

class Response:
    def __init__(self, has_error = True, content = {}):
        self.has_error = has_error
        self.content = content

    def json(self):
        return {'has_error': self.has_error, 'content': self.content}

# ------------------------------ TEST ZONE BELOW THIS LINE ---------------------------------

def test():
    """
        Module unit tests
    """
    out = 'NEGATIVE RESPONSE TEST\n'+json.dumps(Response(True, 'an error occured !').json(), indent=4)
    print(out)
    out = 'POSITIVE RESPONSE TEST\n'+json.dumps(Response(False, 'everything is OK.').json(), indent=4)
    print(out)
    