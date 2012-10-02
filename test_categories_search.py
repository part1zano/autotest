#-*- coding: utf-8 -*-

import test_categories
import sys

class TestCase(test_categories.TestCase):
	def execute(self):
		if not testcase.TestObject.execute(self):
			self.log.write('error', 'login failed')
			return False

		self.info['brandName'] = self.get_our_info('brandName')
		if self.info['brandName'] is None:
			self.log.write('error', 'brandName is null, exiting')
			return False

		for link in self.links:
			if not self.visit_link(link):
				self.log.write('error', 'error visiting %s, see above' % link['url'])
				return False

		inserts = []

		for ccat, name in categories.items():
			if not self.find_link(name, by='text'):
				toInsert.append({ccat: name})

		for category in toInsert:
			if not self.click_btn(u'Редактировать', by='text'):
				self.log.write('error', 'some shit pressing edit btn, see above')
				return False



		self.log.write('info', '%s PASSED' % sys.argv[0])
		return True

if __name__ == '__main__':
	tc = TestCase()
	sys.exit(int(not tc.execute()))
