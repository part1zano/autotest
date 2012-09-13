#-*- coding: utf-8 -*-

import test_feedback
import sys

class TestCase(test_feedback.TestCase):
	def execute(self):
		for link in self.links:
			if not self.visit_dlink(link):
				self.log.write('error', 'error visiting %s' % link['url'])
				return False

		for edit in self.edits:
			if not self.edit_control(edit['name'], edit['value'], clear=bool(int(edit['clear']))):
				self.log.write('error', 'failed editing %s, see above' % edit['name'])
				return False

			if bool(int(edit['submit'])):
				if not self.click_btn(u'Отправить'):
					self.log.write('error', 'error submitting')
					return False

				self.sleep(2)

				error = self.errors[self.edits.index(edit)]
				try:
					if not self.check_error(error['name'], error['value'], error['ok']):
						self.log.write('error', 'wrong err value for case %2d' % int(self.edits.index(edit)/2))
						return False
				except IndexError:
					self.log.write('warning', 'index errors for self.errors: something is REALLY wrong')
					continue

				self.log.write('info', '%s pass %2d ok' % (sys.argv[0], int(self.edits.index(edit)/2)))

		return True

if __name__ == '__main__':
	tc = TestCase()
	sys.exit(int(not tc.execute()))
