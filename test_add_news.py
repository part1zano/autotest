# -*- coding: utf-8 -*-

from testlib import testcase,myrandom
import sys

class TestCase(testcase.TestObject):
	def execute(self):
		if not testcase.TestObject.execute(self):
			self.log.write('error', 'login failed')
			return False

		news_text = myrandom.randomPhrase()

		if not self.edit_control('add_event', news_text, clear=True, click=True):
			self.log.write('error', 'unable to add news: no edit or error editing')
			return False

		self.sleep(2)

		if not self.click_btn(u'Опубликовать'):
			self.log.write('error', 'no submit btn or error submitting')
			return False
		
		self.log.write('info', 'wrote %s into news' % news_text)

		self.sleep(2)

		if not self.check_div_value('news-view', news_text):
			self.log.write('error', 'no post in news')
			return False

		self.log.write('info', 'appeared in news...')

		if not self.visit_link('mc_sidebar_profile', 'news'):
			self.log.write('error', 'error visiting profile')
			return False

		if not self.check_div_value('news-view', news_text):
			self.log.write('error', 'no post in self-news')
			return False

		self.log.write('info', 'appeared in self-news!')

		return True

if __name__ == '__main__':
	tc = TestCase()
	sys.exit(int(not tc.execute()))
