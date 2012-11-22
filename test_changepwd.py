#!/usr/bin/env python
# -*- coding: utf-8 -*-

from testlib import testcase
import sys

class TestCase(testcase.TestObject):
	def __init__(self, config='tests.conf'):
		testcase.TestObject.__init__(self, config)
		
		self.links = self.make_json_list('json_lists/change-passwd/changepwd-links.json')
	
	def work_case(self, case):
		'''
		Works on test case. Eats <case> (testcase name), reads edits from a json file, submits the form, checks errors.
		Errors are now stored in separate json files for each case. 
		'''
		edits = self.make_json_list('json_lists/change-passwd/change-passwd-%s.json' % case)
		errors = self.make_json_list('json_lists/change-passwd/err-change-passwd-%s.json' % case)

		for edit in edits:
			if not self.dedit(edit):
				self.log.write('error', 'failed editing %s case %s' % (edit['name'], case))
				return False

			if bool(int(edit['submit'])):
				if not self.click_btn(u'Сохранить'):
					self.log.write('error', 'failed clicking submit')
					return False

				self.sleep(2)

				if not self.check_error(errors[0]['name'], errors[0]['value'], errors[0]['ok']):
					self.log.write('error', 'error text NOK, case %s' % case)
					return False
				
				self.go(self.driver.current_url)

		return True

	def execute(self):
		if not testcase.TestObject.execute(self):
			self.log.write('error', 'login failed, see above')
			return False

		for link in self.links:
			if not self.visit_dlink(link, sleep=True):
				self.log.write('error', 'failed visiting '+link['url']+', see above')
				return False

		result = True
		results = {True: 'PASSED', False: 'FAILED'}

		for case in ['pos', 'neg-nomatch', 'neg-1wrong', 'pos-symbols', 'afterall']:
			result_ = self.work_case(case)
			self.log.write('info', 'case %s result: %s' % (case, results[result_]))
			result = result and result_

		return result

if __name__ == '__main__':
	tc = TestCase()
	if not tc.execute():
		tc.log.write('error', '%s FAILED, see above' % sys.argv[0])
		sys.exit(1)
	
	tc.log.write('info', '%s PASSED' % sys.argv[0])
	sys.exit(0)
