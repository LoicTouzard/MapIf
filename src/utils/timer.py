# -*- coding: utf-8 -*-

import time

def get_time():
	return time.time()

def get_date():
	return str(time.strftime("[%d/%m/%Y %H:%M:%S]"))

def get_diff(start, end):
	return end - start
