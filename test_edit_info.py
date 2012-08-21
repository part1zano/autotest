#!/usr/bin/env python
# -*- coding: utf-8 -*-

from testlib import testcase
import sys

class TestCase(testcase.TestObject):
	def __init__(self, config='tests.conf'):
		testcase.TestObject.__init__(self, config)

		if not self.make_objlist('objlists/edit-profile/text/objlist-edit-profile.conf', 'edits'):
			self.log.write('error', 'objlist make error; see above')
			sys.exit(1)
	
	def execute(self):
		if not self.visit_link('link_profile', 'profile'):
			self.log.write('error', 'no profile link or shit')
			return False

		for edit in self.edits:
			if not bool(int(edit['clear'])):
				value = self.get_value(edit['name'])+edit['value']
			else:
				value = edit['value']
			self.results.append({'name': edit['name'], 'value': value})
		if not self.click_btn(u'Редактировать'):
			self.log.write('error', 'btn click failure, see above')
			return False
		if not self.edit_all_controls():
			self.log.write('error', 'controls edit failure, see above')
			return False
		if not self.check_results():
			self.log.write('error', 'results NOK, see above')
			return False
		return True

if __name__ == '__main__':
	tc = TestCase()
	if not tc.do_login():
		tc.log.write('error', 'login failed')
		sys.exit(1)
	
	if not tc.execute():
		tc.log.write('error', 'test FAILED')
		sys.exit(1)
	
	tc.log.write('info', 'test PASSED')
	sys.exit(0)
