#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''@file invite_test.py
Invite test. Just checks invite url and some textarea in it
'''

from testlib import testcase,myrandom
import sys,datetime,re

class TestCase(testcase.TestObject):
	def __init__(self, config='tests.conf'):
		'''The constructor. Eats the edits, links and errors, also makes up results'''
		testcase.TestObject.__init__(self, config)

		for objfile in ['invite-pos', 'invite-neg-reg-email', 'invite-neg-empty-email', 'invite-neg-empty-msg', 'invite-neg-already-sent']:
			for edit in self.make_json_list('json_lists/invite/'+objfile+'.json'):
				if 'random' in edit['value']:
					edit['value'] = myrandom.random_email()
				elif 'neg-reg-email' in objfile:
					edit['value'] = self.login
				self.edits.append(edit)

		self.links = self.make_json_list('json_lists/invite/linklist-invite.json')

		self.errors = self.make_json_list('json_lists/invite/errlist-invite.json')

		self.results.append({}) # empty
		self.results.append({'name': 'invites', 'value': '', 'method': 'grep'})

	def execute(self):
		'''Executor method'''
		if not testcase.TestObject.execute(self):
			self.log.write('error', 'login failed, see above')
			return False
		
		try:
			bname = self.json_info()['common_data']['brandName'][:20]
		except KeyError:
			self.log.write('error', 'error getting brandName')
			return False
				
		for link in self.links:
			if not self.visit_link(link['link'], link['url'], link['by']):
				self.log.write('error', 'error visiting '+link['url']+', see above')
				return False

		for index in range(len(self.edits)):
			if not self.dedit(self.edits[index]):
				self.log.write('error', 'error editing '+self.edits[index]['name']+', see above')
				return False

			if bool(int(self.edits[index]['submit'])):
				if not self.click_btn(u'Отправить'):
					self.log.write('error', 'couldnt click submit, see above')
					return False

				self.sleep(3)

				if index == 3:
					if not self.find_link(bname, 'text', 2):
						self.log.write('error', 'no brand name in msg-box')
						return False
				elif index == 1:
					self.results[index]['value'] = self.edits[index-1]['value']+u' - Отправлено '+datetime.date.today().strftime('%d.%m.%Y')

					if not self.check_result(self.results[index], True):
						self.log.write('error', 'no sent invite data')
						return False

				if not self.check_error(self.errors[index]['name'], self.errors[index]['value'], self.errors[index]['ok']):
					self.log.write('error', 'error/ok msg NOK')
					return False

				self.log.write('info', '%s pass %2d ok' % (sys.argv[0], int(index/2)))

		return True

if __name__ == '__main__':
	tc = TestCase()
	if not tc.execute():
		tc.log.write('error', '%s FAILED, see above' % sys.argv[0])
		sys.exit(1)
	
	tc.log.write('info', '%s PASSED' % sys.argv[0])
	sys.exit(0)
