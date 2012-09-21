#-*- coding: utf-8 -*-

from testlib import testcase
import sys

class TestCase(testcase.TestObject):
	def __init__(self, config='tests.conf'):
		testcase.TestObject.__init__(self, config)
		
		self.links = self.make_json_list('json_lists/profile-links/profile-links.json') # FIXME :: a lil bit wrong json_list
#		self.titles = self.make_json_list('json_lists/titles/titles.json') # FIXME :: unexistent file yet

	def find_dict_in(self, where, field, field_val):
		for elem in where:
			try:
				if elem[field] == field_val:
					return elem
			except KeyError:
				self.log.write('error', 'wrong dict type to search')
				return None

	def check_dtitle(self, title):
		if title['page_title'] not in self.driver.title:
			self.log.write('error', 'wrong title for url %s' % title['url'])
			self.log.write('error', 'should contain: %s' % title['page_title'])
			self.log.write('error', 'but is: %s' % self.driver.title)
			return False
		
		self.log.write('info', 'title ok for url %s' % title['url'])
		return True

	def execute(self):
		if not testcase.TestObject.execute(self):
			self.log.write('error', 'login failed')
			return False

		for link in self.links:
			if not self.visit_dlink(link):
				self.log.write('error', 'error visiting %s' % link['url'])
				return False

			title = self.find_dict_in(self.titles, 'url', link['url'])
			if title is None:
				self.log.write('error', 'wrong title file, check it!')
				return False

			if not self.check_dtitle(title):
				self.log.write('error', 'wrong title for url %s, see above' % link['url'])
				return False

		return True

if __name__ == '__main__':
	tc = TestCase()
	sys.exit(int(not tc.execute()))
