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
	log.write('error', 'failed to login, see above')
	driver.close()
	sys.exit(1)

log.write('info', 'login ok')
for cond in [True, False]:
	driver.get(server)
	if not functions.recommend_by_title(driver, 'Kaya', cond):
		log.write('error', 'failed recommending company, see above')
		driver.close()
		sys.exit(1)


log.write('info', 'test PASSED')
driver.close()
sys.exit(0)
