#!/usr/bin/env python
# -*- coding: utf-8 -*-

import simplejson,re,codecs
links = []
index = 0
for link in ['settings', 'settings', 'additional-settings', 'change-password']:
	if index == 0:
		links.append({'link': u'Настройки', 'url': 'settings', 'by': 'text'})
	else:
		links.append({'link': 'link_'+re.sub('-', '_', link), 'url': link, 'by': 'id'})
	index += 1

fh = codecs.open('json_lists/settings-links/links.json', encoding='utf-8', mode='a+')
print simplejson.dumps(links)
fh.write(simplejson.dumps(links))
fh.close()


