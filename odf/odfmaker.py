#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Before running this shit, run something like:
	libreoffice --accept="socket,host=localhost,port=2002;urp;StarOffice.ServiceManager"
'''

import sys,re,uno,codecs

infile = codecs.open('persons.csv', encoding='utf-8')
objlist = [elem.rstrip() for elem in infile.readlines()]
infile.close()

local = uno.getComponentContext()
resolver = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
context = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
desktop = context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", context)

searchStrings = ['%%company%%', '%%surname%%', '%%name_f%%', '%%full_name%%']
arr_strings = ['%%company%%', '%%sex%%', '%%surname%%', '%%full_name%%', '%%phone%%', '%%address%%', '%%city%%', '%%name_f%%']

index = 0
for obj in objlist:
	index += 1
	document = desktop.loadComponentFromURL('file:///home/che/wrk/odf/template.odt', '_blank', 0, ())
	arr = obj.split(',')
	arr.append(arr[3].split(' ')[0][:1]+'. '+arr[3].split(' ')[1][:1]+'.')

	search = document.createSearchDescriptor()
	for searchString in searchStrings:
		search.SearchString = searchString
		found = document.findFirst(search)
		while found:
			found.String = re.sub(searchString, arr[arr_strings.index(searchString)], found.String)
			found = document.findNext(found.End, search)

	document.storeAsURL(u'file:///home/che/wrk/odf/work/'+arr[0]+u'.odt', ())
	document.dispose()
	if index >= 30:
		sys.exit(0)
