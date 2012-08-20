#!/usr/bin/env python
# -*- coding: utf-8 -*-

from logger import Log
import time,ConfigParser
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,NoSuchElementException,WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

def get_browser(browser, proxy_host=None, proxy_port=None):
	if proxy_port is None:
		proxy_port = 8090
	if browser == 'firefox':
		if proxy_host is None:
			return webdriver.Firefox()
		else:
			fp = webdriver.FirefoxProfile()

			fp.set_preference('network.proxy.type', 1)

			for proto in ['http', 'ftp', 'ssl']:
				fp.set_preference('network.proxy.'+proto, proxy_host)
				fp.set_preference('network.proxy.'+proto+'_port', proxy_port)

			fp.set_preference('network.proxy.no_proxies_on', '')

			return webdriver.Firefox(firefox_profile=fp)
	elif browser == 'chrome':
		return webdriver.Chrome()
	else:
		return None


class TestObject():
	def __init__(self, config='tests.conf'):
		self.log = Log(config)
		cnf = ConfigParser.ConfigParser()
		cnf.read(config)
		self.url = cnf.get('net-creds', 'server')
		self.login = cnf.get('net-creds', 'login')
		self.password = cnf.get('net-creds', 'passwd')
		self.browser = cnf.get('browser', 'browser')

		self.driver = get_browser(self.browser) # FIXME :: proxy
		self.driver.get(self.url)
		self.links = []
		self.buttons = []
		self.edits = []
		self.results = []
	
	def new_objlist(self, objfile):
		objf = codecs.open(objfile, encoding='utf-8')
		objlist = objf.readlines()
		objf.close()

		for obj in objlist:
			if re.match('^#', obj):
				continue
			obj = obj.rstrip()

			name, value, submit, clear = obj.split('~!~')

			self.edits.append({'name': name, 'value': value, 'submit': bool(int(submit)), 'clear': bool(int(submit))})

	def __del__(self):
		self.driver.close()

	def sleep(self, time_):
		self.log.write('debug', 'sleepin for '+str(time_)+'s')
		time.sleep(time_)
		self.log.write('debug', 'woke up after sleep, next...')

	def go(self, url):
		if 'http' in url:
			self.driver.get(url)
		else:
			self.driver.get(self.url+'/'+url)

	def do_login(self, foreign=False):
		self.go(self.url)
		try:
			logins = self.driver.find_elements_by_name('username')
		except NoSuchElementException:
			self.log.write('error', 'no login elements')
			return False
		for login in logins:
			self.log.write('debug', 'found a login element')
			login.send_keys(self.login)
			self.log.write('debug', 'sent ' + self.login + ' into it')
		try:
			passwords = self.driver.find_elements_by_name('password')
		except NoSuchElementException:
			self.log.write('error', 'no password elements')
			return False
		for password in passwords:
			self.log.write('debug', 'found a password element')
			password.send_keys(self.password)
			self.log.write('debug', 'sent ' + self.password + ' into it')

		if foreign:
			try:
				foreign = self.driver.find_element_by_id('publicpc')
			except NoSuchElementException:
				self.log.write('error', 'no foreign computer checkbox')
				return False
			try:
				foreign.click()
				self.log.write('debug', 'foreign computer checkbox clicked')
			except WebDriverException:
				self.log.write('warning', 'foreign computer checkbox unclickable')
#			return False
		try:
			self.driver.find_element_by_name('login').click()
		except NoSuchElementException:
			self.log.write('error', 'No login button')
			return False
		self.log.write('debug', 'clicked "login"')

		try:
			WebDriverWait(self.driver, 10).until(lambda driver : u'profile' in self.driver.current_url)
			self.log.write('debug', 'logged in, visited profile')
		except TimeoutException:
			self.log.write('error', 'timeout waiting for shit to load')
			return False
		
		self.log.write('debug', 'sleeping for 2s waiting for shit to load')
		time.sleep(2)
		self.log.write('debug', 'woke up, will now check divs')

		if not self.check_page():
			self.log.write('error', 'some divs missing, see above')
			return False
		self.log.write('debug', 'divs ok')

		for cookie in self.driver.get_cookies():
			if bool(u'sessionid' in cookie['name'].lower()) != bool(foreign):
				self.log.write('debug', 'Cookies ok')
				return True
		self.log.write('error', 'Cookies not ok')
		return False

	def check_page(self):
		divs = ['content']
		if 'feedback' in self.driver.current_url:
			divs.append('feedback')
		else:
			divs.append('tabs_container')
			divs.append('tabs')
			divs.append('left-sidebar')
			if 'chat' in self.driver.current_url:
				divs.append('employee-header')
			else:
				divs.append('company-header')

		for divname in divs:
			if not self.check_div(divname):
				self.log.write('error', 'no such div: '+divname)
				return False
			self.log.write('debug', 'found '+divname)

		return True

	def check_div(self, divname):
		try:
			div = self.driver.find_element_by_id(divname)
		except NoSuchElementException:
			self.log.write('error', 'no such div id='+divname)
			return False

		self.log.write('info', 'found div id='+divname)
		self.log.write('debug', 'its content follows:'+div.text)
		return True

	def clear_element(self, control):
		try:
			self.driver.find_element_by_id(control).clear()
		except NoSuchElementException:
			self.log.write('error', 'no such element id='+control)
			return False

		self.log.write('verbose', 'cleared element id='+control)
		return True

	def edit_control(self, control, value, ctl_type='text', clear=False):
		try:
			ctl = self.driver.find_element_by_id(control)
		except NoSuchElementException:
			self.log.write('error', 'no such control id='+ctl)
			return False

		if ctl_type == 'text':
			self.log.write('debug', control+' is a textarea or so')
			old_value = ctl.get_attribute('value')
			self.log.write('debug', control+' value is: '+old_value)
			if clear:
				ctl.clear()
				new_value=old_value
			else:
				new_value=old_value+value

			ctl.send_keys(value)
			self.log.write('debug', 'sent '+value+' into control')

			return (ctl.get_attribute('value') == new_value)
		else:
			self.log.write('error', control+': unknown ctl type')
			return False

	def edit_all_controls(self, submit=u'Сохранить'):
		for edit in self.edits:
			if not self.edit_control(edit['name'], edit['value'], clear=bool(int(edit['clear']))):
				self.log.write('error', 'control '+edit['name']+' edit failed, see above')
				return False

			if bool(int(edit['submit'])):
				if self.click_btn(submit):
					self.log.write('error', 'some shit submitting, see above')
					return False

		return True

	def click_btn(self, btn_text):
		try:
			self.driver.find_element_by_partial_link_text(btn_text).click()
		except NoSuchElementException:
			self.log.write('error', 'no submit btn: '+btn_text)
			self.log.write('error', 'no submit btn!')
			return False

		return True

	def check_results(self):
		for result in self.reslts:
			try:
				res = driver.find_element_by_id(result['name'])
			except NoSuchElementException:
				self.log.write('error', 'no such field: '+result['name'])
				return False

			if res.text.lower() != result['value'].lower(): # FIXME :: dog-nail for fckn selenium
				self.log.write('error', 'field '+result['name']+' values dont match: NOK')
				self.log.write('error', 'should be: '+result['value'])
				self.log.write('error', 'but actually it is: '+res.text)
				return False

		return True

	def visit_link(self, link, url, by='id'):
		try:
			if by == 'id':
				self.driver.find_element_by_id(link).click()
			elif by == 'text':
				self.driver.find_element_by_partial_link_text(link).click()
			else:
				self.log.write('error', 'unknown link search criteria for '+link)
				return False
		except NoSuchElementException:
			self.log.write('error', 'no such link: '+link)
			return False

		try:
			WebDriverWait(self.driver, 10).until(lambda driver : url in self.driver.current_url)
		except TimeoutException:
			self.log.write('timeout waiting for shit to load or no '+url+' in cureent_url')
			return False

		self.log.write('info', 'got to '+url+', checkin divs')
		return self.check_page()


