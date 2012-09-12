#-*- coding: utf-8 -*-

from testlib import testcase,myrandom
import sys

class TestCase(testcase.TestObject):
	def execute(self):
		if not testcase.TestObject.execute(self):
			self.log.write('error', 'login failed')
			return False

		comment_text = myrandom.randomPhrase()

		commented = False

		for elem_id in range(1, 100):
			if not self.click_btn_in_xpath('//ul/li[%d]/table' % elem_id, u'Комментировать'):
				self.log.write('warning', 'no comment link @ post # %d' % elem_id)
			else:
				self.log.write('info', 'found a post to comment #%d' % elem_id)
				self.sleep(2)
				if not self.edit_control('//ul/li[%d]/table/tbody/tr/td[2]/span/div/textarea' % elem_id, comment_text, by='xpath'):
					self.log.write('error', 'error adding comment')
					return False

				if not self.click_btn(u'Отправить'):
					self.log.write('error', 'error submitting comment')
					return False

				commented = True
				break

		if not commented:
			self.log.write('error', 'failed to find a comment link')
			return False

		self.log.write('info', 'wrote a comment, finding it in news')

		self.go(self.driver.current_url)

		if not self.check_div_value('news-view', comment_text):
			self.log.write('error', 'no comment in news')
			return False

		self.log.write('info', 'found comment in news!')

		if not self.visit_link('//ul/li[%d]/table/tbody/tr/td[2]/span/span/span/h3/a' % elem_id, 'news', by='xpath', sleep=True):
			self.log.write('error', 'error visiting OP\'s news')
			return False

		if not self.check_div_value('news', comment_text):
			self.log.write('error', 'no comment in their news')
			return False

		self.log.write('info', 'found comment in their news')

		return True

if __name__ == '__main__':
	tc = TestCase()
	sys.exit(int(not tc.execute()))
