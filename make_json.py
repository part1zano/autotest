#!/usr/bin/env python

import sys,os,json,codecs,re,simplejson

for objdir in os.popen('ls objlists').readlines():
	objdir = objdir.rstrip()
	for objfile in os.popen('find objlists/'+objdir+' -type f').readlines():
		objfile = objfile.rstrip()
		basename = re.sub('conf', 'json', os.popen('basename '+objfile).readline().rstrip())
		print '+'+objfile+' ('+basename+')'
		if 'popup' in objfile:
			print 'popup detected'
			continue
		objlist = codecs.open(objfile, encoding='utf-8').readlines()
		toprint = []
		for obj in objlist:
			if re.match('^#', obj):
				continue
			obj = obj.rstrip()
			print '---'+obj
			cond = False
			for substr in ['pos', 'neg', 'objfile', 'text']:
				if substr in objfile:
					cond = True
			if cond:
				# objfile for controls
				name, value, submit, clear = obj.split('~!~')
				toprint.append({'name': name, 'value': value, 'submit': submit, 'clear': clear})
			else:
				# objfile for links
				link, text, by = obj.split('~!~')
				toprint.append({'link': link, 'text': text, 'by': by})

		json_file = codecs.open('json_lists/'+objdir+'/'+basename, mode='a+', encoding='utf-8')
		print simplejson.dumps(toprint)
		json_file.write(simplejson.dumps(toprint))
		json_file.close()

