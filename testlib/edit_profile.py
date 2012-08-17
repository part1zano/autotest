#!/usr/bin/env python
# -*- coding: utf-8 -*-

from testlib import objlib
import re

class TestCase(objlib.TestObject):
	def __init__(self, config='tests.conf', objlist_file='./objlists/edit-profile/text/objlist-edit-profile.conf', parent=None):
		objlib.TestObject.__init__(self, config, parent)

		self.new_objlist(objlist_file)

	def edit_elems(self, edit_btn=u'Редактировать', submit_btn=u'Сохранить'):
		self.get(self.server)
		objlist_index = 0

		for objlist in self.objlists:
			
			self.log.write('debug', 'objlist #'+str(objlist_index))
			for obj in objlist:
				if re.match('^#', obj):
					continue
				if not self.click_button(edit_btn):
					self.log.write('error', 'error clicking button, see above')
					return False

				obj = obj.rstrip()

				name, value = obj.split('~!~')
				new_value = self.get_value(name)+value

				if 'estYear' in name:
					self.clear_element(name)
					new_value = value

				if not self.edit_control(name, value):
					self.log.write('error', 'editing '+name+' failed, see above')
					return False

				if not self.click_button(submit_btn):
					self.log.write('error', 'submit not found')
					return False

				self.sleep(2)

				if not self.check_value(name, new_value):
					self.log.write('error', 'values dont match: see above')
					return False
			self.log.write('debug', 'case '+str(objlist_index)+' ok')
			objlist_index += 1
		return True

	def execute(self):
		return self.edit_elems()

if __name__ == '__main__':
	tc = TestCase('tests.conf')
	if tc.do_login():
		if tc.execute():
			tc.log.write('info', 'test PASSED')
			sys.exit(0)
	
	tc.log.write('error', 'test FAILED, see above')
	sys.exit(1)
