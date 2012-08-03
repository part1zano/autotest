#!/usr/bin/env python
# -*- coding: utf-8 -*-

from testlib import logger,functions

import sys,ConfigParser,codecs,re,time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,NoSuchElementException,WebDriverException
from selenium.webdriver.support.ui import WebDriverWait

passwd_objlists = []

for passwd_file in ['change-passwd-pos.conf', 'change-passwd-neg-1wrong.conf', 'change-passwd-neg-nomatch.conf', 'change-passwd-afterall.conf']:
	passwd_objfile = codecs.open('./objlists/change-passwd/text/'+passwd_file, encoding='utf-8')
	passwd_objlists.append(passwd_objfile.read())
	passwd_objfile.close()

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

if not functions.find_link_and_click(driver, u'Настройки', 'settings'):
	log.write('error', 'failed to visit settings, see above')
	driver.close()
	sys.exit(1)

log.write('debug', 'in settings, what to do?')

try:
	driver.find_element_by_partial_link_text('Пароль').click()
	log.write('debug', 'password link clicked')
except NoSuchElementException:
	log.write('error', 'no password link or wrong link text')
	driver.close()
	sys.exit(1)

objlist_index = 0
failed = False

msgs = [u'успешно', u'неправильный', u'не совпадает', u'успешно']

for passwd_objects in passwd_objlists:
	passwd_objects = passwd_objects.rstrip()
	passwd_objlist = passwd_objects.split("\n")
	for passwd_obj in passwd_objlist:
		if re.match('^#', passwd_obj):
			continue

		passwd_obj = passwd_obj.rstrip()
		objname, value = passwd_obj.split('~!~')
		
		if functions.edit_control(driver, objname, value, 'text'):
			log.write('debug', 'edited element '+objname+' successfully')
		else:
			log.write('error', 'failed editing '+objname+', see above')
			driver.close()
			sys.exit(1)
	
	try:
		driver.find_element_by_partial_link_text(u'Сохранить').click()
		log.write('debug', 'submit clicked')
	except NoSuchElementException:
		log.write('error', 'no submit button or wrong link text')
		driver.close()
		sys.exit(1)
	
	log.write('debug', 'sleeping for 2s to wait for shit to load')
	time.sleep(2)
	log.write('debug', 'woke up, will now chek da shit')
	if (objlist_index == 0) or (objlist_index == 3):
		try:
			msg = driver.find_element_by_id('informer-text')
		except NoSuchElementException:
			log.write('error', 'no informer')
			driver.close()
			sys.exit(1)

		txt = msg.text
	else:
		try:
			msg = find_element_by_name('error-text')
		except NoSuchElementException:
			log.write('error', 'no informer')
			driver.close()
			sys.exit(1)

		txt = msg.get_attribute('value')
	
	log.write('debug', 'found informer, lets see what it says...')
	
	try:
		if msgs[objlist_index] in txt:
			log.write('debug', 'case '+str(objlist_index)+' informer value OK')
		else:
			log.write('error', 'case '+str(objlist_index)+' informer value NOK')
			log.write('error', 'it is: '+txt+', while it should be: '+msgs[objlist_index])
			driver.close()
			sys.exit(1)
	except IndexError:
		log.write('warning', 'something is wrong with objlist or msgs: you should fix that')

	objlist_index += 1
	driver.get(driver.current_url)


log.write('info', 'test PASSED')
driver.close()
sys.exit(0)
