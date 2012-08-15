#!/usr/bin/env python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from logger import Log
import string,time,stabledict,ConfigParser
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,NoSuchElementException,WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

class TestObject:
	def __init__(self, confFile='tests.conf', parent=None):
		self.log = Log(confFile)

		cnf = ConfigParser.ConfigParser()
		cnf.read(confFile)

		self.server = cnf.get('net-creds', 'server')
		self.login = cnf.get('net-creds', 'login')
		self.passwd = cnf.get('net-creds', 'passwd')
		browser = cnf.get('browser', 'browser')

		self.driver = get_browser(browser) # FIXME :: proxy

		self.driver.get(self.server)
		self.info = {}

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

	def check_div(self, div_id):
		try:
			div = self.driver.find_element_by_id(div_id)
			self.log.write('debug', 'found div id='+div_id)
			self.log.write('debug', 'its content follows: '+div.text)
		except NoSuchElementException:
			self.log.write('error', 'no such div id='+div_id)
			return False

		return True
	
	def doLogin(self, foreign=False):
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
			password.send_keys(self.passwd)
			self.log.write('debug', 'sent ' + self.passwd + ' into it')
		
		if foreign:
			try:
				publicpc = self.driver.find_element_by_id('publicpc')
			except NoSuchElementException:
				self.log.write('error', 'no foreign computer checkbox')
				return False
			try:
				publicpc.click()
				self.log.write('debug', 'foreign computer checkbox clicked')
			except WebDriverException:
				self.log.write('warning', 'foreign computer checkbox unclickable')
#				return False
		try:
			self.driver.find_element_by_name('login').click()
		except NoSuchElementException:
			self.log.write('error', 'No login button')
			return False
		self.log.write('debug', 'clicked "login"')

		try:
			WebDriverWait(self.driver, 10).until(lambda driver : u'profile' in self.driver.current_url)
		except TimeoutException:
			self.log.write('error', 'timeout waiting for shit to load')
			return False
		
		self.log.write('debug', 'logged in, visited profile')
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

	

def get_ff_proxy(proxy_host, proxy_port):
	fp = webdriver.FirefoxProfile()

	fp.set_preference('network.proxy.type', 1)

	for proto in ['http', 'ftp', 'ssl']:
		fp.set_preference('network.proxy.'+proto, proxy_host)
		fp.set_preference('network.proxy.'+proto+'_port', proxy_port)

	fp.set_preference('network.proxy.no_proxies_on', '')

	return webdriver.Firefox(firefox_profile = fp)

def get_browser(browser, proxy_host=None, proxy_port=None):
	"""
	doesn't work with chrome
	"""
	if proxy_port is None:
		proxy_port = 8090
	if browser == 'firefox':
		if proxy_host is None:
			return webdriver.Firefox()
		return get_ff_proxy(proxy_host, proxy_port)
	elif browser == 'chrome':
		return webdriver.Chrome()
	else:
		return None

