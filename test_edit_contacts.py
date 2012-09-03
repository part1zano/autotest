#!/usr/bin/env perl
# -*- coding: utf-8 -*-

from testlib import testcase
import sys

class TestCase(testcase.TestObject):
	def __init__(self, config='tests.conf'):
		testcase.TestObject.__init__(self, config)

		self.links = self.make_json_list('json_lists/edit-contacts/linklist-edit-contacts.json')
		self.edits = self.make_json_list('json_lists/edit-contacts/objlist-edit-contacts.json')
		for edit in self.edits:
			self.results.append({'name': 'contacts', 'value': edit['value'], 'method': 'grep'})

	def execute(self):
		if not testcase.TestObject.execute(self):
			return False
		for link in self.links:
			if not self.visit_link(link['link'], link['url'], by=link['by']):
				self.log.write('error', 'error visiting '+link['url'])
				return False

		objlist_index = 0
		for edit in self.edits:
			if not self.click_btn(u'Редактировать'):
				self.log.write('error', 'error clicking edit btn')
				return False

			if not self.edit_control(edit['name'], edit['value'], clear=True):
				self.log.write('error', 'error editing '+edit['name']+', see above')
				return False

			if not self.click_btn(u'Сохранить'):
				self.log.write('error', 'error clicking save-btn')
				return False

			if not self.check_single_result(objlist_index, method='grep'):
				self.log.write('error', 'results dont match')
				return False
			objlist_index += 1
			self.log.write('info', '%s pass %2d ok' % (sys.argv[0], objlist_index))

		return True

if __name__ == '__main__':
	tc = TestCase()
	if not tc.execute():
		tc.log.write('error', 'test FAILED')
		sys.exit(1)
	
	tc.log.write('info', 'test PASSED')
	sys.exit(0)
