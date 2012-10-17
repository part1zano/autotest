#-*- coding: utf-8 -*-

from testlib import testcase
import sys

class TestCase(testcase.TestObject):
	def get_id_by_title(self, title_fragment):
		url = self.driver.current_url
		if not self.find_stuff(title_fragment):
			self.log.write('error', 'error finding shit for getting its id')
			return None

		links = self.make_json_list('json_lists/default-links.json')

		for link in links:
			if not self.visit_dlink(link):
				self.log.write('error', 'error visiting %s for getting some fucker\'s id, see above' % link['url'])
				return None

		self.log.write('debug', 'url is %s' % self.driver.current_url)
		self.log.write('debug', 'this id is: %s, returning that shit' % self.driver.current_url.split('/')[3])

		return self.driver.current_url.split('/')[3]

	def add_ctr_by_title(self, title_fragment):
		their_id = self.get_id_by_title(title_fragment)
		if their_id is None:
			self.log.write('error', 'null id, stopping')
			return False
		if not self.find_stuff(title_fragment):
			self.log.write('error', 'error finding shit, see above')
			return False

		if not self.visit_link(title_fragment, 'news', by='text'):
			self.log.write('error', 'error visiting profile from search')
			return False

		if not self.click_btn(u'Добавить в контрагенты', by='text'): # fixing shit
			self.log.write('warning', 'no such btn or some shit')
			links = self.make_json_list('json_lists/default-links.json')

			if not self.go(self.url):
				self.log.write('error', 'error visiting main page')
				return False

			found = False

			for link in links:
				if not self.visit_dlink(link):
					self.log.write('error', 'error visiting %s, see above' % link['url'])
					return False

				if not self.find_link(title_fragment, by='text'):
					continue

				if not self.move_to(


		return True

	def execute(self):
		if not testcase.TestObject.execute(self):
			self.log.write('error', 'login failed')
			return False

		return True

if __name__ == '__main__':
	tc = TestCase()
	sys.exit(int(not tc.execute()))
