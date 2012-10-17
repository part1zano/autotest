#-*- coding: utf-8 -*-

from testlib import testcase
import sys

class TestCase(testcase.TestObject):
	def get_id_by_title(self, title_fragment):
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

	def remove_ctr_by_title(self, title_fragment, added=True):
		their_id = self.get_id_by_title(title_fragment)
		if their_id is None:
			self.log.write('error', 'null id: too bad, not un-contracting')
			return False

		self.go(self.url)

		links = [{'link': 'mc_sidebar_contractors', 'url': 'contractors', 'by': 'id'}]
		if not added:
			links.append({'link': 'link_out_reqs', 'url': 'outgoing', 'by': 'id'})

		for link in links:
			if not self.visit_dlink(link):
				self.log.write('error', 'error visiting %s while removing from ctrs' % link['url'])
				return False

		if not self.move_to('listelem_%s' % their_id, by='id'):
			self.log.write('error', 'error moving to list elem while deleting ctr')
			return False

		if not self.click_btn(u'Редактировать', by='text'):
			self.log.write('error', 'error clicking edit btn')
			return False

		self.sleep(2)

		if not self.click_btn(u'Удалить из контрагентов', by='text'):
			pass

		return True

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
			self.log.write('warning', 'trying to remove ctr')
			addeds = [True, False]
			for added in addeds:
				if not self.remove_ctr_by_title(title_fragment, added):
					self.log.write('warning', 'not removed pass %2d' % addeds.index(added))
				else:
					addeds.remove(added)
					break

			if len(addeds) > 1:
				self.log.write('error', 'didn\'t remove contractor, returning false')
				return False

		# btn clicked, going next



		return True

	def execute(self):
		if not testcase.TestObject.execute(self):
			self.log.write('error', 'login failed')
			return False

		return True

if __name__ == '__main__':
	tc = TestCase()
	sys.exit(int(not tc.execute()))
