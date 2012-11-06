#!/usr/bin/env python
# -*- coding: utf-8 -*-

from testlib import testcase,myrandom
import sys

class TestCase(testcase.TestObject):
	def __init__(self, config='tests.conf'):
		testcase.TestObject.__init__(self, config)

		self.links = self.make_json_list('json_lists/edit-contacts/linklist-edit-contacts.json')
		domain = myrandom.random_domain()
		for edit in self.make_json_list('json_lists/edit-contacts/objlist-edit-contacts.json'):
			if 'phone' in edit['name']:
				edit['value'] = myrandom.random_phone()
			elif 'site' in edit['name']:
				edit['value'] = 'http://'+domain+'/'
			elif 'email' in edit['name']:
				edit['value'] = myrandom.random_login()+'@'+domain

			self.edits.append(edit)

		for edit in self.edits:
			self.results.append({'name': 'contacts', 'value': edit['value'], 'method': 'grep'})

	def execute(self):
		if not testcase.TestObject.execute(self):
			return False
		for link in self.links:
			if not self.visit_link(link['link'], link['url'], by=link['by'], sleep=True):
				self.log.write('error', 'error visiting '+link['url'])
				return False

		objlist_index = 0
		for edit in self.edits:
			if not self.click_btn(u'Редактировать'):
				self.log.write('error', 'error clicking edit btn')
				return False

			if not self.dedit(edit):
				self.log.write('error', 'error editing '+edit['name']+', see above')
				return False

			if not self.click_btn(u'Сохранить'):
				self.log.write('error', 'error clicking save-btn')
				return False
			self.sleep(2)
			if not self.check_result(self.results[objlist_index], True):
				self.log.write('error', 'results dont match')
				return False
			objlist_index += 1
			self.log.write('info', '%s pass %2d ok' % (sys.argv[0], objlist_index))

		return True

if __name__ == '__main__':
	tc = TestCase()
	if not tc.execute():
		tc.log.write('error', '%s FAILED' % sys.argv[0])
		sys.exit(1)
	
	tc.log.write('info', '%s PASSED' % sys.argv[0])
	sys.exit(0)
