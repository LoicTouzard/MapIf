
import json

class Response:
    def __init__(self, has_error = True, content = {}):
        self.has_error = has_error
        self.content = content

    def json(self):
        return {'has_error': self.has_error, 'content': self.content}