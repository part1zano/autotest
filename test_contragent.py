#-*- coding: utf-8 -*-

from testlib import testcase
import sys

class TestCase(testcase.TestObject):
	def get_id_by_title(self, title_fragment):
		if not self.find_stuff(title_fragment):
			self.log.write('error', 'error finding shit for getting its id')
			return None

		if not self.visit_link(title_fragment, 'news', by='text'):
			self.log.write('error', 'error visiting profile from search')
			return None

		links = self.make_json_list('json_lists/default-links.json')

		for link in links:
			if not self.visit_dlink(link, sleep=True):
				self.log.write('error', 'error visiting %s for getting some fucker\'s id, see above' % link['url'])
				return None

		self.log.write('debug', 'url is %s' % self.driver.current_url)
		self.log.write('debug', 'this id is: %s, returning that shit' % self.driver.current_url.split('/')[3])

		return self.driver.current_url.split('/')[3]

	def remove_ctr_by_title(self, title_fragment, added=True, out=False):
		their_id = self.get_id_by_title(title_fragment)
		if their_id is None:
			self.log.write('error', 'null id: too bad, not un-contracting')
			return False

		self.go(self.url)
		if out:
			links = self.make_json_list('json_lists/contractors/links-out.json')
		else:
			links = self.make_json_list('json_lists/contractors/links-in.json')

		if added:
			del links[1]

		for link in links:
			if not self.visit_dlink(link, sleep=True):
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
			self.log.write('error', 'error clicking delete link/btn')
			return False

		self.sleep(2)

#		if not self.click_btn(u'Удалить', by='text'):
		if not self.click_btn_in_xpath('//div[@class="modalbox modalbox-default"]', u'Удалить'):
			self.log.write('error', 'error committing')
			return False

		return True

	def add_ctr_by_title(self, title_fragment):
		links = self.make_json_list('json_lists/contractors/links-out.json')	

		if not self.find_stuff(title_fragment):
			self.log.write('error', 'error finding shit, see above')
			return False

		if not self.visit_link(title_fragment, 'news', by='text', sleep=True):
			self.log.write('error', 'error visiting profile from search')
			return False

		if not self.click_btn(u'Добавить в контрагенты', by='text'): # fixing shit
			self.log.write('warning', 'no such btn or some shit')
			self.log.write('warning', 'trying to remove ctr')
			addeds = [True, False]
			for added in addeds:
				if not self.remove_ctr_by_title(title_fragment, added, out=True):
					self.log.write('warning', 'not removed pass %2d' % addeds.index(added))
				else:
					addeds.remove(added)
					break

			if len(addeds) > 1:
				self.log.write('error', 'didn\'t remove contractor, returning false')
				return False

		# btn clicked, going next
		self.go(self.url)
		for link in links:
			if not self.visit_dlink(link, sleep=True):
				self.log.write('error', 'error visiting %s while checking whether added' % link['url'])
				return False

		self.go(self.driver.current_url)

		if not self.find_link(title_fragment, by='text'):
			self.log.write('error', 'title fragment not found in outgoing')
			return False

		return True

	def approve_ctr_request(self, id_):
		links = self.make_json_list('json_lists/contractors/links-in.json')

		for link in links:
			if not self.visit_dlink(link, sleep=True):
				self.log.write('error', 'error visiting %s while approving ctr request' % link['url'])
				return False

		if not self.move_to('listelem_%s' % id_, by='id'):
			self.log.write('error', 'error pointing to list elem, possibly no request')
			return False

		if not self.click_btn(u'Добавить в контрагенты', by='text'):
			self.log.write('error', 'error clicking approve btn, see above')
			return False

		if not self.visit_link('link_contractors_list', 'contractors', by='id', sleep=True):
			self.log.write('error', 'error going to ctr list, see above')
			return False

		return True

	def execute(self):
		if not testcase.TestObject.execute(self):
			self.log.write('error', 'login failed')
			return False

		title_fragment = u'™'
		try:
			self.info['id'] = self.json_info()['common_data']['ownCompanyRekId']
		except KeyError:
			self.log.write('error', 'error getting our id')
			return False

		if not self.add_ctr_by_title(title_fragment):
			self.log.write('error', 'error adding ctr, see above')
			return False

		self.login, self.password, self.aslogin, self.aspwd = self.aslogin, self.aspwd, self.login, self.password
		if not self.logout():
			self.log.write('error', 'error logging out')
			return False

		if not self.do_login():
			self.log.write('error', 'error logging in as %s, see above')
			return False

		if not self.approve_ctr_request(self.info['id']):
			self.log.write('error', 'error approving request from our id=%s' % self.info['id'])
			return False

		self.login, self.password, self.aslogin, self.aspwd = self.aslogin, self.aspwd, self.login, self.password
		if not self.logout():
			self.log.write('error', 'error logging out')
			return False

		if not self.do_login():
			self.log.write('error', 'error logging in as %s' % self.login)
			return False

		if not self.remove_ctr_by_title(title_fragment, added=True, out=True):
			self.log.write('error', 'error cleaning up, see above')
			return False

		self.log.write('info', '%s PASSED' % sys.argv[0])

		return True

if __name__ == '__main__':
	tc = TestCase()
	sys.exit(int(not tc.execute()))
