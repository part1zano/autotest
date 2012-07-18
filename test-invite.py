#!/usr/bin/env python
# -*- coding: utf-8 -*-

from testlib import logger,functions

import string,sys,ConfigParser,codecs,re,time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,NoSuchElementException,WebDriverException
from selenium.webdriver.support.ui import WebDriverWait

log = logger.Log('tests.conf')

objfile = codecs.open('./objlists/invite/text/invite.conf', encoding='utf-8')
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
	log.write('error', 'failed to login: see above')
	driver.close()
	sys.exit(1)

log.write('info', 'login ok')

links = {u'рекомендации' : 'our_proposers', u'Пригла' : 'invite'}

for link_text, url in links.iteritems():
	if not functions.find_link_and_click(driver, link_text, url):
		log.write('error', 'not going to '+link_text+' and url '+url+', see above')
		driver.close()
		sys.exit(1)

log.write('debug', 'finally in invites')

for line in objlist:
	if re.match('^#', line):
		continue

	line = line.rstrip()

	objname, value = line.split('~!~')

	if not functions.edit_control(driver, objname, value, 'text'):
		log.write('error', 'failed editing '+objname+', see above')
		driver.close()
		sys.exit(1)

try:
	driver.find_element_by_partial_link_text(u'Пригласить').click()
except NoSuchElementException:
	log.write('error', 'no submit button or wrong link text')
	driver.close()
	sys.exit(1)

log.write('debug', 'found and clicked submit-invite btn, sleeping for 2s')
time.sleep(2)
log.write('debug', 'woke up, continuing')

for ok in [u'ОК', 'OK']:
	try:
		driver.find_element_by_partial_link_text(ok).click()
		log.write('info', 'test PASSED')
		driver.close()
		sys.exit(0)
	except NoSuchElementException:
		log.write('warning', 'button '+ok+' not found')

log.write('error', 'possibly no ok button at all')
log.write('info', 'test FAILED')
driver.close()
sys.exit(1)

