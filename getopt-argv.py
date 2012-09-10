#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,getopt,re

options, operands = getopt.getopt(sys.argv[1:], 'bu:d', ['test=', 'tr='])

config = {}
for name,value in options:
	config[re.sub('--', '', name)] = value

for name,value in config.items():
	print '%s -> %s' % (name, value)
	
