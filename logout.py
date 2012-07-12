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

log = logger.Log('tests.conf')

driver = webdriver.Firefox()
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

try:
	driver.find_element_by_partial_link_text(u'Выйти').click()
	log.write('debug', 'found logout link and clicked it')
except NoSuchElementException:
	log.write('error', 'logout link not found')
	driver.close()
	sys.exit(1)


try:
	WebDriverWait(driver,10).until(lambda driver : u'profile' not in driver.current_url)
except TimeoutException:
	log.write('debug', 'timeout waiting for shit to load')
	driver.close()
	sys.exit(1)

log.write('info', 'logged out ok')
sys.exit(0)
