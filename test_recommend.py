#!/usr/bin/env python
# -*- coding: utf-8 -*-

from testlib import testcase
import sys

class TestCase(testcase.TestObject):
	def __init__(self, config='tests.conf'):
		testcase.TestObject.__init__(self, config)
	
	def recommend_by_title(self, title_fragment, re_cond = True, accept = True):
		our_links = {'mc_sidebar_our_proposers': 'our_proposers', 'link_we_recommend': 'we_recommend'}
		their_links = {'mc_sidebar_our_proposers': 'our_proposers'}

		give_links = {True: u'Дать рекомендацию', False: u'Отозвать рекомендацию'}

		give_link = give_links[re_cond]
		
		btns = {True: {True: give_link, False: u'Отмена'}, False: {True: u'Да', False: u'Нет'}}

		btn = btns[re_cond][accept]

		if not self.find_stuff(title_fragment):
			self.log.write('error', 'error in search: see above')
			return False
		
		if not self.visit_link(title_fragment, 'news', 'text', True):
			self.log.write('error', 'error visiting profile from search, see above')
			return False
		
		info_cluster = {'links': [our_links, their_links], 
				'bnames': [title_fragment, self.info['brandName']], 
				'urls': [self.info['url'], self.driver.current_url],
				'divs': ['we_recommend', 'our_proposers'],
				'adjs': ['our', 'their']
				}

		if not self.click_btn(give_link):
			self.log.write('warning', 'no recommendation link or wrong direction')
			self.log.write('warning', 'trying to fix it')

			if not self.click_btn(give_links[not re_cond]):
				self.log.write('error', 'now for sure: no fucking link')
				return False

			if not self.click_btn(btns[not re_cond][True]):
				self.log.write('error', 'no button: %s' % btns[not re_cond][True])
				return False

			if not self.click_btn(give_link):
				self.log.write('error', 'fixed button doesn\'t appear to be clickable')
				return False
			
		
		if not self.click_btn_in_xpath('//div[@class="modalbox modalbox-default"]', btn):
			self.log.write('error', 'no accept-decline btn or something else strange and frightening')
			return False

		for i in range(2):
			self.go(info_cluster['urls'][i])
			for link, url in info_cluster['links'][i].items():
				if not self.visit_link(link, url, by='id'):
					self.log.write('error', 'link error: '+url)
					return False

			if not self.check_div_value(info_cluster['divs'][i], info_cluster['bnames'][i], (re_cond == accept)):
				self.log.write('error', 'no value in '+info_cluster['adjs'][i]+' info')
				return False

		return True
	
	def execute(self):
		if not testcase.TestObject.execute(self):
			self.log.write('error', 'login failed')
			return False

		for field in ['brandName', 'url']:
			self.info[field] = self.cut_string(self.get_our_info(field))
			if self.info[field] is None:
				self.log.write('error', 'error finding brand name, aborting')
				return False
		index = 0	
		for re_cond in [True, False]:
			for accept in [False, True]:
				index += 1
				if not self.recommend_by_title(u'™', re_cond, accept):
					self.log.write('error', 'recommend failed, case '+str(index))
					return False

				self.log.write('info', '%s pass %2d ok' % (sys.argv[0], index))

		return True

if __name__ == '__main__':
	tc = TestCase()
	if not tc.execute():
		tc.log.write('error', '%s FAILED, see above' % sys.argv[0])
		sys.exit(1)

	tc.log.write('info', '%s PASSED' % sys.argv[0])
	sys.exit(0)
