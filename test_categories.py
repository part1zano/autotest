#-*- coding: utf-8 -*-

from testlib import testcase
import sys

class TestCase(testcase.TestObject):
	def __init__(self, config='tests.conf'):
		testcase.TestObject.__init__(self,config)

		self.links = self.make_json_list('json_lists/default-links.json')
		self.categories = [
				{'id': 'ccat-startup', 'text': u'Стартап'},
				{'id': 'ccat-social_project', 'text': u'Социальный проект'},
				{'id': 'ccat-small', 'text': u'Малый бизнес'}
				]

	def execute(self):
		if not testcase.TestObject.execute(self):
			self.log.write('error', 'login failed')
			return False
		
		try:
			self.info['brandName'] = self.json_info()['common_data']['brandName'][:12]
		except KeyError:
			self.log.write('error', 'error getting brandName')
			return False
		
		for link in self.links:
			if not self.visit_dlink(link, sleep=True):
				self.log.write('error', 'error visiting %s' % link['url'])
				return False

		for category in self.categories:
			if not self.click_btn(u'Редактировать'):
				self.log.write('error', 'error clicking edit for normal edit of category %s' % category['id'])
				return False

			if not self.edit_control(category['id'], True, ctl_type='checkbox'):
				self.log.write('error', 'error clicking checkbox for %s' % category['id'])
				return False

			if not self.click_btn(u'Сохранить'):
				self.log.write('error', 'error submitting change for %s category' % category['id'])
				return False

			self.log.write('debug', 'submitted change of category to %s' % category['id'])

			self.sleep(2)

			if not self.visit_link(category['text'], 'search', by='text'):
				self.log.write('error', 'error visiting search')
				return False

			self.sleep(2)
			self.go(self.driver.current_url)

			if not self.find_link(self.info['brandName'], by='text', count=2):
				self.log.write('error', 'brandName not found in search for category %s' % category['id'])
				return False

			self.log.write('info', 'found brandName for category %s, returning back to profile edit' % category['id'])

			self.driver.back()
			self.sleep(2)
			if not self.check_div('profile'):
				self.log.write('error', 'error returning to profile')
				return False

		self.log.write('info', '%s PASSED' % sys.argv[0])
		return True

if __name__ == '__main__':
	tc = TestCase()
	sys.exit(int(not tc.execute()))
