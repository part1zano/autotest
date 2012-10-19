#-*- coding: utf-8 -*-

from testlib import testcase,myrandom
import sys

def to_bool(stri):
	return (stri.lower() not in ['false', 'none', ''])

class TestCase(testcase.TestObject):
	def check_permission(self, perm, value):
		if 'news' in perm:
			links = self.make_json_list('json_lists/permissions/news.json')

			for link in links:
				if not self.visit_dlink(link):
					self.log.write('error', 'error visiting %s' % link['url'], sleep=True)
					return False

			post = myrandom.random_phrase()

			if self.edit_control('add_event', post, 'text', click=True) != value:
				self.log.write('error', 'wrong permission set for %s permission' % perm)
				return False

		elif 'contractors' in perm:
			links = self.make_json_list('json_lists/permissions/contractors.json')
			links_novisit = self.make_json_list('json_lists/permissions/contractors-novisit.json')

		elif 'recommend' in perm:
			if not self.find_stuff(self.title_fragment):
				self.log.write('error', 'error finding shit and so')
				return False

			if not self.visit_link(title_fragment, 'news', by='text', sleep=True):
				self.log.write('error', 'error visiting profile from search')
				return False

			if self.click_btn(u'Дать рекомендацию', by='text') != value:
				self.log.write('error', 'recommend permission is NOK')
				return False
			elif self.click_btn(u'Отозвать рекомендацию', by='text') != value:
				self.log.write('error', 'recommend permission NOK')
				return False

		elif 'finance' in perm:
			links = self.make_json_list('json_lists/permissions/deposit.json')
			links_novisit = self.make_json_list('json_lists/permissions/deposit-novisit.json')

		elif 'company' in perm:
			links = self.make_json_list('json_lists/default-links.json')

			for link in links:
				if not self.visit_dlink(link, sleep=True):
					self.log.write('error', 'error visiting %s' % link['url'])
					return False

				if self.click_btn(u'Редактировать', by='text') != value:
					self.log.write('error', 'error clicking btn @ %s' % link['url'])
					return False

		else:
			self.log.write('error', 'unknown permission type')
			return False

		for link in self.links:
			if not self.visit_dlink(link, sleep=True):
				self.log.write('error', 'error visiting %s')
				return False
		try:
			for link in links_novisit:
				if self.visit_dlink(link, sleep=True):
					self.log.write('error', 'managed to visit %s: NOK' % link['url'])
					return False
		except NameError:
			pass

		return True

	def execute(self):
		self.links = self.make_json_list('json_lists/permissions/links.json')
		self.edits = self.make_json_list('json_lists/permissions/edits.json')
		if not testcase.TestObject.execute(self):
			self.log.write('error', 'login failed')
			return False

		try:
			self.info['uid'] = self.json_info()['common_data']['ownEmployee']['_id']
		except KeyError:
			self.log.write('error', 'error getting myid')
			return False

		for edit in self.edits:
			for link in self.links:
				if not self.visit_dlink(link, sleep=True):
					self.log.write('error', 'error visiting %s link' % link['url'])
					return False
			
			if not self.move_to('empllist_%s' % self.info['uid'], by='id'):
				self.log.write('error', 'error moving cursor to <li>')
				return False

			if not self.click_btn(u'Редактировать', by='text'):
				self.log.write('error', 'error clicking edit btn')
				return False

			if not self.edit_control(edit['name'], edit['value'], ctl_type='checkbox'):
				self.log.write('error', 'error editing %s' % edit['name'])
				return False

			if not self.check_permission(edit['name'], to_bool(edit['value'])):
				self.log.write('error', 'error checking permission %s' % edit['name'])

		self.log.write('info', '%s PASSED' % sys.argv[0])
		return True

if __name__ == '__main__':
	tc = TestCase()
	sys.exit(int(not tc.execute()))
