#-*- coding: utf-8 -*-

import sys
from testlib import myrandom, testcase

class TestCase(testcase.TestObject):
	def request_recommendation_by_title(self, title_fragment, do=True, msg=''):
		link = u'Запросить рекомендацию'
		btns = {True: u'Отправить', False: u'Отмена'}
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

		return True

	def confirm_recommendation(self, do=True):
		''' Confirms recommendation
		Requires logout and login as another company before
		'''
		btns = {True: u'Рекомендовать', False: u'Отказать'}

		links = [
				{'link': 'mc_sidebar_our_proposers', 'url': 'our_proposers', 'by': 'id'},
				{'link': 'link_we_recommend', 'url': 'we_recommend', 'by': 'id'}
				]

		for link in links:
			if not self.visit_dlink(link):
				self.log.write('error', 'error visiting %s' % link['url'])
				return False

		if not self.check_div_value('we_recommend', self.info['brandName']):
			self.log.write('error', 'no brandName in recommend div')
			return False

		if not self.click_btn('//a[@class="arrow"]', by='xpath'):
			self.log.write('error', 'error finding buttons')
			return False

		self.sleep(2)

		if not self.find_link(u'Посмотреть профиль компании', by='text'):
			self.log.write('error', 'no profile link')
			return False

		if not self.click_btn(btns[do], by='text'):
			self.log.write('error', 'error clicking btn to submit aciton')
			return False

		return True

	def check_recommended_by_title(self, title_fragment, who, me=True): # FIXME :: me and not me
		'''
			A very buggy method
		'''
		if me:
			links = [
					{'link': 'mc_sidebar_our_proposers', 'url': 'our_proposers', 'by': 'id'}
					]
			divname = 'our_proposers'
		else:
			if not self.find_stuff(title_fragment):
				self.log.write('error', 'not going to search')
				return False
			links = [
					{'link': title_fragment, 'url': 'news', 'by': 'text'},
					{'link': 'mc_sidebar_our_proposers', 'url': 'our_proposers', 'by': 'id'},
					{'link': 'link_we_recommend', 'url': 'we_recommend', 'by': 'id'}
					]
			divname = 'we_recommend'

		for link in links:
			if not self.visit_dlink(link):
				self.log.write('error', 'error visiting %s' % link['url'])
				return False

		if not self.check_div_value(divname, who):
			self.log.write('error', 'not finding who in %s' % divname)
			return False

		return True

	def execute(self):
		title_fragment = u'™'
		asLogin = 'part1zancheg@gmail.com'
		asPassword = 'fgihad5'

		if not testcase.TestObject.execute(self):
			self.log.write('error', 'login failed')
			return False
		
		for field in ['brandName']:
			self.info[field] = self.get_our_info(field)
			if self.info[field] is None:
				self.log.write('error', 'error getting %s' % field)
				return False
			else:
				self.info[field] = self.cut_string(self.info[field], 30)

		if not self.request_recommendation_by_title(u'™'):
			self.log.write('error', 'error requesting recommendation')
			return False

		if not self.logout():
			self.log.write('error', 'error logging out')
			return False

		self.login,self.password,asLogin,asPassword = asLogin,asPassword,self.login,self.password
		if not self.do_login():
			self.log.write('error', 'error logging in as %s' % self.login)
			return False

		if not self.confirm_recommendation():
			self.log.write('error', 'error confirming as %s' % self.login)
			return False
	
		for me in (True, False):
			if not self.check_recommended_by_title(title_fragment, self.info['brandName'], me):
				self.log.write('error', 'not recommended')
				return False
		
		if not self.logout():
			self.log.write('error', 'error logging out as %s' % self.login)
			return False

		self.login,self.password,asLogin,asPassword = asLogin,asPassword,self.login,self.password

		if not self.do_login():
			self.log.write('error', 'error logging in as %s' % self.login)
			return False
		
		for me in (True, False):
			if not self.check_recommended_by_title(title_fragment, self.info['brandName'], me):
				self.log.write('error', 'not recommended')
				return False

		return True

if __name__ == '__main__':
	tc = TestCase()
	sys.exit(int(not tc.execute()))
