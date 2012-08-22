#!/usr/bin/env python
# -*- coding: utf-8 -*-

from testlib import testcase
import sys


class TestCase(testcase.TestObject):
	def __init__(self, config='tests.conf'):
		testcase.TestObject.__init__(self, 'tests.conf')

		self.links.append({'link': u'Обратная связь', 'url': 'feedback', 'by': 'text'})

		self.edits.append({'name': 'feedback-email', 'value': '', 'submit': '1', 'clear': '1'})
		self.edits.append({'name': 'feedback-message', 'value': '', 'submit': '1', 'clear': '1'})
		self.edits.append({'name': 'feedback-message', 'value': 'This is just a test msg', 'submit': '1', 'clear': '0'})
		
		self.errors.append({'name': 'error-text', 'value': u'Неправильный e-mail'})
		self.errors.append({'name': 'error-text', 'value': u'Поле не должно быть пустым'})
		self.errors.append({'name': 'error-text', 'value': ''})

	def execute(self):
		if not testcase.TestObject.execute(self):
			self.log.write('error', 'login failed, see above')
			return False

		for link in self.links:
			if not self.visit_link(link['link'], link['url'], by=link['by']):
				self.log.write('error visiting '+link['link']+', see above')
				return False

		for index in range(len(self.edits)):
			if not self.edit_control(self.edits[index]['name'], self.edits[index]['value']):
				self.log.write('error', 'failed editing '+self.edits[index]['name']+', see above')
				return False
			
			try:
				if not self.check_error(self.errors[index]['name'], self.errors[index]['value']):
					self.log.write('error', 'wrong err value for case '+str(index))
					return False
			except IndexError:
				self.log.write('warning', 'index error for self.errors: something is REALLY wrong')

		return True

if __name__ == '__main__':
	tc = TestCase()

	if not tc.execute():
		tc.log.write('error', 'test FAILED, see above')
		sys.exit(1)

	tc.log.write('info', 'test PASSED')
	sys.exit(0)

