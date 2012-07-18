#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys,time

for param_name, param in os.environ.iteritems():
	print "%s -> %s" % (param_name, param)

scripts_to_run = []

if len(sys.argv) < 2:
	scripts_to_run = [script.rstrip() for script in os.popen('find . -maxdepth 1 -type f -name "test-*.py"').readlines()]
else:
	scripts_to_run = ['./'+sys.argv[index] for index in range(1, len(sys.argv))]

fails = 0

for script in scripts_to_run:
	if 'bug-208' in script: # buggy bug 208 reproduction
		continue

	print '='*20
	print 'RUN TEST: '+script
	print '='*20
	if os.system('python '+script) == 0:
		result = 'PASSED'
	else:
		result = 'FAILED'
		fails = fails+1

	print '='*20
	print 'RESULT: ', script, result
	print '='*20

	time.sleep(2)

if fails > 0:
	sys.exit(1)
