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

		if not self.click_btn(u'Редактировать'):
			self.log.write('error', 'error clicking edit')
			return False

		for delete in deletes:



		return True

if __name__ == '__main__':
	tc = TestCase()
	sys.exit(int(not tc.execute()))
