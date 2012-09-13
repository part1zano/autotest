#!/usr/bin/env python
# -*- coding: utf-8 -*-

from testlib import testcase
import sys,re


class TestCase(testcase.TestObject):
	def __init__(self, config='tests.conf'):
		testcase.TestObject.__init__(self, 'tests.conf')

		self.links.append({'link': u'Обратная связь', 'url': 'feedback', 'by': 'text'})

		self.edits = self.make_json_list('json_lists/feedback/objlist-feedback.json')
		for edit in self.edits:
			if edit['value'] == '%%LOGIN%%':
				edit['value'] = re.sub('%%LOGIN%%', self.login, edit['value'])

		self.errors = self.make_json_list('json_lists/feedback/errlist-feedback.json')

	def execute(self):
		if not testcase.TestObject.execute(self):
			self.log.write('error', 'login failed, see above')
			return False

		for link in self.links:
			if not self.visit_link(link['link'], link['url'], by=link['by']):
				self.log.write('error visiting '+link['link']+', see above')
				return False

		if self.login != self.get_value('feedback-email'):
			self.log.write('error', 'email not entered before edit')
			return False

		self.log.write('info', 'email in field, thats ok')

		for index in range(len(self.edits)):
			if not self.edit_control(self.edits[index]['name'], self.edits[index]['value'], clear=bool(int(self.edits[index]['clear']))):
				self.log.write('error', 'failed editing '+self.edits[index]['name']+', see above')
				return False
			
			if bool(int(self.edits[index]['submit'])):
				if not self.click_btn(u'Отправить'):
					self.log.write('error', 'submit not clicked, see above')
					return False

				self.sleep(2)

				try:
					if not self.check_error(self.errors[index]['name'], self.errors[index]['value'], self.errors[index]['ok']):
						self.log.write('error', 'wrong err value for case %2d' % int(index/2))
						return False
				except IndexError:
					self.log.write('warning', 'index error for self.errors:something is REALLY wrong')

				self.log.write('info', '%s pass %2d ok' % (sys.argv[0], int(index/2)))

		return True

if __name__ == '__main__':
	tc = TestCase()

	if not tc.execute():
		tc.log.write('error', '%s FAILED, see above' % sys.argv[0])
		sys.exit(1)

	tc.log.write('info', '%s PASSED' % sys.argv[0])
	sys.exit(0)

