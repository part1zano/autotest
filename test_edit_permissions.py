#-*- coding: utf-8 -*-

from testlib import testcase,myrandom
import sys
import test_recommend, test_contragent

class TestCase(testcase.TestObject):
	def check_permission(self, perm, value):
		if 'news' in perm:
			links = self.make_json_list('json_lists/permissions/news.json')

			for link in links:
				if not self.visit_dlink(link):
					self.log.write('error', 'error visiting %s' % link['url'])
					return False

			post = myrandom.random_phrase()

			if self.edit_control('add_event', post, 'text', click=True) != value:
				self.log.write('error', 'wrong permission set for %s permission' % perm)
				return False

		elif 'contractors' in perm:
			links = self.make_json_list('json_lists/permissions/contractors.json')
			for link in links:
				if not self.visit_dlink(link):
					self.log.write('error', 'error visiting %s' % link['url'])
					return False

		elif 'recommend' in perm:
			pass
		elif 'finance' in perm:
			links = self.make_json_list('json_lists/permissions/deposit.json')
		elif 'company' in perm:
			links = self.make_json_list('json_lists/default-links.json')
		else:
			self.log.write('error', 'unknown permission type')
			return False

		return True

	def execute(self):
		self.title_fragment = u'»'
		self.links = self.make_json_list('json_lists/permissions/links.json')
		if not testcase.TestObject.execute(self):
			self.log.write('error', 'login failed')
			return False

		return True

if __name__ == '__main__':
	tc = TestCase()
	sys.exit(int(not tc.execute()))
