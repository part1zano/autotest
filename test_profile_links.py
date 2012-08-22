#!/usr/bin/env python
# -*- coding: utf-8 -*-

from testlib import testcase
import sys,re

class TestCase(testcase.TestObject):
	def __init__(self, config='tests.conf'):
		testcase.TestObject.__init__(self, config)

		if not self.make_objlist('./objlists/profile-links/profile-links.conf', klasse='links'):
			self.log.write('error', 'objlist creation failure, see above')
			sys.exit(1)

	def execute(self):
		if not testcase.TestObject.execute(self):
			return False
		for linkitem in self.links:
			if not self.visit_link(linkitem['link'], linkitem['url'], by=linkitem['by']):
				self.log.write('error', 'couldnt visit '+linkitem['url'])
				return False

			divname = linkitem['url']
			if linkitem['url'] == 'topping-up':
				divname = linkitem['url'] = re.sub('-', '_', linkitem['url'])
			elif linkitem['url'] == 'chat':
				divname = 'dialog_list'
			elif linkitem['url'] in ('contractors', 'incoming', 'outgoing'):
				divname += 'list'

			if not self.check_div(divname):
				self.log.write('error', 'no div id='+divname)
				return False

		return True

if __name__ == '__main__':
	tc = TestCase()
	if not tc.execute():
		tc.log.write('error', 'test FAILED')
		sys.exit(1)
	tc.log.write('info', 'test PASSED')
	sys.exit(0)
