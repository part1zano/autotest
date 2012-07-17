#!/usr/bin/env python

import os,sys

scripts_to_run = []

if len(sys.argv) < 2:
	scripts_to_run = [script.rstrip() for script in os.popen('find . -type f -name "test-*.py"').readlines()]
else:
	scripts_to_run = ['./'+sys.argv[index] for index in range(1, len(sys.argv))]

for script in scripts_to_run:
	if os.system('python '+script) == 0:
		print script, 'PASSED'
	else:
		print script, 'FAILED'

