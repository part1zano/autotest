# -*- coding: utf-8 -*-

import sys
from testlib import testcase

class TestCase(testcase.TestObject):
	def __init__(self, config='tests.conf'):
		testcase.TestObject.__init__(self, config)

		self.links = self.make_json_list('json_lists/profile-links-nologin/links.json')

	def execute(self):
		if not self.find_stuff(u'™'):
			self.log.write('error', 'error accessing search')
			return False

		urls = []

		for link in self.links:
			if not self.visit_dlink(link, True):
				self.log.write('error', 'error visiting %s' % link['url'])
				return False

			divname = link['url']

			if not self.check_div(divname):
				self.log.write('error', 'no div id=%s at page, NOK' % divname)
				return False

			if link['url'] not in urls:
				for btn in [u'Написать сообщение', u'Подписаться на новости']: #, u'Добавить в контрагенты']:
					if not self.click_btn(btn):
						self.log.write('error', 'btn not found, see above')
						return False

					self.sleep(2)

					if not self.find_link(u'зарегистрируйтесь', by='text'):
						self.log.write('error', 'register link not found')
						return False

					self.sleep(2)

					if not self.click_btn(u'Закрыть', by='text'):
						self.log.write('error', 'close btn not found')
						return False
					self.sleep(2)
			
			urls.append(link['url'])

		return True

if __name__ == '__main__':
	tc = TestCase()
	sys.exit(int(not tc.execute()))
