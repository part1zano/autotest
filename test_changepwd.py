#!/usr/bin/env python
# -*- coding: utf-8 -*-

from testlib import testcase
import sys

class TestCase(testcase.TestObject):
	def __init__(self, config='tests.conf'):
		testcase.TestObject.__init__(self, config)

		for objstr in ['pos', 'neg-nomatch', 'neg-1wrong', 'afterall']:
			for edit in self.make_json_list('json_lists/change-passwd/change-passwd-'+objstr+'.json'):
				self.edits.append(edit)

		self.links.append({'link': 'mc_sidebar_profile', 'url': 'news', 'by': 'id'})
		self.links.append({'link': u'Настройки', 'url': 'settings', 'by': 'text'})
		self.links.append({'link': 'link_change_password', 'url': 'change-password', 'by': 'id'})

		self.errors = self.make_json_list('json_lists/change-passwd/changepwd-errors.json')


	def execute(self):
		if not testcase.TestObject.execute(self):
			self.log.write('error', 'login failed, see above')
			return False

		for link in self.links:
			if not self.visit_dlink(link):
				self.log.write('error', 'failed visiting '+link['url']+', see above')
				return False

		# got to change-passwd
		index = 0
		for edit in self.edits:
			if not self.dedit(edit):
				self.log.write('error', 'failed editing '+edit['name']+' case '+str(index))
				return False

			if bool(int(edit['submit'])):
				if not self.click_btn(u'Сохранить'):
					self.log.write('error', 'failed clicking submit')
					return False

				self.sleep(2)

				if not self.check_error(self.errors[index]['name'], self.errors[index]['value'], self.errors[index]['ok']):
					self.log.write('error', 'error text NOK, case '+str(index))
					return False

				self.go(self.driver.current_url)

			self.log.write('info', '%s pass %2d ok' % (sys.argv[0], index))
			index += 1

		return True

if __name__ == '__main__':
	tc = TestCase()
	if not tc.execute():
		tc.log.write('error', 'test FAILED, see above')
		sys.exit(1)
	
	tc.log.write('info', 'test PASSED')
	sys.exit(0)
