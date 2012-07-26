#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
#import testlib.logger, testlib.functions
from testlib import functions,logger
import sys,ConfigParser

cnf = ConfigParser.ConfigParser()
cnf.read('tests.conf')
hostname = cnf.get('net-creds', 'server')
username = cnf.get('net-creds', 'login')
password = cnf.get('net-creds', 'passwd')
browser = cnf.get('browser', 'browser')

log = logger.Log('tests.conf')

driver = functions.get_browser(browser)
driver.get(hostname)

if u'profile' in driver.current_url:
	log.write('info', 'already logged in')
else:
	log.write('info', 'not logged in; logging in')
	if functions.login(driver, username, password):
		log.write('info','login ok')
	else:
		log.write('error', 'login failed, exiting')
		driver.close()
		sys.exit(1)

log.write('info', 'logged in, logging out')

if not functions.logout(driver):
	log.write('error', 'logout failed: see above')
	driver.close()
	sys.exit(1)
	
log.write('info', 'logged out ok')
log.write('info', 'test PASSED')
driver.close()
sys.exit(0)
