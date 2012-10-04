#-*- coding: utf-8 -*-

from testlib import testcase,myrandom
import sys,re

class TestCase(testcase.TestObject):
	def send_msg_by_title(self, title_fragment, msg=myrandom.random_phrase()):
		if not self.find_stuff(title_fragment):
			self.log.write('error', 'search error')
			return False

		for link in self.links:
			if link['link'] == '%%title_fragment%%':
				link_ = re.sub('%%title_fragment%%', title_fragment, link['link'])
			else:
				link_ = link['link']

			if not self.visit_link(link_, link['url'], link['by'], sleep=True):
				self.log.write('error', 'error visiting %s, see above' % link['url'])
				return False

		if not self.edit_control('chat_message_ta', msg, ctl_type='text', by='id'):
			self.log.write('error', 'error editing message textarea')
			return False
		self.log.write('debug', 'entered msg successfully')
		self.log.write('debug', 'msg is: %s' % msg)

		if not self.click_btn('send_message_btn', by='id'):
			self.log.write('error', 'error submitting msg')
			return False

		self.log.write('debug', 'submitted entered msg successfully')

		self.sleep(2)

		if not self.check_div_value('//ul[@class="messages"]', msg, by='xpath'):
			self.log.write('error', 'no msg appeared: NOK')
			return False

		self.log.write('info', 'sent msg successfully')

		return True

	def check_appeared_msg(self, msg):
		if not self.visit_link('main-header-chat-notification', 'chat', by='id', sleep=True):
			self.log.write('error', 'not going to chat, see above')
			return False

#		if not self.visit_link('//a[@class="open-dialog-action js-open-dialog-action"]', 'chat', by='xpath'):
#			self.log.write('error', 'error opening received msg')

#		if not self.check_div_value('//ul[@class="messages"]', msg, by='xpath'):
		if not self.check_div_value('dialog_list', msg):
			self.log.write('error', 'msg not received or wrong something')
			return False

		self.log.write('info', 'received msg successfully')
		return True


	def execute(self):
#		asLogin = self.aslogin
#		asPassword = self.aspwd
		self.links = self.make_json_list('json_lists/write-msg/links.json')
		if not testcase.TestObject.execute(self):
			self.log.write('error', 'login failed')
			return False

		msg = myrandom.random_phrase()
		if not self.send_msg_by_title(u'™', msg):
			self.log.write('error', 'error sending msg, see above')
			return False

		self.login, self.password, self.aslogin, self.aspwd = self.aslogin, self.aspwd, self.login, self.password
		if not self.logout():
			self.log.write('error', 'error logging out')
			return False

		if not self.do_login():
			self.log.write('error', 'error logging in as %s' % self.aslogin)
			return False

		if not self.check_appeared_msg(msg):
			self.log.write('error', 'msg not received, see above')
			return False

		self.log.write('info', '%s PASSED' % sys.argv[0])

		return True

if __name__ == '__main__':
	tc = TestCase()
	sys.exit(int(not tc.execute()))
