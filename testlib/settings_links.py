#!/usr/bin/env python
# -*- coding: utf-8 -*-

from testlib import objlib
import re

class TestCaseSL(objlib.TestObject):
	def __init__(self, config='tests.conf', parent=None):
		objlib.TestObject.__init__(self, config, parent)

		self.links = {}

		for url in ['settings', 'additional-settings', 'change-password']:
			link_id = 'link_'+re.sub('-', '_', url)
			self.links[link_id] = url

	def click_links_dict(self, btn=u'Настройки', btn_url='settings'):
		if btn is not None:
			if not self.visit_link(btn, btn_url, by='text'):
				self.log.write('error', 'error visiting '+btn_url)
				return False
		for link_id, link_url in self.links.items():
			if not self.visit_link(link_id, link_url):
				self.log.write('error', 'error visiting link id='+link_id+', see above')
				return False

			divname = link_url
			if 'additional' in divname:
				divname = re.sub('-', '_', divname)

			if not self.check_div(divname):
				self.log.write('error', 'div not found: id='+divname)
				return False

			self.log.write('info', 'found div id='+divname)

		return True

	def execute(self):
		return self.click_links_dict()

if __name__ == '__main__':
	tc = TestCaseSL()
	if tc.do_login():
		if tc.execute():
			tc.log.write('info', 'test PASSED')
			sys.exit(0)

	tc.log.write('error', 'test FAILED, see above')
	sys.exit(1)


