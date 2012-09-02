#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import ConfigParser

def find_num(array, argument):
	for index in range(0, len(array)):
		if argument == array[index]:
			return index
	
	return None

levels = ['debug', 'verbose', 'info', 'warning', 'error', 'stfu']

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
			if find_num(levels, level) >= find_num(levels, 'warning'):
				out = sys.stderr
			else:
				out = sys.stdout
			try:
				print >> out, level.upper() + ' ' + string 
			except UnicodeEncodeError:
				print >> out, level.upper() + ' ' + 'some shit with unicode, bro'

log = Log('tests.conf')
