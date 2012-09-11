#!/usr/bin/env python
# -*- coding: utf-8 -*-

from testlib import testcase
import sys

class TestCase(testcase.TestObject):
	def __init__(self, config='tests.conf'):
		testcase.TestObject.__init__(self, config)
		
		self.edits = self.make_json_list('json_lists/edit-profile/objlist-edit-profile.json')
		self.links = self.make_json_list('json_lists/default-links.json')
	
	def execute(self):
		if not testcase.TestObject.execute(self):
			return False

		for link in self.links:
			if not self.visit_dlink(link):
				self.log.write('error', 'no '+link['url']+' link or shit')
				return False

		for edit in self.edits:
			if not bool(int(edit['clear'])):
				value = self.get_value(edit['name'])+edit['value']
			else:
				value = edit['value']
			self.results.append({'name': edit['name'], 'value': value, 'method': 'equal'})
		if not self.click_btn(u'Редактировать'):
			self.log.write('error', 'btn click failure, see above')
			return False
		if not self.edit_all_controls():
			self.log.write('error', 'controls edit failure, see above')
			return False
		self.sleep(2)
		if not self.check_results():
			self.log.write('error', 'results NOK, see above')
			return False
		return True

if __name__ == '__main__':
	tc = TestCase()
	if not tc.execute():
		tc.log.write('error', '%s FAILED' % sys.argv[0])
		sys.exit(1)
	
	tc.log.write('info', '%s PASSED' % sys.argv[0])
	sys.exit(0)
