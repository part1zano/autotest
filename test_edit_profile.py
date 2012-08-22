#!/usr/bin/env python
# -*- coding: utf-8 -*-

from testlib import logger,functions

import string,sys,ConfigParser,codecs,re,time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,NoSuchElementException,WebDriverException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait

log = logger.Log('tests.conf')

objfile = codecs.open('./objlists/edit-profile/text/objlist-edit-profile.conf', encoding='utf-8')
objlist = objfile.readlines()
objfile.close()

cnf = ConfigParser.ConfigParser()
cnf.read('tests.conf')
server = cnf.get('net-creds', 'server')
login = cnf.get('net-creds', 'login')
passwd = cnf.get('net-creds', 'passwd')
browser = cnf.get('browser', 'browser')

driver = functions.get_browser(browser)
driver.get(server)

if not functions.login(driver, login, passwd):
	log.write('error', 'login failed')
	driver.close()
	sys.exit(1)

log.write('info', 'login ok')

if not functions.find_link_by_id_and_click('link_profile', 'profile'):
	log.write('error', 'some shit with profile link, see above')
	driver.close()
	sys.exit(1)

try:
	driver.find_element_by_partial_link_text(u'Редактировать').click()
except NoSuchElementException:
	log.write('error', 'no edit button, wrong link text or wrong page')
	driver.close()
	sys.exit(1)

log.write('debug', 'in settings, trying to edit them')

val_list = []

for obj in objlist:
	if re.match('^#', obj):
		continue

	obj = obj.rstrip()
	objName, value = obj.split('~!~')
	if 'estYear' in objName:
		if not functions.clear_element(driver, objName):
			log.write('error', 'clearing estYear failed: see above')
			driver.close()
			sys.exit(1)
		
	new_value = functions.get_value(driver, objName)+value
#	if 'bank_account' in objName:
#		val_list.append(re.sub('bank_account', 'essentialElements', objName)+'~!~'+new_value)
#	else:
	val_list.append(objName+'~!~'+new_value)
	if functions.edit_control(driver, objName, value, 'text'):
		log.write('debug', 'element '+objName+' edited successfully')
	else:
		log.write('warning', 'unsuccessful edit of '+objName+', see above')
		driver.close()
		sys.exit(1)

try:
	driver.find_element_by_partial_link_text(u'Сохранить').click()
	log.write('info', 'submit clicked')
except NoSuchElementException:
	log.write('error', 'no submit button, wrong page or wrong link text')
	driver.close()
	sys.exit(1)

log.write('debug', 'clicked submit, sleeping for 2s')
time.sleep(2)
log.write('debug', 'woke up, will now check the shit')

for val in val_list:
	if re.match('^#', val):
		continue

	val = val.rstrip()
	objName, value = val.split('~!~')
	try:
		if functions.check_value(driver, objName, value):
			log.write('debug', 'element '+objName+' has the required value')
		else:
			log.write('error', 'wrong text of '+objName+', see above')
			driver.close()
			sys.exit(1)
	except StaleElementReferenceException:
		log.write('error', objName+' somewhy uncheckable')

log.write('info', 'finished ok')
log.write('info', 'test PASSED')
driver.close()
sys.exit(0)

