#!/usr/bin/env python
# -*- coding: utf-8 -*-

from testlib import logger,functions

import string,sys,ConfigParser,codecs,re,time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,NoSuchElementException,WebDriverException
from selenium.webdriver.support.ui import WebDriverWait

msgs = ['This is just a test msg', '']

log = logger.Log('tests.conf')

cnf = ConfigParser.ConfigParser()
cnf.read('tests.conf')
server = cnf.get('net-creds', 'server')
login = cnf.get('net-creds', 'login')
passwd = cnf.get('net-creds', 'passwd')
browser = cnf.get('browser', 'browser')

driver = functions.get_browser(browser)
driver.get(server)

if not functions.login(driver, login, passwd):
	log.write('error', 'failed to login: see above')
	driver.close()
	sys.exit(1)

log.write('info', 'login ok')

if not functions.find_link_and_click(driver, u'Обратная связь', 'feedback'):
	log.write('error', 'no feedback link or wrong link/url text')
	driver.close()
	sys.exit(1)

log.write('info', 'feedback link found and clicked')

for msg in msgs:
	if not functions.check_div(driver, 'feedback'):
		log.write('error', 'no feedback div')
		driver.close()
		sys.exit(1)

	log.write('info', 'feedback div found')
	
	if not functions.edit_control(driver, 'feedback-message', msg, 'text'):
		log.write('error', 'failed to edit text area')
		driver.close()
		sys.exit(1)

	log.write('info', 'edited message text')

	if login not in functions.get_value(driver, 'feedback-email'):
		log.write('error', 'email not stated in email field')
		driver.close()
		sys.exit(1)
	
	try:
		driver.find_element_by_partial_link_text(u'Отправить').click()
	except NoSuchElementException:
		log.write('error', 'no submit button or wrong link text')
		driver.close()
		sys.exit(1)

	log.write('info', 'submit clicked')
	
	if bool(msg):
		for text in ['OK', u'ОК']:
			try:
				ok = driver.find_element_by_partial_link_text(text)
			except NoSuchElementException:
				log.write('warning', 'no '+text+' button')

		try:
			ok.click()
		except NameError:
			log.write('error', 'no ok button on informer or no informer')
			driver.close()
			sys.exit(1)
	else:
		try:
			info = driver.find_element_by_name('error-text')
		except NoSuchElementException:
			log.write('error', 'no error informer')
			driver.close()
			sys.exit(1)

		if u'не должно быть пустым' not in info.get_attribute('value'):
			log.write('error', 'error text wrong')
			log.write('error', 'it should contain an msg bout not empty, but doesnt')
			driver.close()
			sys.exit(1)

	driver.get(driver.current_url)

log.write('info', 'test PASSED')
driver.close()
sys.exit(0)
