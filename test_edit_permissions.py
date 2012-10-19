#-*- coding: utf-8 -*-

from testlib import testcase,myrandom
import sys

class TestCase(testcase.TestObject):
	def check_permission(self, perm, value):
		if 'news' in perm:
			links = self.make_json_list('json_lists/permissions/news.json')
		elif 'contractors' in perm:
			pass
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
		self.links = self.make_json_list('json_lists/permissions/links.json')
		if not testcase.TestObject.execute(self):
			self.log.write('error', 'login failed')
			return False

		return True

if __name__ == '__main__':
	tc = TestCase()
	sys.exit(int(not tc.execute()))
