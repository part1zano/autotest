#!/usr/bin/env python
# -*- coding: utf-8 -*-

from testlib import objlib
import re

class TestCase(objlib.TestObject):
	def __init__(self, config='tests.conf', parent=None):
		objlib.TestObject.__init__(self, config, parent)
		self.links = {}

		for link in ['profile', 'deposit', 'contractors', 'our_proposers', 'chat']:
			self.links['mc_sidebar_'+link] = [link, {}]
			if 'profile' in link:
				sublinks = ['profile', 'contacts']
			elif 'deposit' in link:
				sublinks = ['deposit', 'topping_up', 'payments']
			elif 'contractors' in link:
				sublinks = ['contractors_list', 'in_reqs', 'out_reqs']
			elif 'our_proposers' in link:
				sublinks = ['our_proposers', 'we_recommend', 'invites']
			elif 'chat' in link:
				sublinks = ['dialog_list']
			
			for sublink in sublinks:
				if 'contractors' in sublink:
					self.links['mc_sidebar_'+link][1]['link_'+sublink] = link
				elif '_reqs' in sublink:
					if 'in' in sublink:
						in_out = 'coming'
					else:
						in_out = 'going'
					self.links['mc_sidebar_'+link][1]['link_'+sublink] = re.sub('_reqs', in_out, sublink)
				elif 'chat' in link:
					self.links['mc_sidebar_'+link][1]['link_'+sublink] = link
				else:
					self.links['mc_sidebar_'+link][1]['link_'+sublink] = sublink

	def execute(self):
		for sidebar_id, tablinks in self.links.items():
			if not self.visit_link(sidebar_id, tablinks[0]):
				self.log.write('error', 'no sidebar link id='+sidebar_id)
				return False

			for tablink, taburl in tablinks[1].items():
				if 'deposit' in sidebar_id:
					taburl = re.sub('_', '-', taburl)

				if not self.visit_link(tablink, taburl):
					self.log.write('error', 'no tablink id='+tablink)
					return False

				layername=taburl
				if 'deposit' in sidebar_id:
					layername = re.sub('-', '_', layername)
				elif 'contractors' in sidebar_id:
					layername += 'list'
				elif 'chat' in sidebar_id:
					layername = re.sub('link_', '', tablink)

				if not self.check_div(layername):
					return False

		return True


if __name__ == '__main__':
	tc = TestCase('tests.conf')
	if tc.do_login():
		if tc.execute():
			tc.log.write('info', 'test PASSED')
			sys.exit(0)
	tc.log.write('error', 'test FAILED, see above')
	sys.exit(1)
