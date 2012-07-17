#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys

scripts_to_run = []

if len(sys.argv) < 2:
	scripts_to_run = [script.rstrip() for script in os.popen('find . -maxdepth 1 -type f -name "test-*.py"').readlines()]
else:
	scripts_to_run = ['./'+sys.argv[index] for index in range(1, len(sys.argv))]

for script in scripts_to_run:
	print '='*20
	print 'RUN TEST: '+script
	print '='*20
	if os.system('python '+script) == 0:
		result = 'PASSED'
	else:
		result = 'FAILED'

	print '='*20
	print 'RESULT: ', script, result
	print '='*20
