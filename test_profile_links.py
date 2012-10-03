#!/usr/bin/env python
# -*- coding: utf-8 -*-

from testlib import testcase
import sys,re

class TestCase(testcase.TestObject):
	def __init__(self, config='tests.conf'):
		testcase.TestObject.__init__(self, config)

		self.links = self.make_json_list('json_lists/profile-links/profile-links.json')

	def execute(self):
		if not testcase.TestObject.execute(self):
			return False
		for linkitem in self.links:
			if not self.visit_link(linkitem['link'], linkitem['url'], by=linkitem['by'], sleep=True):
				self.log.write('error', 'couldnt visit '+linkitem['url'])
				return False

			divname = linkitem['url']
			if linkitem['url'] == 'topping-up':
				divname = linkitem['url'] = re.sub('-', '_', linkitem['url'])
			elif linkitem['url'] == 'news-feed':
				divname += '-block'
			elif linkitem['url'] == 'news':
				divname += '-view'
			elif linkitem['url'] == 'chat':
				divname = 'dialog_list'
			elif linkitem['url'] in ['contractors', 'incoming', 'outgoing']:
				divname += 'list'

			if not self.check_div(divname):
				self.log.write('error', 'no div id='+divname)
				return False

		return True

if __name__ == '__main__':
	tc = TestCase()
	if not tc.execute():
		tc.log.write('error', '%s FAILED' % sys.argv[0])
		sys.exit(1)
	tc.log.write('info', '%s PASSED' % sys.argv[0])
	sys.exit(0)
