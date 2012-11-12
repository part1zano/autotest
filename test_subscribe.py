# -*- coding: utf-8 -*-

from testlib import testcase,myrandom
import sys

class TestCase(testcase.TestObject):
	def subscribe_by_title(self, title_fragment, su_cond=True):
		subscribe_btns = {True: u'Подписаться', False: u'Отписаться'}

		if not self.find_stuff(title_fragment):
			self.log.write('error', 'search error, see above')
			return False

		if not self.visit_link(title_fragment, 'news', by='text', sleep=True):
			self.log.write('error', 'error visiting profile from search')
			return False

		urls = [self.info['url'], self.driver.current_url]
		divs = ['news-subscriptions', 'subscribed-people']
		titles = [title_fragment, self.info['brandName']]
		linkchains = [[
			{'link': 'mc_sidebar_subscriptions', 'url': 'news-subscriptions', 'by': 'id'}
			],
			[
				{'link': 'mc_sidebar_company_subscribers', 'url': 'subscribed-people', 'by': 'id'}
			]]
		
		if not self.click_btn(subscribe_btns[su_cond]):
			self.log.write('warning', 'possibly wrong subscribe direction: trying to fix')
			if not self.find_link(subscribe_btns[not su_cond], by='text'):
				self.log.write('error', 'no subscribe btns at all, NOK')
				return False
			self.log.write('warning', 'button found, continuing as is')

		for index in range(len(urls)):
			if not self.go(urls[index]):
				self.log.write('error', 'error getting to %s, see above' % urls[index])
				return False

			for link in linkchains[index]:
				if not self.visit_dlink(link, sleep=True):
					self.log.write('error', 'error visiting %s' % link['url'])
					return False

			if not self.check_div_value(divs[index], titles[index], su_cond):
				self.log.write('error', 'wrong %s div value' % divs[index])
				return False

		return True

	def execute(self):
		if not testcase.TestObject.execute(self):
			self.log.write('error', 'login failed, see above')
			return False

		self._info = self.json_info()

		for field in ['brandName', 'ownCompanyRekId']:
			try:
				self.info[field] = self._info['common_data'][field][:25]
			except KeyError:
				self.log.write('error', 'error getting %s' % field)
				return False

		self.info['id'] = self.info['ownCompanyRekId']
		self.info['url'] = self.url+'/'+self.info['id']+'/profile'

		title_fragment = u'™'
		index = 0

		for condition in [True, False]:
			if not self.subscribe_by_title(title_fragment, condition):
				self.log.write('error', 'error subscribing pass %2d' % index)
				return False
			index += 1
			self.log.write('info', '%s pass %2d ok' % (sys.argv[0], index))

		self.log.write('info', '%s PASSED' % sys.argv[0])
		return True


if __name__ == '__main__':
	tc = TestCase()
	sys.exit(int(not tc.execute()))
