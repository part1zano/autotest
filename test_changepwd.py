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
		Works on test case. Eats <case> (testcase name), reads edits from a json file, submits the form, checks error msg (taken from self.errors in an order)
		Maybe I should rewrite the script's errors in json?
		'''
		self.edits = self.make_json_list('json_lists/change-passwd/change-passwd-%s.json' % case)
		self.errors = self.make_json_list('json_lists/change-passwd/err-change-passwd-%s.json' % case)

		for edit in self.edits:
			if not self.dedit(edit):
				self.log.write('error', 'failed editing %s case %s' % (edit['name'], case))
				return False

			if bool(int(edit['submit'])):
				if not self.click_btn(u'Сохранить'):
					self.log.write('error', 'failed clicking submit')
					return False

				self.sleep(2)

				if not self.check_error(self.errors[0]['name'], self.errors[0]['value'], self.errors[0]['ok']):
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

#		errors = self.make_json_list('json_lists/change-passwd/changepwd-errors.json')

		result = True
		results = {True: 'PASSED', False: 'FAILED'}
		i = 0

		for case in ['pos', 'neg-nomatch', 'neg-1wrong', 'pos-symbols', 'afterall']:
#			self.errors = errors[3*i:3*i+3]
			result_ = self.work_case(case)
			self.log.write('info', 'case %s result: %s' % (case, results[result_]))
			result = result and result_

			i += 1

		return result

if __name__ == '__main__':
	tc = TestCase()
	if not tc.execute():
		tc.log.write('error', '%s FAILED, see above' % sys.argv[0])
		sys.exit(1)
	
	tc.log.write('info', '%s PASSED' % sys.argv[0])
	sys.exit(0)
