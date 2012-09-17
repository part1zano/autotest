#-*- coding: utf-8 -*-

import sys
import test_recommend
from testlib import myrandom

class TestCase(test_recommend.TestCase):
	def request_recommendation_by_title(self, title_fragment, do=True, msg=''):
		link = u'Запросить рекомендацию'
		btns = {True: 'Отправить', False: 'Отмена'}
		if not self.find_stuff(title_fragment):
			self.log.write('error', 'error searching for stuff')
			return False

		if not self.visit_link(title_fragment, 'news', by='text'):
			self.log.write('error', 'error visiting news from search: maybe no search result?')
			return False

		if not self.click_btn(link):
			self.log.write('error', 'wrong recommendator or some shit')
			return False

		if not self.edit_control('//textarea[@name="dialog-ta"]', msg, by='xpath'):
			self.log.write('error', 'error editing msg textarea')
			return False

		if not self.click_btn(btns[do]):
			self.log.write('error', 'error clicking button to submit')
			return False

		return False

	def confirm_recommendation(self, asLogin='part1zancheg@gmail.com', asPasswd='fgihad5', do=True):
		if not self.logout():
			self.log.write('error', 'logout failed')
			return False

		self.login,self.password,asLogin,asPassword = asLogin,asPassword,self.login,self.password

		if not self.do_login():
			self.log.write('error', 'login as other face failed')
			self.login,self.password,asLogin,asPassword = asLogin,asPassword,self.login,self.password
			return False

		links = [
				{'link': 'mc_sidebar_our_proposers', 'url': 'our_proposers', 'by': 'id'},
				{'link': 'link_we_recommend', 'url': 'we_recommend', 'by': 'id'}
				]

		for link in links:
			if not self.visit_dlink(link):
				self.log.write('error', 'error visiting %s' % link['url'])
				return False

		if not check_div_value('we_recommend', self.info['brandName']):
			self.log.write('error', 'no brandName in recommend div')
			return False

		return True

	def execute(self):
		title_fragment = u'™'


		if not testcae.TestObject.execute(self):
			self.log.write('error', 'login failed')
			return False

		return True

if __name__ == '__main__':
	tc = TestCase()
	sys.exit(int(not tc.execute()))
