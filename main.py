#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""@package main.py
Starts all of the scripts

Supported command-line keys follow:
	* -b or --browser: for defining whether to run firefox or chrome (is passed to scripts)
	* -c or --config: to define the config file (is passed to scripts)
	* -e or --exclude: to define which script(s) to exclude from runlist (consumes it by itself)
	* -l or --level: to define log level (is passed to scripts)
	* -u or --url: to define url to go to start (is passed to scripts)
	* -d or --debug: to define log level as debug (is passed to scripts)
	* -a or --all: to define whether to run all of the scripts or no (by default, there is an internal runlist and an internal exclude list
"""

import os,sys,time,re,getopt

scripts_to_run = []
exclude_scripts = []
run_opts = ' '
all_ = False

options,operands = getopt.getopt(sys.argv[1:], 'b:c:e:l:u:da', ['browser=', 'config=', 'exclude=', 'level=', 'url=', 'debug', 'all'])

for name, value in options:
	if name in ('-e', '--exclude'):
		exclude_scripts.append(value)
	elif name in ('-a', '--all'):
		all_ = True
	else:
		run_opts += name+' '+value

search_string = 'find . -maxdepth 1 -type f -name "test_*.py" '
if not all_:
	for script in exclude_scripts:
		search_string += ' -and -not -name "'+script+'"'

search_string += ' 2>/dev/null'

if len(operands) == 0:
	scripts_to_run = [script.rstrip() for script in os.popen(search_string).readlines()]
	#	scripts_to_run = [script.rstrip() for script in os.popen('find . -maxdepth 1 -type f -name "test-*.py" -and -not -name "test-feedback.py" -and -not -name "test-settings.py" -and -not -name "test-contacts.py"').readlines()]
else:
	scripts_to_run = [script.rstrip() for script in operands]

fails = 0

for script in scripts_to_run:
	print '='*20
	print 'RUN TEST: '+script
	print '='*20
	if os.system('python '+script+run_opts) == 0:
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
