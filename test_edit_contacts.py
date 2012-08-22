#!/usr/bin/env perl
# -*- coding: utf-8 -*-

from testlib import testcase
import sys

class TestCase(testcase.TestObject):
	def __init__(self, config='tests.conf'):
		testcase.TestObject.__init__(self, config)

		self.links.append({'link': 'link_contacts', 'url': 'contacts', 'by': 'id'})
		self.make_objlist('objlists/edit-contacts/text/objlist-edit-contacts.conf', klasse='edits')
		for edit in self.edits:
			self.results.append({'name': 'contacts', 'value': edit['value'], })

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

		return True

if __name__ == '__main__':
	tc = TestCase()
	if not tc.execute():
		tc.log.write('error', 'test FAILED')
		sys.exit(1)
	
	tc.log.write('info', 'test PASSED')
	sys.exit(0)
