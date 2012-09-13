#-*- coding: utf-8 -*-

from testlib import testcase
import sys

class TestCase(testcase.TestObject):
	def __init__(self, config='tests.conf'):
		testcase.TestObject.__init__(self,config)

		self.links = self.make_json_list('json_lists/categories/linklist_categories.json')
		self.categories = [
				{'id': 'ccat-startup', 'text': u'Стартап'},
				{'id': 'ccat-social_project', 'text': 'Социальный проект'},
				{'id': 'ccat-small', 'text': 'Малый бизнес'}
				]

	def find_category_text(self, category_item, shouldbe=True):
		pass

	def execute(self):
		if not testcase.TestObject.execute(self):
			self.log.write('error', 'login failed')
			return False

		self.info['brandName'] = self.get_our_info('brandName')

		for link in self.links:
			if not self.visit_dlink(link):
				self.log.write('error', 'error visiting %s' % link['url'])
				return False

		deletes = []

		self.log.write('debug', 'got to profile, checking categories present')

		for cat_item in self.categories:
			if self.find_link(cat_item['text'], by='text'):
				self.log.write('debug', 'found link for %s, it must be deleted' % cat_item['id'])
				deletes.append(cat_item)

		self.log.write('debug', 'found %2d categories' % len(deletes))
		
		if len(deletes) > 0:
			self.log.write('info', 'found categories to delete, deleting')
			if not self.click_btn(u'Редактировать'):
				self.log.write('error', 'error clicking edit')
				return False

			for delete in deletes:
				if not self.click_btn('//label[@for="%s"]' % delete['id'], by='xpath'):
					self.log.write('error', 'error clicking %s checkbox' % delete['id'])
					return False
				self.log.write('debug', 'submitted %s checkbox' % delete['id'])

			if not self.click_btn(u'Сохранить'):
				self.log.write('error', 'error submitting')
				return False
			self.log.write('info', 'deleted \'em all')

		for category in categories:
			if not self.click_btn(u'Редактировать'):
				self.log.write('error', 'error clicking edit for normal edit of category %s' % category['id'])
				return False

			if not self.click_btn('//label[@for="%s"]' % category['id'], by='xpath'):
				self.log.write('error', 'error clicking checkbox for %s' % category['id'])
				return False

			if not self.click_btn(u'Сохранить'):
				self.log.write('error', 'error submitting change for %s category' % category['id'])
				return False

			self.sleep(2)

			if not self.visit_link(category['text'], 'q', by='text'):
				self.log.write('error', 'error visiting search')
				return False

			if not self.find_link(self.info['brandName'], by='text'):
				self.log.write('error', 'brandName not found in search for category %s' % category['id'])
				return False

			self.driver.back()
			self.sleep(2)
			if not self.check_div('profile'):
				self.log.write('error', 'error returning to profile')
				return False

		return True

if __name__ == '__main__':
	tc = TestCase()
	sys.exit(int(not tc.execute()))
