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

		if not self.visit_link(title_fragment, 'news', by='text', sleep=True):
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

	def confirm_recommendation(self, do=True, msg=''):
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
		
		self.sleep(2)

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

		if not self.check_div_value('we_recommend', msg):
			self.log.write('error', 'msg not found in we_recommend')
			return False

		if not self.click_btn(btns[do], by='text'):
			self.log.write('error', 'error clicking btn to submit aciton')
			return False

		return True

	def check_recommended_by_title(self, recommendator, recommended, mine=True): # FIXME :: me and not me
		links = [
				{'link': 'mc_sidebar_our_proposers', 'url': 'our_proposers', 'by': 'id'},
				{'link': 'link_we_recommend', 'url': 'we_recommend', 'by': 'id'}
				]
		divname = 'we_recommend'
		
		for link in links:
			if not self.visit_dlink(link,sleep=True):
				self.log.write('error', 'error visiting %s' % link['url'])
				return False

		self.sleep(2)

		if not self.check_div_value(divname, recommended):
			self.log.write('error', 'not finding who in %s' % divname)
			return False

		return True

	def undo_recommend(self, recommended):
		links = [
				{'link': 'mc_sidebar_our_proposers', 'url': 'our_proposers', 'by': 'id'},
				{'link': 'link_we_recommend', 'url': 'we_recommend', 'by': 'id'},
				{'link': recommended, 'url': 'news', 'by': 'text'}
				]
		btns = [u'Отозвать рекомендацию', u'Да']
		for link in links:
			if not self.visit_dlink(link):
				self.log.write('error', 'not visiting %s' % link['url'])
				return False

		for btn in btns:
			if not self.click_btn(btn):
				self.log.write('error', 'not unrecommending due to some shit with buttn %s' % btn)
				return False

		return True

	def execute(self):
		title_fragment = u'™'
#		asLogin = 'part1zancheg@gmail.com'
#		asPassword = 'fgihad5'
		asLogin = self.aslogin
		asPassword = self.aspwd
		message = myrandom.random_phrase()

		if not testcase.TestObject.execute(self):
			self.log.write('error', 'login failed')
			return False

		try:
			self.info['brandName'] = self.json_info()['common_data']['brandName'][:20]
		except KeyError:
			self.log.write('error', 'error getting brandName')
			return False

		if not self.request_recommendation_by_title(u'™', msg=message):
			self.log.write('error', 'error requesting recommendation')
			return False

		self.log.write('info', 'requested recommendation successfully')
		self.sleep(2)

		if not self.logout():
			self.log.write('error', 'error logging out')
			return False

		self.login,self.password,asLogin,asPassword = asLogin,asPassword,self.login,self.password
		if not self.do_login():
			self.log.write('error', 'error logging in as %s' % self.login)
			return False

		if not self.confirm_recommendation(msg=message):
			self.log.write('error', 'error confirming as %s' % self.login)
			return False

		self.log.write('info', 'confirmed recommendation successfully')

		self.go(self.url)
	
		if not self.check_recommended_by_title(title_fragment, self.info['brandName']):
			self.log.write('error', 'not recommended')
			return False

		self.log.write('info', 'checked: recommended')

		if not self.undo_recommend(self.info['brandName']):
			self.log.write('error', 'error unrecommending finally')
			return False

		self.log.write('info', 'cleanup after work done')
		self.log.write('info', '%s PASSED' % sys.argv[0])

		return True

if __name__ == '__main__':
	tc = TestCase()
	sys.exit(int(not tc.execute()))
