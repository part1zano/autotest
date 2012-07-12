#!/usr/bin/env python
# -*- coding: utf-8 -*-

from testlib import logger,functions

import string,sys,ConfigParser,codecs,re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,NoSuchElementException,WebDriverException
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

driver = webdriver.Firefox()
driver.get(server)

if not functions.login(driver, login, passwd):
	log.write('error', 'login failed')
	driver.close()
	sys.exit(1)

log.write('info', 'login ok')
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
	val_list.append(objName+'~!~'+functions.get_value(driver,objName)+value)
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

for val in val_list:
	if re.match('^#', val):
		continue

	val = val.rstrip()
	objName, value = val.split('~!~')

	if functions.check_value(driver, objName, value):
		log.write('debug', 'element '+objName+' has the required value')
	else:
		log.write('warning', 'wrong text of '+objName+', see above')
		driver.close()
		sys.exit(1)

log.write('info', 'finished ok')
log.write('info', 'test PASSED')
driver.close()
sys.exit(0)

