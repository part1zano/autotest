# -*- coding: utf-8 -*-

import sys
from testlib import testcase

class TestCase(testcase.TestObject):
	def __init__(self, config='tests.conf'):
		testcase.TestObject.__init__(self, config)

		self.links = self.make_json_list('json_lists/profile-links-nologin/links.json')

	def execute(self):
		if not self.find_stuff(u'™'):
			self.log.write('error', 'error accessing search')
			return False

		for link in self.links:
			if not self.visit_dlink(link):
				self.log.write('error', 'error visiting %s' % link['url'])
				return False

			divname = link['url']
			if 'contractors' in divname:
				divname += 'list'

			if not self.check_div(divname):
				self.log.write('error', 'no div id=%s at page, NOK' % divname)
				return False

		return True

if __name__ == '__main__':
	tc = TestCase()
	sys.exit(int(not tc.execute()))
