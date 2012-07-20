#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, string
import ConfigParser

def find_num(array, argument):
	for index in range(0, len(array)):
		if argument == array[index]:
			return index
	
	return None

levels = [u'debug', u'verbose', u'info', u'warning', u'error', u'stfu']

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
			try:
				print level.upper() + ' ' + string 
			except UnicodeEncodeError:
				print level.upper() + ' ' + 'some shit with unicode, bro'

log = Log('tests.conf')
