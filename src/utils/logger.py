# -*- coding: utf-8 -*-

from .timer import get_date, get_diff
import traceback
import config

def read_file(filePath):
	with open(filePath, 'r') as file:
		print(file.read())

def append_content(filePath, content):
	with open(filePath, 'a') as file:
		file.write(content+'\n')

def write_content(filePath, content):
	with open(filePath, 'w') as file:
		file.write(content+'\n')

def log_performance(start, end, params, filePath):
	time = get_diff(start, end)
	date = get_date()
	content = date+" - Execution time = "+str(time)+" sec "+params

	if config.LOG_PERF:
		append_content(filePath, content)
	if config.PRINT_PERF:
		print(content)

def log_error(ex):
	date = get_date()
	with open('error.log', 'a') as f:
		f.write(date+" - ")
		traceback.print_exc(file=f)

def log_trace(msg):
	with open('trace.log', 'a') as f:
		f.write("{0}: {1}\n".format(get_date(), msg))
