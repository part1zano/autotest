# -*- coding: utf-8 -*-

from testlib import testcase
import sys

class TestCase(testcase.TestObject):
	def execute(self):
		if not testcase.TestObject.execute(self):
			self.log.write('error', 'login failed')
			return False

		shared = False

		for elem_id in range(1, 10):
			if not self.click_btn_in_xpath('//ul/li[%d]/table' % elem_id, u'Поделиться'):
				self.log.write('warning', 'possibly, no share button at post %2d' % elem_id)
			else:
				shared = True
				post_text = self.get_xpath_text('//ul/li[%d]/table/tbody/tr/td[2]/span/span/span/p' % elem_id)
				break

		self.go(self.driver.current_url)
		
		if not shared:
			self.log.write('error', 'no post to share, sorry')
			return False

		if not self.check_div_value('news-view', post_text):
			self.log.write('error', 'no repost in news')
			return False
		
		if not self.visit_link('mc_sidebar_profile', 'news'):
			self.log.write('error', 'error visiting self-news')
			return False

		if not self.check_div_value('news-view', post_text):
			self.log.write('error', 'no repost in self-news')
			return False

		return True

if __name__ == '__main__':
	tc = TestCase()
	sys.exit(int(not tc.execute()))
