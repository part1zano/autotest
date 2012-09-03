#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from testlib import testcase
import sys,re

class TestCase(testcase.TestObject):
	def __init__(self, config='tests.conf'):
		testcase.TestObject.__init__(self, config)

		self.links = self.make_json_list('json_lists/settings-links/links.json')

	def execute(self):
		if not testcase.TestObject.execute(self):
			self.log.write('error', 'login failed')
			return False

		for link in self.links:
			if not self.visit_dlink(link):
				self.log.write('error', 'error visiting '+link['url']+', see above')
				return False

			divid = re.sub('-', '_', link['url'])

			if not self.check_div(divid):
				self.log.write('error', 'div id='+divid+' not found')
				return False

		return True

if __name__ == '__main__':
	tc = TestCase()
	sys.exit(int(not tc.execute()))
