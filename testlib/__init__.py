__all__ = ['logger', 'testcase', 'myrandom']

import testcase

class TestCase(testcase.TestObject):
	def __init__(self, config='tests.conf'):
		testcase.TestObject.__init__(self,config)
