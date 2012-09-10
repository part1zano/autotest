#!/usr/bin/env python
# -*- coding: utf-8 -*-

from logger import Log
import time,ConfigParser,codecs,re,json,getopt,sys,os.path
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,NoSuchElementException,WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

def get_browser(browser, proxy_host='', proxy_port=''):
	if proxy_port == '':
		proxy_port = 8090
	if browser == 'firefox':
		if proxy_host == '':
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
		options,operands = getopt.getopt(sys.argv[1:], 'bclu:d', ['browser=', 'config=', 'level=', 'url='])
		defaultCfg = True
		for name, value in options:
			if (name == '-c') or (name == '--config'):
				if os.path.exists(value):
					config = value
					defaultCfg = False
		
		self.log = Log(config)
		cnf = ConfigParser.ConfigParser()
		cnf.read(config)

		self.login = cnf.get('net-creds', 'login')
		self.password = cnf.get('net-creds', 'passwd')
		self.url = cnf.get('net-creds', 'server')
		self.browser = cnf.get('browser', 'browser')
		self.proxy_host = cnf.get('proxy', 'proxy_host')
		self.proxy_port = cnf.get('proxy', 'proxy_port')

		for name, value in options:
			if name == '-d':
				self.log.level = 'debug'
			elif (name == '-u') or (name == '--url'):
				self.url = value or self.url
			elif (name == '-b') or (name == '--browser'):
				self.browser = value or self.browser
			elif (name == '-l') or (name == '--level'):
				self.log.level = value or self.log.level

		self.log.write('debug', 'starting instance with parameters:')
		self.log.write('debug', 'config: %s' % config)
		self.log.write('debug', 'login: %s' % self.login)
		self.log.write('debug', 'password: %s' % self.password)
		self.log.write('debug', 'url: %s' % self.url)
		self.log.write('debug', 'browser: %s' % self.browser)
		self.log.write('debug', 'proxy_host: %s' % self.proxy_host)
		self.log.write('debug', 'proxy_port: %s' % self.proxy_port)

		self.driver = get_browser(self.browser) # FIXME :: proxy
		self.driver.get(self.url)
		self.links = []
		self.edits = []
		self.results = []
		self.errors = []
		self.info = {}

	def find_stuff(self, stuff):
		try:
			search = self.driver.find_element_by_name('q')
		except NoSuchElementException:
			self.log.write('error', 'no search form, aborting right now')
			return False
		search.clear()
		search.send_keys(stuff)
		search.submit()
		try:
			WebDriverWait(self.driver, 10).until(lambda driver : self.check_div('global-search-result'))
		except TimeoutException:
			self.log.write('error', 'timeout waiting for shit to load')
			return False

		return True

	def move_to(self, elem, by='id'):
		try:
			if by == 'id':
				obj = self.driver.find_element_by_id(elem)
			elif by == 'text':
				obj = self.driver.find_element_by_partial_link_text(elem)
			elif by == 'xpath':
				obj = self.driver.find_element_by_xpath(elem)
			else:
				self.log.write('error', 'unknown search criteria: by %s' % by)
				return False
		except NoSuchElementException:
			self.log.write('error', 'no such element %s' % elem)
			return False
	
		hover = ActionChains(self.driver).move_to_element(obj)
		hover.perform()
		return True

	def cut_string(self, string):
		if (len(string) > 20) and ('http' not in string):
			return string[:18]+'...'
		else:
			return string

	def find_link(self, link, by='id', count=1):
		try:
			if by == 'text':
				link_ = self.driver.find_elements_by_partial_link_text(link)
				if len(link_) < count:
					self.log.write('error', 'found only %2d elements, NOK' % len(link_))
					return False
			elif by == 'id':
				if count > 1:
					self.log.write('warning', 'searching by id returns only one element. always.')
				link = self.driver.find_element_by_id(link)
			else:
				self.log.write('error', 'unknown search criteria: '+by)
				return False
			return True
		except NoSuchElementException:
			self.log.write('error', 'no link: '+link)
			return False

	def get_our_info(self, field):
		links = {'mc_sidebar_profile': 'news', 'link_profile': 'profile'}
		for link, url in links.items():
			if not self.visit_link(link, url, by='id'):
				return None
		if field == 'id':
			toReturn = self.driver.current_url.split('/')[3]
			return toReturn
		elif field == 'url':
			toReturn = self.driver.current_url
			return toReturn
		try:
			field_ = self.driver.find_element_by_id(field)
		except NoSuchElementException:
			self.log.write('error', 'no such field')
			self.go(url)
			return None

		toReturn = field_.text
		return toReturn


	def make_json_list(self, json_file):
		json_fh = codecs.open(json_file, encoding='utf-8')
		to_return = json.load(json_fh)
		json_fh.close()
		return to_return

	def execute(self):
		if not self.do_login():
			self.log.write('error', 'login failed, see above')
			return False
		return True

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
			WebDriverWait(self.driver, 10).until(lambda driver : u'news' in self.driver.current_url)
			self.log.write('debug', 'logged in, visited profile')
		except TimeoutException:
			self.log.write('error', 'timeout waiting for shit to load')
			return False

		self.sleep(2)

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

	def logout(self):
		if not self.click_btn(u'Выйти'):
			self.log.write('error', 'logout button not found')
			return False

		self.log.write('debug', 'clicked logout btn')

		try:
			WebDriverWait(self.driver, 10).until(lambda driver : 'profile' not in self.driver.current_url)
		except TimeoutException:
			self.log.write('error', 'timeout trying to log out')
			return False

		self.log.write('info', 'logout ok')

		return True

	def check_page(self):
		divs = ['content']
		if 'feedback' in self.driver.current_url:
			divs.append('feedback')
		else:
			divs.append('tabs_container')
			divs.append('tabs')
			divs.append('left-sidebar')
			emp_header = False
			for substr in ('chat', 'news-feed', 'subscr'):
				if substr in self.driver.current_url:
					emp_header = True
			if emp_header:
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

		self.log.write('debug', 'found div id='+divname)
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
	
	def dedit(self, control):
		return self.edit_control(control['name'], control['value'], ctl_type=control['type'], clear=bool(int(control['clear'])))

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
				new_value=value
			else:
				new_value=old_value+value

			ctl.send_keys(value)
			self.log.write('debug', 'sent '+value+' into '+control+' control')

			return (ctl.get_attribute('value').lower() == new_value.lower()) # FIXME dog-nail for fckn selenium
		elif ctl_type == 'popup':
			self.log.write('debug', control+' is a popup or so')

			try:
				all_options = ctl.find_elements_by_name('option')
			except NoSuchElementException:
				self.log.write('warning', control+' has no options')
				return False
			clicked = False
			for option in all_options:
				self.log.write('debug', control+': found option '+option.get_attribute('value'))
				if value in option.get_attribute('value'):
					option.click()
					self.log.write('debug', control+': clicked '+option.get_attribute('value'))
					clicked = True
			return clicked

		else:
			self.log.write('error', control+': unknown ctl type')
			return False

	def edit_all_controls(self, submit=u'Сохранить'):
		for edit in self.edits:
			if not self.edit_control(edit['name'], edit['value'], clear=bool(int(edit['clear'])), ctl_type=edit['type']):
				self.log.write('error', 'control '+edit['name']+' edit failed, see above')
				return False

			self.log.write('info', '%s edited successfully' % edit['name'])

			if bool(int(edit['submit'])):
				if not self.click_btn(submit):
					self.log.write('error', 'some shit submitting, see above')
					return False

				self.log.write('info', 'clicked submit with editing %s' % edit['name'])

		return True

	def check_div_value(self, div, value, condition=True):
		try:
			div_ = self.driver.find_element_by_id(div)
		except NoSuchElementException:
			self.log.write('error', 'no such div')
			return False

		if (value in div_.text) != condition:
			self.log.write('error', 'no '+value+' in '+div)
			self.log.write('error', 'div text follows: '+div_.text)
			return False

		return True

	def get_value(self, control):
		try:
			ctl = self.driver.find_element_by_id(control)
		except NoSuchElementException:
			self.log.write('error', 'no such element '+control)
			return None

		if ctl.get_attribute('value') is not None:
			return ctl.get_attribute('value')
		else:
			return ctl.text

	def click_btn(self, btn_text):
		clicked = False
		try:
			btns = self.driver.find_elements_by_partial_link_text(btn_text)
		except NoSuchElementException:
			self.log.write('error', 'no submit btn: '+btn_text)
			self.log.write('error', 'no submit btn!')
			return False

		for btn in btns:
			btn.click()
			clicked = True
			self.log.write('debug', 'clicked button')
			self.log.write('debug', 'clicked '+btn_text)

		return clicked

	def check_single_result(self, index, method='equal'):
		self.log.write('debug', 'trying to find field '+self.results[index]['name']+' for check...')
		try:
			res = self.driver.find_element_by_id(self.results[index]['name'])
		except NoSuchElementException:
			self.log.write('error', 'no such field: '+self.results[index]['name'])
			return False

		if method == 'equal':
			found = res.text.lower() == self.results[index]['value'].lower()
		elif method == 'grep':
			found = self.results[index]['value'].lower() in res.text.lower()
		else:
			self.log.write('error', 'unknown comparison method for '+self.results[index]['name'])
			return False

		if not found:
			self.log.write('error', self.results[index]['name']+' values dont match: NOK')
			self.log.write('error', 'value is: '+res.text)
			self.log.write('error', 'should contain: '+self.results[index]['value'])
		
		return found

	def check_results(self, method='equal'):
		for index in range(len(self.results)):
			if not self.check_single_result(index, method):
				self.log.write('error', 'error checking '+self.results[index]['name'])
				return False

		return True
		
	def visit_dlink(self, link, sleep=False):
		return self.visit_link(link['link'], link['url'], link['by'], sleep)
	
	def visit_plink(self, link, url, by='text'):
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
			self.log.write('error', 'timeout waiting for shit to load or no '+url+' in cureent_url')
			return False

		return True

	def get_xpath_text(self, xpath):
		try:
			xpath = self.driver.find_element_by_xpath(xpath)
			return xpath.text
		except NoSuchElementException:
			self.log.write('error', 'no such xpath: '+xpath)
			return None

	def visit_link(self, link, url, by='id', sleep=False):
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
			self.log.write('error', 'timeout waiting for shit to load or no '+url+' in cureent_url')
			return False

		self.log.write('info', 'got to '+url+', checkin divs')
		if sleep:
			self.sleep(2)
		return self.check_page()

	def check_error(self, name, value, ok):
		if name != '':
			try:
				if 'informer-text' in name:
					err = self.driver.find_element_by_id(name)
					errval = err.text
				elif 'error-text' in name:
					err = self.driver.find_element_by_name(name)
					errval = err.get_attribute('value')
				else:
					self.log.write('error', 'wrong informer name: '+name+', unknown search criteria')
					return False
			except NoSuchElementException:
				self.log.write('error', 'no such error elem: '+name)
				return False

			if value not in errval: 
				self.log.write('error', name+' has wrong error message')
				self.log.write('error', 'it should contain: '+value)
				self.log.write('error', 'but it is: '+err.get_attribute('value'))
				return False
		if bool(int(ok)):
			return self.click_oks()

		return True

	def click_oks(self):
		clicked = False
		for ok in ['OK', u'ОК']:
			try:
				self.driver.find_element_by_partial_link_text(ok).click()
				clicked = True
			except NoSuchElementException:
				self.log.write('warning', 'no '+ok+' button')

		return clicked


