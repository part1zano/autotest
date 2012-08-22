#!/usr/bin/env python
# -*- coding: utf-8 -*-

from testlib import logger,functions

import string,sys,ConfigParser,codecs,re,time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,NoSuchElementException,WebDriverException
from selenium.webdriver.support.ui import WebDriverWait

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
links = {
		'link_settings' : 'settings', 
		'link_additional_settings' : 'additional-settings', 
		'link_change_password' : 'change-password'
		}

for linktext, url in links.items():
	if not functions.find_link_by_id_and_click(driver, linktext, url):
		log.write('error', 'error visiting '+url+', see above')
		driver.close()
		sys.exit(1)

	log.write('info', 'visited '+url)
	log.write('debug', 'visited '+url+' by clicking '+linktext)

	divname = url
	if 'additional' in divname:
		divname = re.sub('-', '_', divname)

	if not functions.check_div(driver, divname):
		log.write('error', 'div id='+divname+' not found, see above')
		driver.close()
		sys.exit(1)

	log.write('info', 'found div id='+divname)


log.write('info', 'test PASSED')
driver.close()
sys.exit(0)

