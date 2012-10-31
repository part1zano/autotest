#-*- coding: utf-8 -*-

from testlib import testcase
import sys,re

class TestCase(testcase.TestObject):
	def __init__(self, config='tests.conf'):
		testcase.TestObject.__init__(self, config)
		
		self.links = self.make_json_list('json_lists/titles/profile-links.json') # FIXME :: a lil bit wrong json_list
		self.titles = self.make_json_list('json_lists/titles/titles.json') # FIXME :: unexistent file yet

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

		self._info = self.json_info()

		self.info['brandName'] = self._info['common_data']['brandName']
		ftuple = tuple(self._info['common_data']['ownEmployee'][field] for field in ['s_name', 'f_name', 'm_name'])
		self.info['fio'] = '%s %s %s' % ftuple

		if self.info['brandName'] is None:
			self.log.write('error', 'brandName is None, exiting')
			return False

		for title in self.titles:
			if '%%brandName%%' in title['page_title']:
				title['page_title'] = re.sub('%%brandName%%', self.info['brandName'], title['page_title'])
			elif '%%fio%%' in title['page_title']:
				title['page_title'] = re.sub('%%fio%%', self.info['fio'], title['page_title'])

		for link in self.links:
			if not self.visit_dlink(link, sleep=True):
				self.log.write('error', 'error visiting %s' % link['url'])
				return False

			if 'person/' in self.driver.current_url:
				title = self.find_dict_in(self.titles, 'url', 'person')
			else:
				title = self.find_dict_in(self.titles, 'url', link['url'])

			if title is None:
				self.log.write('error', 'wrong title file, check it!')
				return False

			if not self.check_dtitle(title):
				self.log.write('error', 'wrong title for url %s, see above' % link['url'])
				return False

		self.log.write('info', '%s passed' % sys.argv[0])
		return True

if __name__ == '__main__':
	tc = TestCase()
	sys.exit(int(not tc.execute()))
