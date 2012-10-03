#-*- coding: utf-8 -*-

from testlib import testcase
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
			if not self.visit_dlink(link):
				self.log.write('error', 'error visiting %s, see above' % link['url'])
				return False

		inserts = []

		for category in self.categories:
			if not self.find_link(category['text'], by='text'):
				inserts.append(category)

		if len(inserts) > 0:
			if not self.click_btn(u'Редактировать', by='text'):
				self.log.write('error', 'some shit pressing edit btn, see above')
				return False

		for category in inserts:
			if not self.click_btn('//label[@for="%s"]' % category['id'], by='xpath'):
				self.log.write('error', 'no such checkbox in profile-edit: %s' % category['id'])
				return False

		if len(inserts) > 0:
			if not self.click_btn(u'Сохранить'):
				self.log.write('error', 'error submitting info')
				return False

		if not self.visit_link(u'Компании', 'search', by='text', sleep=True):
			self.log.write('error', 'error visiting search')
			return False
		
		ids = [(0,1), (0,2), (1,2), (0,1,2)]

		for id_tuple in ids:
			for id_ in id_tuple:
				self.go(self.driver.current_url)
				if not self.click_btn('//label[@for="%s"]' % self.categories[id_]['id'], by='xpath'):
					self.log.write('error', 'error clicking %s checkbox' % self.categories[id_]['id'])
					return False

			self.sleep(2)

			if not self.find_link(self.info['brandName'], count=2, by='text'):
				try:
					self.log.write('error', 'brandName not found in set %d, %d' % (id_tuple)) # FIXME :: HUGE UGLY PIECE OF DOG-NAIL
				except TypeError:
					self.log.write('error', 'brandName not found in set %d, %d, %d' % (id_tuple)) # FIXME :: HUGE UGLY PIECE OF DOG-NAIL
				return False

		self.log.write('info', '%s PASSED' % sys.argv[0])
		return True

if __name__ == '__main__':
	tc = TestCase()
	sys.exit(int(not tc.execute()))
