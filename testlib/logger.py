#!/usr/bin/env python

import os, sys, string
import ConfigParser

def find_num(array, argument):
	for index in range(0, len(array)):
		if argument == array[index]:
			return index
	
	return None

levels = ['debug', 'info', 'warning', 'error', 'stfu']

class Log:
	def __init__(self, conf):
		config = ConfigParser.ConfigParser()
		config.read(conf)
		self.level = config.get('log', 'level')

	def write(self, level, string):
		if level not in levels:
			return 1
		if level == 'stfu':
			return 2
		if find_num(levels, level) >= find_num(levels, self.level):
			print level.upper() + ' ' + string 

log = Log('tests.conf')
