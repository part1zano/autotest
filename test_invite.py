#-*- coding: utf-8 -*-

from testlib import testcase
import sys

class TestCase(testcase.TestObject):
	def execute(self):
		if not testcase.TestObject.execute(self):
			self.log.write('error', 'login failed')
			return False

		self.log.write('info', '%s PASSED' % sys.argv[0])
		return True

if __name__ == '__main__':
	tc = TestCase()
	sys.exit(int(not tc.execute()))
