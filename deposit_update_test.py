#-*- coding: utf-8 -*-

from testlib import testcase
import sys

class TestCase(testcase.TestObject):
	def __init__(self, config='tests.conf'):
		testcase.TestObject.__init__(self, config)
		
		self.links = self.make_json_list('json_lists/deposit-update/links.json')
		self.edits = self.make_json_list('json_lists/deposit-update/edits.json')
		self.errors = self.make_json_list('json_lists/deposit-update/errors.json')

	def execute(self):
		if not testcase.TestObject.execute(self):
			self.log.write('error', 'login failed')
			return False

		for link in self.links:
			if not self.visit_dlink(link):
				self.log.write('error', 'error visiting %s, see above' % link['url'])
				return False

		if not self.click_btn('wire-transfer-title', by='id'):
			self.log.write('error', 'update link unclickable, see above')
			return False

		num_of_results = len(self.driver.find_elements_by_xpath('//tr')) - 1

		for edit in self.edits:
			if not self.edit_control(edit['name'], edit['value'], by='id', clear=bool(int(edit['clear']))):
				self.log.write('error', 'error editing %s, see above' % edit['name'])
				return False

			if not self.click_btn(u'Выписать счет', by='text'):
				self.log.write('error', 'submit not clicked, see above')
				return False

			error = self.errors[self.edits.index(edit)]
			if not (error['name'] == error['value'] == ''):
				if not self.check_error(error['name'], error['value'], bool(int(error['ok']))):
					self.log.write('error', 'error-text NOK, see above')
					return False
			else:
				if num_of_results >= len(self.driver.find_elements_by_xpath('//tr')) - 1:
					self.log.write('error', 'no new field appeared')
					return False

				
		self.log.write('info', '%s PASSED' % sys.argv[0])
		return True

if __name__ == '__main__':
	tc = TestCase()
	sys.exit(int(not tc.execute()))
