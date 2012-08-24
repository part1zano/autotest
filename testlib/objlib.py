#!/usr/bin/env python
# -*- coding: utf-8 -*-

from logger import Log
import time,stabledict,ConfigParser,codecs
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
		try:
			self.proxy_host = cnf.get('proxy', 'host')
			self.proxy_port = cnf.get('proxy', 'port')
		except ConfigParser.Error:
			self.proxy_host = None
			self.proxy_port = None
		browser = cnf.get('browser', 'browser')

		self.driver = get_browser(browser, self.proxy_host, self.proxy_port) # FIXME :: proxy

		self.driver.get(self.server)
		self.info = {}
		self.objlists = []
		self.links = stabledict.StableDict()

	def __del__(self):
		self.driver.close()

	def sleep(self, time_):
		time.sleep(time_)

	def get_value(self, control):
		try:
			ctl = self.driver.find_element_by_id(control)
		except NoSuchElementException:
			self.log.write('error', 'element not found: '+control)
			return None

		if ctl.get_attribute('value') is not None:
			return ctl.get_attribute('value')
		else:
			return ctl.text

	def clear_element(self, element):
		try:
			self.driver.find_element_by_id(element).clear()
		except NoSuchElementException:
			self.log.write('error', 'no such element to clear: '+element)
			return False
		
		self.log.write('debug', 'cleared '+element+' successfully')
		return True

	def click_button(self, link):
		try:
			self.driver.find_element_by_partial_link_text(link).click()
		except NoSuchElementException:
			self.log.write('error', 'no such button '+link)
			return False

		return True
	
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

	def get_our_info(self, field):
		url = self.driver.current_url
		self.driver.get(self.server)

		if field == 'id':
			info = self.driver.current_url.split('/')[3]
		elif field == 'url':
			info = self.driver.current_url
		else:
			try:
				info = self.driver.find_element_by_id(field).text
			except NoSuchElementException:
				self.log.write('error', 'no such field in profile')
				info = None

		self.driver.get(url)
		return info

	def get(self, url):
		if 'http' in url:
			self.driver.get(url)
		else:
			self.driver.get(self.server+url)

	def new_objlist(self, obj_file):
		objfile = codecs.open(obj_file, encoding='utf-8')
		self.objlists.append(objfile.readlines())
		self.log.write('debug', 'new objlist from file '+obj_file)
		objfile.close()

	def edit_control(self, control, value, ctl_type='text'):
		try:
			ctl = self.driver.find_element_by_id(control)
		except NoSuchElementException:
			self.log.write('error', 'no such element '+control)
			return False

		old_value = ctl.get_attribute('value')
		self.log.write('debug', 'old value for '+control+' is: '+old_value)

		if ctl_type == 'text':
			self.log.write('debug', control+' is a textarea or so')
			ctl.send_keys(value)
			self.log.write('debug', 'sent '+value+' into '+control)
			return (self.get_value(control).lower() == (old_value+value).lower())

		else:
			self.log.write('error', 'unsupported control type')
			return False

	def check_value(self, control, value):
		return (self.get_value(control).lower() == value.lower())

	
	def visit_link(self, text, url, by='id'):
		try:
			if by == 'id':
				link = self.driver.find_element_by_id(text)
			elif by == 'text':
				link = self.driver.find_element_by_partial_link_text(text)
			else:
				self.log.write('error', 'unknown link search type')
				return False
		except NoSuchElementException:
			self.log.write('error', 'no such link')
			return False

		link.click()

		try:
			WebDriverWait(self.driver, 10).until(lambda driver : url in self.driver.current_url)
		except TimeoutException:
			self.log.write('error', 'error on page: timeout or some divs missing')
			return False

		return self.check_page()
	


	def check_div(self, div_id):
		try:
			div = self.driver.find_element_by_id(div_id)
			self.log.write('debug', 'found div id='+div_id)
			self.log.write('debug', 'its content follows: '+div.text)
		except NoSuchElementException:
			self.log.write('error', 'no such div id='+div_id)
			return False

		return True
	
	def do_login(self, foreign=False):
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

def get_browser(browser, proxy_host=None, proxy_port=None):
	"""
	doesn't work with chrome
	"""
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

