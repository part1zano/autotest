#-*- coding: utf-8 -*-

from testlib import testcase
import sys

class TestCase(testcase.TestObject):
	def execute(self):
		if not testcase.TestObject.execute(self):
			self.log.write('error', 'login failed')
			return False

		self.info['uid'] = self.json_info()['common_data']['ownEmployee']['_id']
		to_detect = self.url+'/invites/from-person/'+self.info['uid']

		for link in self.make_json_list('json_lists/invite/links.json'):
			if not self.visit_dlink(link, sleep=True):
				self.log.write('error', 'error visiting %s' % link['url'])
				return False

		ta_value = self.get_value('textarea-message', by='id')
		if ta_value is None:
			self.log.write('error', 'error getting msg value')
			return False

		if to_detect not in ta_value:
			self.log.write('error', 'url not in textarea')
			return False

		self.log.write('info', '%s PASSED' % sys.argv[0])
		return True

if __name__ == '__main__':
	tc = TestCase()
	sys.exit(int(not tc.execute()))
