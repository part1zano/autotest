#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
import time,sys,string,codecs
import testlib.logger
import ConfigParser

def login(driver, loginstr, passwordstr):
	logins = driver.find_elements_by_name('username')
	for login in logins:
		login.send_keys(loginstr)
	
	passwords = driver.find_elements_by_name('password')
	for password in passwords:
		password.send_keys(passwordstr)

	driver.find_element_by_name('login').click()

	try:
		WebDriverWait(driver, 10).until(lambda driver : u'profile' in driver.current_url)

		for cookie in driver.get_cookies():
			if (u'sessionid' in string.lower(cookie['name'])):
				return True
			return False

	except TimeoutException:
		log.write('error', 'timeout waiting for shit to load')
		return False

def edit_controls(driver, objfname):
	ourfile = codecs.open(objfname, encoding='utf-8')

	objlist = ourfile.readlines()
	ourfile.close()

	for objstr in objlist:

		obj, value = objstr.split('~!~')
		try:
			control = driver.find_element_by_id(obj)
		except NoSuchElementException:
			log.write('warning', 'no such element ('+obj+') in form '+objfname)
			continue
		if u'text' in objfname:
			control.send_keys(value)
			old_value = control.get_attribute('value')
#			driver.execute_script('document.getElementById("'+obj+'").value="'+old_value+value.rstrip()+'"')
		elif u'popup' in objfname:
			all_options = control.find_elements_by_tag_name('option');
			for option in all_options:
				log.write('info', 'found value '+option.get_attribute('value')+' in '+obj)
				if value in option.get_attribute('value'):
					option.click()
		else:
			log.write('warning', 'the type of control selected is currently unavailable')
			continue

		try:
			objname = driver.find_element_by_id(obj)
		except NoSuchElementException:
			log.write('error', 'No '+obj+' field in html')
			return 1
		log.write('info', obj+' changed to ' + objname.text)
		if value in objname.text:
			log.write('info', 'profile unit '+objname+' changed successfully')
		else:
			log.write('error', 'profile unit '+objname+' changed to some shit')
			return 1
	return 0

log = testlib.logger.Log('tests.conf')
cfg = ConfigParser.ConfigParser()
cfg.read('tests.conf')
hostname = cfg.get('net-creds', 'server')
username = cfg.get('net-creds', 'login')
password = cfg.get('net-creds', 'passwd')

driver = webdriver.Firefox()
driver.get(hostname)

if u'profile' in driver.current_url:
	log.write('info', 'logged in')
else:
	log.write('info', 'not logged in: logging in')
	if login(driver, username, password):
		log.write('info', 'login ok')
	else:
		log.write('error', 'login failed, exiting')
		driver.close()
		sys.exit(1)
			
for edit_title in (u'Редактировать', u'Edit'):
	try:
		edit = driver.find_element_by_partial_link_text(edit_title)
	except NoSuchElementException:
		continue

try:
	edit.click()
	log.write('info', 'editing profile...')
	edit_controls(driver, './objlists/edit-profile/text/objlist-edit-profile.conf')
	try:
		submit = driver.find_element_by_partial_link_text(u'Сохранить')
		submit.click()
		log.write('info', 'info edited successfully')
		driver.close()
	except NoSuchElementExpception:
		log.write('error', 'no submit button!')
		driver.close()
		sys.exit(1)

except NameError:
	log.write('error', 'no edit button!')
	driver.close()
	sys.exit(1)
