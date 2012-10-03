#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import ConfigParser

levels = ['debug', 'verbose', 'info', 'warning', 'error', 'stfu']

class Log:
	def __init__(self, conf):
		config = ConfigParser.ConfigParser()
		config.read(conf)
		self.level = config.get('log', 'level')
		self.stderr = bool(int(config.get('log', 'stderr')))
		self.syslog = bool(int(config.get('log', 'syslog')))

	def write(self, level, string):
		if level not in levels:
			return 1
		if level == 'stfu':
			return 2
		if levels.index(level) >= levels.index(self.level):
			if (levels.index(level) >= levels.index('warning')) and self.stderr:
				out = sys.stderr
			else:
				out = sys.stdout
			try:
				print >> out, level.upper() + ' ' + string 
			except UnicodeEncodeError:
				print >> out, level.upper() + ' ' + 'some shit with unicode, bro'

log = Log('tests.conf')
