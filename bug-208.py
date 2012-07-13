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

driver = webdriver.Firefox()
driver.get(server)

if not functions.login(driver, login, passwd):
	log.write('error', 'failed to login: see above')
	driver.close()
	sys.exit(1)

log.write('info', 'login ok')

try:
	search = driver.find_element_by_name('q')
	log.write('debug', 'found search form')
except NoSuchElementException:
	log.write('error', 'no search form or wrong name')
	driver.close()
	sys.exit(1)

search.send_keys(u'™')
search.commit()
try:
	WebDriverWait(driver, 10).until(lambda driver : '™' in driver.current_url)
except TimeoutException:
	log.write('error', 'timeout waiting for shit to load')
	driver.close()
	sys.exit(1)

log.write('debug', 'got to search results')

links = {u'™' : 'profile', u'Написать сообщение' : 'dialog'}

for link, url in links.iteritems():
	log.write('debug', 'link: '+link+'; url: '+url)
	if not functions.find_link_and_click(driver, link, url):
		log.write('error', 'no link')
		driver.close()
		sys.exit(1)

# now some check about where we are (TODO)

# got to msgs, now go back
driver.back()
try:
	WebDriverWait(driver, 10).until(lambda driver : 'profile' in driver.current_url)
except TimeoutException:
	log.write('error', 'timeout waiting for shit to load')
	driver.close()
	sys.exit(1)

try:
	div = driver.find_element_by_id('profile')
except NoSuchElementException:
	log.write('error', 'profile not loaded, lol')
	driver.close()
	sys.exit(1)

log.write('info', 'test PASSED')
driver.close()
sys.exit(0)
