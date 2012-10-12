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

		urls = [self.info['url']]
		divs = ['news-subscriptions']
		titles = [title_fragment]
		linkchains = [[
			{'link': 'mc_sidebar_subscriptions', 'url': 'subscribed-people', 'by': 'id'},
			{'link': 'link_news_subscriptions', 'url': 'news-subscriptions', 'by': 'id'}
			]]
		
		if not self.click_btn(subscribe_btns[su_cond]):
			self.log.write('warning', 'possibly wrong subscribe direction: trying to fix')
			if not self.find_link(subscribe_btns[not su_cond], by='text'):
				self.log.write('error', 'no subscribe btns at all, NOK')
				return False
			self.log.write('warning', 'button found, continuing as is')

		for index in range(len(urls)):
			self.go(urls[index])

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

		for field in ('brandName', 'id', 'url'):
			self.info[field] = self.cut_string(self.get_our_info(field), 30)

		title_fragment = u'™'
		index = 0

		for condition in [True, False]:
			if not self.subscribe_by_title(title_fragment, condition):
				self.log.write('error', 'error subscribing pass %2d' % index)
				return False
			index += 1
			self.log.write('info', '%s pass %2d ok' % (sys.argv[0], index))

		return True


if __name__ == '__main__':
	tc = TestCase()
	sys.exit(int(not tc.execute()))
