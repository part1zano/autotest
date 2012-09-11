# -*- coding: utf-8 -*-

import sys,getopt

options, operands = getopt.getopt(sys.argv[1:], 'b:c:e:l:u:d', ['debug'])

log_level = 'info'
browser = 'firefox'

for name, value in options:
	if name in ('-d', '--debug'):
		log_level = 'debug'
		print 'log level debug'
	elif (name == '-u') or (name == '--url'):
		url = value or url
	elif (name == '-b') or (name == '--browser'):
		browser = value or browser
	elif (name == '-l') or (name == '--level'):
		log_level = value or log_level

	print '%s -> %s' % (name, value)

for index in range(len(operands)):
	print 'operand %d -> %s' % (index, operands[index])
