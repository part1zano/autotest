#!/usr/bin/env python
# -*- coding: utf-8 -*-

from logger import Log
import time,ConfigParser,codecs,re,json,getopt,sys,os.path
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,NoSuchElementException,WebDriverException,StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.command import Command
from selenium.webdriver.common.keys import Keys

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
		'''
			Class constructor, takes config filename. Also checks command-line parameters:
			-b, --browser
			-c, --config
			-l, --level
			-u, --url
			-d, --debug -- takes no parameter, sets log level to debug
		'''
		options,operands = getopt.getopt(sys.argv[1:], 'b:c:l:u:d', ['browser=', 'config=', 'level=', 'url=', 'debug'])
		for name, value in options:
			if name in ('-c', '--config'):
				if os.path.exists(value):
					config = value
		
		self.log = Log(config)
		cnf = ConfigParser.ConfigParser()
		cnf.read(config)

		self.login = cnf.get('net-creds', 'login')
		self.password = cnf.get('net-creds', 'passwd')
		self.url = cnf.get('net-creds', 'server')
		self.browser = cnf.get('browser', 'browser')
		self.proxy_host = cnf.get('proxy', 'proxy_host')
		self.proxy_port = cnf.get('proxy', 'proxy_port')
		self.aslogin = cnf.get('user2', 'login')
		self.aspwd = cnf.get('user2', 'passwd')

		for name, value in options:
			value = value.strip()
			if name in ('-d', '--debug'):
				self.log.level = 'debug'
			elif name in ('-u', '--url'):
				self.url = value or self.url
			elif name in ('-b', '--browser'):
				self.browser = value or self.browser
			elif name in ('-l', '--level'):
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
		self.log.write('debug', 'initialized self.links')
		self.edits = []
		self.log.write('debug', 'initialized self.edits')
		self.results = []
		self.log.write('debug', 'initialized self.results')
		self.errors = []
		self.log.write('debug', 'initialized self.errors')
		self.info = {}
		self.log.write('debug', 'initialized self.info')

	def find_stuff(self, stuff):
		'''
		Finds something using the site's search engine. Takes a text fragment to search for
		'''
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

	def json_info(self, id_=None, entity='person'):
		'''
		Takes the site's json info (aka common_data), takes id_ of entity and entity type ('person' or 'company')
		'''
		url = self.driver.current_url
		if id_ is None:
			self.go('%s/settings/s' % self.url)
		elif entity == 'company':
			self.go('%s/profile/i/%s' % (self.url, id_))
		elif entity == 'person':
			self.go('%s/person/%s/s' % (self.url, id_))
		else:
			return None
		
		text = self.get_value('//pre', by='xpath')
		self.go(url)
		return json.loads(text)

	def find_dict_in(self, where, name, value):
		'''
		Finds a name:value in where, which is a list of dicts
		'''
		for elem in where:
			try:
				if elem[name] == value:
					return elem
			except KeyError:
				self.log.write('error', 'KeyError: no %s in list element' % name)
				return {}
		return {}

	def click_btn_in_xpath(self, xpath, btn=u'Поделиться'):
		'''
		Clicks a btn in an xpath; returns True if everything is ok
		'''
		try:
			table = self.driver.find_element_by_xpath(xpath)
		except NoSuchElementException:
			self.log.write('error', 'no such table or wrong xpath: %s' % xpath)
			return False

		try:
			table.find_element_by_partial_link_text(btn).click()
		except NoSuchElementException:
			self.log.write('warning', 'no such button in table')
			self.log.write('warning', 'btn text is %s' % btn)
			return False

		return True

	def move_to(self, elem, by='id'):
		'''
		Moves cursor to an element, returns True if ok. Takes elem description and search criteria: 'id', 'text', 'xpath'.
		By default, by='id'
		'''
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
	
#		hover = ActionChains(self.driver).move_to_element(obj)
#		hover.perform()
		
		result = self.driver.execute(Command.MOVE_TO, {'element': obj.id})
		if result['status'] == 0:
			return True
		else:
			self.log.write('error', 'move_to failed: %s' % result['value']['message'])
			return False

#	def cut_string(self, string, length = 20):
#		if (len(string) > length) and ('http' not in string):
#			self.log.write('debug', 'cut %s to %2d chars, got %s' % (string, length, string[:(length-2)]))
#			return string[:(length-2)]
#		else:
#			return string

	def find_link(self, link, by='id', count=1):
		'''
		Finds a link without clicking it, can find multiple links. Takes link description, 'by' parameter and count of links to find
		'''
		try:
			if by == 'text':
				link_ = self.driver.find_elements_by_partial_link_text(link)
				if len(link_) < count:
					self.log.write('debug', 'found only %2d elements, NOK: must be %2d' % (len(link_), count))
					return False
			elif by == 'id':
				if count > 1:
					self.log.write('warning', 'searching by id returns only one element. always.')
				link = self.driver.find_element_by_id(link)
			elif by == 'xpath':
				link_ = self.driver.find_elements_by_xpath(link)
				if len(link_) < count:
					self.log.write('error', 'found only %2d elements (must be %2d)' % (len(link_), count))
					return False
			else:
				self.log.write('error', 'unknown search criteria: '+by)
				return False
			return True
		except NoSuchElementException:
			self.log.write('error', 'no link: '+link)
			return False

	
	def make_json_list(self, json_file):
		'''
		Reads a specified json_file, returns a data structure from it.
		'''
		json_fh = codecs.open(json_file, encoding='utf-8')
		to_return = json.load(json_fh)
		json_fh.close()
		return to_return

	def execute(self):
		'''
		Executes test, In this particular case, just logs on and returns True if ok
		'''
		if not self.do_login():
			self.log.write('error', 'login failed, see above')
			return False
		return True

	def __del__(self):
		'''
		Destructor. Quits browser.
		'''
		if self.browser == 'firefox':
			self.driver.quit()
		else:
			self.driver.close()

	def sleep(self, time_):
		'''
		A wrapper for time.sleep. Sleeps for a period of time_
		'''
		self.log.write('debug', 'sleepin for '+str(time_)+'s')
		time.sleep(time_)
		self.log.write('debug', 'woke up after sleep, next...')

	def go(self, url):
		'''
		Visits a specified url, waits until url is in self.driver.current_url
		'''
		if 'http' in url:
			self.driver.get(url)
		else:
			self.driver.get(self.url+'/'+url)

		try:
			WebDriverWait(self.driver, 10).until(lambda driver: url in self.driver.current_url)
		except TimeoutException:
			self.log.write('error', 'timeout waiting for shit to load while getting to %s' % url)
			return False

		return True

	def do_login(self, foreign=False):
		'''
		Logs in using self.login and self.password
		'''
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
				self.log.write('info', 'login ok')
				return True
		self.log.write('error', 'Cookies not ok')
		return False

	def logout(self):
		'''
		Logs the fuck out
		'''
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
		'''
		Checks the loaded web page for some basic divs. Uses check_div to find 'em
		'''
		logon = self.find_link(u'Выйти', by='text')
		divs = ['content']
		notabs = False
		for substr in ['q', 'feedback', 'search']:
			if substr in self.driver.current_url:
				notabs = True
		if notabs:
			if 'feedback' in self.driver.current_url:
				divs.append('feedback')
			else:
				divs.append('left-sidebar')
		else:
			divs.append('tabs_container')
			divs.append('tabs')
			divs.append('left-sidebar')
			emp_header = False
			for substr in ['chat', 'news-feed',  'person/', 'change-password', 'news-subscriptions', 'invite', 'settings']:
				if substr in self.driver.current_url:
					emp_header = True and logon

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
		'''
		Checks the web page for a single divname. Finds it by id only
		'''
		try:
			div = self.driver.find_element_by_id(divname)
		except NoSuchElementException:
			self.log.write('error', 'no such div id='+divname)
			return False

		self.log.write('debug', 'found div id='+divname)
#		self.log.write('debug', 'its content follows:'+div.text)
		return True
	
	def dedit(self, control):
		'''
		Edits a control specified by a dictionary:
		control = {'name': name, 'value': value, 'clear': clear}
		'''
		return self.edit_control(control['name'], control['value'], ctl_type=control['type'], clear=bool(int(control['clear'])))

	def edit_control(self, control, value, ctl_type='text', by='id', clear=False, click=False):
		'''
		Edits a specified control. 		'''
		if ctl_type == 'text':
			self.log.write('debug', control+' is a text input or so')
			try:
				if by == 'id':
					ctl = self.driver.find_element_by_id(control)
				elif by == 'name':
					ctl = self.driver.find_element_by_name(control)
				elif by == 'xpath':
					ctl = self.driver.find_element_by_xpath(control)
				else:
					self.log.write('error', 'unknown search criteria: by %s' % by)
					return False
			except NoSuchElementException:
				self.log.write('error', 'no such control %s="%s"' % (by, control))
				return False
			old_value = ctl.get_attribute('value')
			self.log.write('debug', control+' value is: '+old_value)
			if clear:
				ctl.clear()
				new_value=value
			else:
				new_value=old_value+value

			ctl.send_keys(value)
			self.log.write('debug', 'sent '+value+' into '+control+' control')

			if click:
				ctl.click()

			return (ctl.get_attribute('value').lower() == new_value.lower()) # FIXME dog-nail for fckn selenium
		elif ctl_type == 'popup':
			self.log.write('debug', control+' is a popup or so')
			
			try:
				ctl_container = self.driver.find_element_by_id('%s-container' % control)
			except NoSuchElementException:
				self.log.write('error', 'no container for popup %s' % control)
				return False

			try:
				ctl_container.find_element_by_xpath('//a[@class="selectBox selectBox-dropdown"]').click()
				#ctl_container.find_element_by_xpath('//a[@tabindex="0"]').click()
			except NoSuchElementException:
				self.log.write('error', 'error opening popup %s' % control)
				return False

			self.log.write('debug', 'clicked dropdown')
			self.sleep(2)

			if not self.click_btn(value, by='text'):#'//a[@rel="%s"]' % value, by='xpath'):
				self.log.write('error', 'error selecting/clicking option in popup %s' % control)
				return False

			self.sleep(2)
			self.log.write('debug', 'clicked value')
			
			return True
		elif ctl_type == 'checkbox': # checked -> true; not checked -> none
			self.log.write('debug', '%s is a checkbox or so' % control)
			try:
				chbox = self.driver.find_element_by_id(control)
			except NoSuchElementException:
				self.log.write('error', 'no such element %s' % control)
				return False

			try: # StaleElementException dog-nail
				value_was = chbox.get_attribute('checked')
			except StaleElementReferenceException:
				self.log.write('error', 'error getting previous value for %s, just inverting that shit' % control)
				value_was = not value

			if str(bool(value_was)).lower() == str(bool(value)).lower():
				self.log.write('warning', 'checkbox %s already has that value' % control)
			else:
				self.log.write('debug', 'inverting %s checkbox' % control)

				if not self.click_btn('//label[@for="%s"]' % control, by='xpath'):
					self.log.write('error', 'error inverting checkbox %s' % control)
					return False
				self.log.write('debug', 'inverted checkbox %s' % control)

			return True
				
		else:
			self.log.write('error', control+': unknown ctl type')
			return False

	def edit_all_controls(self, submit=u'Сохранить'):
		'''
		Edits all controls from self.edits, clicks submit. Submit text is a parameter
		'''
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

	def check_div_value(self, div, value, condition=True, by='id'):
		'''
		checks div for whether or not (defined by condition) value is in div, div is found by id or xpath
		'''
		try:
			if by == 'id':
				div_ = self.driver.find_element_by_id(div)
			elif by == 'xpath':
				div_ = self.driver.find_element_by_xpath(div)
		except NoSuchElementException:
			self.log.write('error', 'no such div')
			return False

		if (value in div_.text) != condition:
			self.log.write('error', 'no '+value+' in '+div)
			self.log.write('error', 'div text follows: '+div_.text)
			return False

		return True

	def get_value(self, control, by='id', ctl_type='text'):
		'''
		Gets value of control. 
		by = ('id' | 'xpath')
		ctl_type = ('text' | 'checkbox')
		'''
		try:
			if by == 'id':
				ctl = self.driver.find_element_by_id(control)
			elif by == 'xpath':
				ctl = self.driver.find_element_by_xpath(control)
		except NoSuchElementException:
			self.log.write('error', 'no such element '+control)
			return None

		if ctl_type == 'text':
			if ctl.get_attribute('value') is not None:
				return ctl.get_attribute('value')
			else:
				return ctl.text
		elif ctl_type == 'checkbox':
			return bool(ctl.get_attribute('checked'))

	def click_btn(self, btn_text, by='text'):
		'''
		clicks a btn, finds it by id, text (default) or xpath
		'''
		clicked = False
		try:
			if by == 'text':
				btns = self.driver.find_elements_by_partial_link_text(btn_text)
			elif by == 'xpath':
				btns = self.driver.find_elements_by_xpath(btn_text)
			elif by == 'id':
				btns = [self.driver.find_element_by_id(btn_text)]
			else:
				self.log.write('error', 'unknown search criteria: by %s' % by)
		except NoSuchElementException:
			self.log.write('error', 'no submit btn: '+btn_text)
			self.log.write('error', 'no submit btn!')
			return False

		if len(btns) == 0:
			self.log.write('error', 'no such btns!')
			return False

		for btn in btns:
			btn.click()
			clicked = True
			self.log.write('debug', 'clicked button')
			self.log.write('debug', 'clicked '+btn_text)

		return clicked

	def check_result(self, result, mustbe=True):
		'''
		Finds an element by id and checks whether some shit is in it
		result ({'name': name, 'value': value})
		'''
		self.log.write('debug', 'trying to find field '+result['name']+' for check...')
		try:
			res = self.driver.find_element_by_id(result['name'])
		except NoSuchElementException:
			self.log.write('error', 'no such field: '+result['name'])
			return False

		if result['method'] == 'equal':
			found = res.text.lower() == result['value'].lower()
			self.log.write('debug', 'method equal, found=%s' % str(found))
		elif result['method'] == 'grep':
			found = result['value'].lower() in res.text.lower()
			self.log.write('debug', 'method grep, found=%s' % str(found))
		else:
			self.log.write('error', 'unknown comparison method for '+result['name'])
			return False

		if not found:
			self.log.write('error', result['name']+' values dont match: NOK')
			self.log.write('error', 'value is: '+res.text)
			self.log.write('error', 'should contain: '+result['value'])
		
		return (found == mustbe)

	def check_results(self, mustbe=True):
		'''
		checks all results in self.results
		'''
		for result in self.results:
			if not self.check_result(result, mustbe):
				self.log.write('error', 'error checking '+result['name'])
				return False

		return True
		
	def visit_dlink(self, link, sleep=False):
		'''
		visits a link (see visit_link) specified by a dictionary: {'link': link, 'url': url, 'by': by}
		'''
		return self.visit_link(link['link'], link['url'], link['by'], sleep)
	
	def visit_plink(self, link, url, by='text'):
		'''
		visits a link without checking divs
		'''
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
		'''
		Gets text from a specified xpath element
		'''
		try:
			xpath = self.driver.find_element_by_xpath(xpath)
			return xpath.text
		except NoSuchElementException:
			self.log.write('error', 'no such xpath: '+xpath)
			return None

	def visit_link(self, link, url, by='id', sleep=False):
		'''
		visits a link, then checks divs. if ok, returns True
		by = ('id' | 'text' | 'xpath'), if not, return False
		sleep (=False) [!!] for Chrome, sleep should always be True
		'''
		try:
			if by == 'id':
				self.driver.find_element_by_id(link).click()
			elif by == 'text':
				self.driver.find_element_by_partial_link_text(link).click()
			elif by == 'xpath':
				self.driver.find_element_by_xpath(link).click()
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
		'''
		Checks an error element, returns True if ok
		
		ok is converted to int, then to bool
		'''
		if name != '':
			self.log.write('debug', 'name is not empty')
			try:
				if 'informer-text' in name:
					err = self.driver.find_element_by_id(name)
					errval = err.text
				elif 'error-text' in name:
					err = self.driver.find_element_by_name(name)
					errval = err.get_attribute('value')
				elif 'class' in name:
					err = self.driver.find_element_by_xpath(name)
					errval = err.text
				else:
					self.log.write('error', 'wrong informer name: '+name+', unknown search criteria')
					return False
			except NoSuchElementException:
				self.log.write('error', 'no such error elem: '+name)
				return False

			if value not in errval: 
				self.log.write('error', name+' has wrong error message')
				self.log.write('error', 'it should contain: '+value)
				self.log.write('error', 'but it is: '+errval)
				return False
		self.log.write('debug', 'clicking oks')
		if bool(int(ok)):
			return self.click_oks()

		return True

	def click_oks(self):
		'''
		Clicks all 'OK' btns, be they latin or cyrillic
		'''
		clicked = False
		for ok in ['OK', u'ОК']:
			self.log.write('debug', 'clicking oks pass some')
			clicked = self.click_btn(ok)

		return clicked


