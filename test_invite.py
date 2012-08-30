#!/usr/bin/env python
# -*- coding: utf-8 -*-

from testlib import testcase
import sys,datetime

class TestCase(testcase.TestObject):
	def __init__(self, config='tests.conf'):
		testcase.TestObject.__init__(self, config)

		for objfile in ['invite-pos', 'invite-neg-reg-email', 'invite-neg-empty-email', 'invite-neg-empty-msg']:
			for edit in self.make_json_list('json_lists/invite/'+objfile+'.json'):
				self.edits.append(edit)

		self.links.append({'link': 'mc_sidebar_our_proposers', 'url': 'our_proposers', 'by': 'id'})
		self.links.append({'link': 'link_invites', 'url': 'invites', 'by': 'id'})

		self.errors.append({}) # empty
		self.errors.append({'name': None, 'value': None, 'ok': '1'})
		self.errors.append({}) # empty
		self.errors.append({'name': None, 'value': None, 'ok': '1'})
		self.errors.append({}) # empty
		self.errors.append({'name': 'informer-text', 'value': u'введите корректный адрес электронной почты', 'ok': '0'})
		self.errors.append({}) # empty
		self.errors.append({'name': 'informer-text', 'value': u'введите ваше сообщение', 'ok': '0'})

		self.results.append({}) # empty
		self.results.append({'name': 'invites', 'value': '', 'method': 'grep'})

	def execute(self):
		if not testcase.TestObject.execute(self):
			self.log.write('error', 'login failed, see above')
			return False
		
		bname = self.get_our_info('brandName')
		if bname is None:
			self.log.write('error', 'couldnt get bname, see above')
			return False
		
		for link in self.links:
			if not self.visit_link(link['link'], link['url'], link['by']):
				self.log.write('error', 'error visiting '+link['url']+', see above')
				return False

		for index in range(len(self.edits)):
			if index == 2:
				value = self.login
			else:
				value = self.edits[index]['value']
			if not self.edit_control(self.edits[index]['name'], value, clear=bool(int(self.edits[index]['clear']))):
				self.log.write('error', 'error editing '+self.edits[index]['name']+', see above')
				return False

			if bool(int(self.edits[index]['submit'])):
				if not self.click_btn(u'Отправить'):
					self.log.write('error', 'couldnt click submit, see above')
					return False
				if index == 3:
					if not self.find_link(bname, by='text'):
						self.log.write('error', 'no brand name in msg-box')
						return False
				elif index == 1:
					self.results[index]['value'] = self.edits[index-1]['value']+u' - Отправлено '+datetime.date.today().strftime('%d.%m.%Y')
					if not self.check_single_result(index, self.results[index]['method']):
						self.log.write('error', 'no sent invite data')
						return False

				if not self.check_error(self.errors[index]['name'], self.errors[index]['value'], self.errors[index]['ok']):
					self.log.write('error', 'error/ok msg NOK')
					return False

		return True

if __name__ == '__main__':
	tc = TestCase()
	if not tc.execute():
		tc.log.write('error', 'test FAILED, see above')
		sys.exit(1)
	
	tc.log.write('info', 'test PASSED')
	sys.exit(0)
