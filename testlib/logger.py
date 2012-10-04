#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import ConfigParser
import syslog

levels = ['debug', 'verbose', 'info', 'warning', 'error', 'stfu']
priorities = [syslog.LOG_DEBUG, syslog.LOG_INFO, syslog.LOG_INFO, syslog.LOG_WARNING, syslog.LOG_ERR, None]

class Log:
	def __init__(self, conf):
		config = ConfigParser.ConfigParser()
		config.read(conf)
		self.level = config.get('log', 'level')
		self.stderr = bool(int(config.get('log', 'stderr')))
		self.syslog = bool(int(config.get('log', 'syslog')))
		if self.syslog:
			syslog.openlog(ident=sys.argv[0], logoption=syslog.LOG_PID, facility=syslog.LOG_USER)


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

			if self.syslog:
				try:
					syslog.syslog(priorities[levels.index(level)], level.upper()+' '+string)
				except:
					syslog.syslog(priorities[levels.index(level)], level.upper()+' '+'some shit with unicode, bro')


log = Log('tests.conf')
