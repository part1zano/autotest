#!/usr/bin/env python
# -*- coding: utf-8 -*-

from testlib import logger,functions

import string,sys,ConfigParser,codecs,re
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
browser = cnf.get('browser', 'browser')

driver = functions.get_browser(browser)
driver.get(server)

if not functions.login(driver, login, passwd):
	log.write('error', 'failed to login: see above')
	driver.close()
	sys.exit(1)

log.write('info', 'login ok')

if not functions.find_link_and_click(driver, u'Контакты', 'contacts'):
	log.write('error', 'no contacts link, wrong link or some shit: see above')
	driver.close()
	sys.exit(1)

for line in objlist:
	if re.match('^#', line):
		continue

	line = line.rstrip()
	objname, value = line.split('~!~')

	try:
		driver.find_element_by_partial_link_text(u'Редактировать').click()
		log.write('debug', 'edit button clicked')
	except NoSuchElementException:
		log.write('error', 'no edit button or wrong link text')
		driver.close()
		sys.exit(1)

	if not functions.clear_element(driver, objname):
		log.write('error', 'failed clearing element '+objname+', see above')
		driver.close()
		sys.exit(1)
	log.write('debug', 'cleared elem '+objname)
	if not functions.edit_control(driver, objname, value, 'text'):
		log.write('error', 'edit of '+objname+' failed: see above')
		driver.close()
		sys.exit(1)
	log.write('info', 'element '+objname+' successfully edited')
	try:
		driver.find_element_by_partial_link_text(u'Сохранить').click()
		log.write('debug', 'submit clicked')
	except NoSuchElementException:
		log.write('error', 'no submit or wrong link text')
		driver.close()
		sys.exit(1)

	try:
		contacts_layer = driver.find_element_by_id('contacts')
		log.write('info', 'contacts layer found')
	except NoSuchElementException:
		log.write('error', 'no contacts layer or wrong id')
		driver.close()
		sys.exit(1)

	if value in contacts_layer.text:
		log.write('debug', 'found posted info in contacts div')
	else:
		log.write('error', 'contacts layer value NOK')
		log.write('error', 'value not found in contacts div, its text follows: '+contacts_layer.text)
		driver.close()
		sys.exit(1)


log.write('info', 'test PASSED')
driver.close()
sys.exit(0)

