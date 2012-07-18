#!/usr/bin/env python
# -*- coding: utf-8 -*-

from testlib import logger,functions

import string,sys,ConfigParser,codecs,re,time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,NoSuchElementException,WebDriverException
from selenium.webdriver.support.ui import WebDriverWait

objfile = codecs.open('objlists/edit-contacts/text/objlist-edit-contacts.conf', encoding='utf-8')
objlist = objfile.readlines()
objfile.close()

log = logger.Log('tests.conf')

cnf = ConfigParser.ConfigParser()
cnf.read('tests.conf')
server = cnf.get('net-creds', 'server')
login = cnf.get('net-creds', 'login')
passwd = cnf.get('net-creds', 'passwd')

driver = webdriver.Firefox()
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

if not functions.check_div(driver, 'feedback'):
	log.write('error', 'no feedback div')
	driver.close()
	sys.exit(1)

log.write('info', 'feedback div found')

if not functions.edit_control(driver, 'feedback-message', 'This is just a test msg', 'text'):
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

for text in ['OK', u'ОК']:
	try:
		driver.find_element_by_partial_link_text(text).click()
		log.write('info', 'ok on informer clicked')
		log.write('info', 'test PASSED')
		driver.close()
		sys.exit(0)
	except NoSuchElementException:
		log.write('warning', 'no '+text+' button')

log.write('error', 'no ok button on informer or no informer')
driver.close()
sys.exit(1)
