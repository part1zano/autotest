#!/usr/bin/env python
# -*- coding: utf-8 -*-

from testlib import testcase
import sys

class TestCase(testcase.TestObject):
	def __init__(self, config='tests.conf'):
		testcase.TestObject.__init__(self, config)

		self.links.append({'link': u'™', 'url': 'news', 'by': 'text'})

	def execute(self):
		if not testcase.TestObject.execute(self):
			self.log.write('error', 'login failed')
			return False

		if not self.find_stuff(u'™'):
			self.log.write('error', 'search failed')
			return False

		for link in self.links:
			if not self.visit_dlink(link):
				self.log.write('error', 'error visiting '+link['url'])
				return False

		self.click_btn(u'Написать сообщение')

		self.driver.back()
		
		return self.check_page()
#		return self.check_div('news')

if __name__ == '__main__':
	tc = TestCase()
	sys.exit(int(not tc.execute()))
