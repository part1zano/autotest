#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys,time

scripts_to_run = []

all_ = False

if not all_:
	search_string = 'find . -maxdepth 1 -type f -name "test-*.py" '
	for script in ['test-feedback.py', 'test-settings.py', 'test-contacts.py']:
		search_string = search_string + ' -and -not -name "'+script+'"'

if len(sys.argv) < 2:
	scripts_to_run = [script.rstrip() for script in os.popen(search_string).readlines()]
	#	scripts_to_run = [script.rstrip() for script in os.popen('find . -maxdepth 1 -type f -name "test-*.py" -and -not -name "test-feedback.py" -and -not -name "test-settings.py" -and -not -name "test-contacts.py"').readlines()]
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
