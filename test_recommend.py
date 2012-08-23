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
		
		if re_cond:
			give_link = u'Дать рекомендацию'
			if accept:
				btn = give_link
			else:
				btn = u'Отмена'
		else:
			give_link = u'Отозвать рекомендацию'
			if accept:
				btn = u'Да'
			else:
				btn = u'Нет'

		if not self.find_stuff(title_fragment):
			self.log.write('error', 'error in search: see above')
			return False
		
		if not self.visit_link(title_fragment, 'news', 'text'):
			self.log.write('error', 'error visiting profile from search, see above')
			return False
		
		info_cluster = {'links': [our_links, their_links], 
				'bnames': [title_fragment, self.info['brandName']], 
				'urls': [self.info['url'], self.driver.current_url],
				'divs': ['we_recommend', 'our_proposers'],
				'adjs': ['our', 'their']
				}

		if not self.click_btn(give_link):
			self.log.write('error', 'no recommendation link or wrong direction')
			return False
		self.sleep(2)
		if not self.click_btn(btn):
			self.log.write('error', 'no accept-decline btn or something else strange and frightening')
			return False

		for i in range(2):
			self.go(info_cluster['urls'][i])
			for link, url in info_cluster['links'][i].items():
				if not self.visit_link(link, url, by='id'):
					self.log.write('error', 'link error: '+url)
					return False
				if (self.check_div_value(info_cluster['divs'][i], info_cluster['bnames'][i]) != (re_cond == accept)):
					self.log.write('error', 'no value in '+info_cluster['adjs'][i]+' info')
					return False

		return True
	
	def execute(self):
		if not testcase.TestObject.execute(self):
			self.log.write('error', 'login failed')
			return False

		self.info = {}

		for field in ['brandName', 'url']:
			self.info[field] = self.get_our_info(field)
			if self.info[field] is None:
				self.log.write('error', 'error finding brand name, aborting')
				return False
		index = 0	
		for re_cond in [True, False]:
			for accept in [False, True]:
				index += 1
				if not self.recommend_by_title('Kaya', re_cond, accept):
					self.log.write('error', 'recommend failed, case '+str(index))
					return False

		return True

if __name__ == '__main__':
	tc = TestCase()
	if not tc.execute():
		tc.log.write('error', 'test FAILED, see above')
		sys.exit(1)

	tc.log.write('info', 'test PASSED')
	sys.exit(0)
