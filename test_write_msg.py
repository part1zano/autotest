#-*- coding: utf-8 -*-

from testlib import testcase,myrandom
import sys,re

class TestCase(testcase.TestObject):
	def send_msg_by_title(self, title_fragment, msg=myrandom.random_phrase()):
		if not self.find_stuff(title_fragment):
			self.log.write('error', 'search error')
			return False

		for link in self.links:
			if link['link'] == '%%title_fragment%%':
				link_ = re.sub('%%title_fragment%%', title_fragment, link['link'])

			if not self.visit_link(link_, link['url'], link['by']):
				self.log.write('error', 'error visiting %s, see above' % link['url'])
				return False

			

			return True

	def execute(self):
#		asLogin = self.aslogin
#		asPassword = self.aspwd
		self.links = self.make_json_list('json_lists/write-msg/links.json')
		if not testcase.TestObject.execute(self):
			self.log.write('error', 'login failed')
			return False

		return True

if __name__ == '__main__':
	tc = TestCase()
	sys.exit(int(not tc.execute()))
