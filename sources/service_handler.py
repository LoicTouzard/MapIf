# -*- coding: utf-8 -*-

from flask import jsonify
from sources.utils.timer import get_time
from sources.utils.logger import log_performance, log_error

def call_service(functionToRun, responseType, **kwargs):
    start = get_time()
    response = ""
    try:
        response = jsonify({ responseType: functionToRun(**kwargs) })
    except Exception as e:
        log_error(e)
        response = jsonify({ 'error': str(e) }), 400
    finally:
        end = get_time()
        params = "| GET endpoint = /"+responseType+" | "+str(kwargs)
        log_performance(start, end, params, "performance.log")
        return response
