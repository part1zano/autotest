#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys,time,re,getopt

scripts_to_run = []
exclude_scripts = ['test_contragent.py', 'test_edit_permissions.py', 'test_repost.py', 'test_categories_search.py']
run_opts = ' '
all_ = False

options,operands = getopt.getopt(sys.argv[1:], 'b:c:e:l:u:da', ['browser=', 'config=', 'exclude=', 'level=', 'url=', 'debug', 'all'])

for name, value in options:
	if name in ('-e', '--exclude'):
		exclude_scripts.append(value)
	elif name in ('-a', '--all'):
		all_ = True
	else:
		run_opts += name+' '+value+' '

search_string = 'find . -maxdepth 1 -type f -name "test_*.py" '

if not all_:
	for script in exclude_scripts:
		search_string += ' -and -not -name "'+script+'"'

search_string += ' 2>/dev/null'

if len(operands) == 0:
	scripts_to_run = [script.rstrip() for script in os.popen(search_string).readlines()]
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
