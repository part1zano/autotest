#-*- coding: utf-8 -*-

from testlib import testcase
import sys

class TestCase(testcase.TestObject):
	def execute(self):
		if not testcase.TestObject.execute(self):
			self.log.write('error', 'login failed')
			return False

		self.links = self.make_json_list('json_lists/side_menu_links/links.json')

		if not self.move_to('//td[@class="ava"]', by='xpath'):
			self.log.write('error', 'error moving to avatar && opening side menu')
			return False

		for link in self.links:
			if not self.visit_dlink(link, sleep=True):
				self.log.write('error', 'error visiting %s' % link['url'])
				return False

		self.log.write('info', '%s PASSED' % sys.argv[0])
		return True

if __name__ == '__main__':
	tc = TestCase()
	sys.exit(int(not tc.execute()))
