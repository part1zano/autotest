#!/usr/bin/env python
# -*- coding: utf-8 -*-

from testlib import logger,functions

import string,sys,ConfigParser,codecs,re,time,stabledict,datetime
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
browser = cnf.get('browser', 'browser')

driver = functions.get_browser(browser)
driver.get(server)

if not functions.login(driver, login, passwd):
	log.write('error', 'failed to login: see above')
	driver.close()
	sys.exit(1)

log.write('info', 'login ok')

links = stabledict.StableDict(((u'рекомендации', 'our_proposers'), (u'Пригла', 'invite')))

for link_text, url in links.items():
	if not functions.find_link_and_click(driver, link_text, url):
		log.write('error', 'not going to '+link_text+' and url '+url+', see above')
		log.write('error', 'not going to '+url+', see above')
		driver.close()
		sys.exit(1)

log.write('info', 'finally in invites')

for line in objlist:
	if re.match('^#', line):
		continue

	line = line.rstrip()

	objname, value = line.split('~!~')

	if not functions.edit_control(driver, objname, value, 'text'):
		log.write('error', 'failed editing '+objname+', see above')
		driver.close()
		sys.exit(1)

	log.write('info', 'edited '+objname)
	if 'email' in objname: # FIXME :: dog-nail for further use
		email = value
for text in [u'Пригласить', u'Отправить']:
	try:
		submit = driver.find_element_by_partial_link_text(text)
	except NoSuchElementException:
		log.write('warning', 'no submit button or wrong link text: '+text)

try:
	submit.click()
except NameError:
	log.write('error', 'no submit button at all')
	driver.close()
	sys.exit(1)

log.write('debug', 'found and clicked submit-invite btn, sleeping for 2s')
time.sleep(2)
log.write('debug', 'woke up, continuing')
log.write('info', 'clicked submit')
for ok in [u'ОК', 'OK']:
	try:
		ok_btn = driver.find_element_by_partial_link_text(ok)
	except NoSuchElementException:
		log.write('warning', 'button '+ok+' not found')

try:
	ok_btn.click()
except NameError:
	log.write('error', 'possibly no ok button at all')
	driver.close()
	sys.exit(1)

log.write('info', 'clicked ok on informer')

try:
	div = driver.find_element_by_id('invites')
except NoSuchElementException:
	log.write('error', 'no invites div, thats really strange')
	driver.close()
	sys.exit(1)

matchstring = email+' - '+datetime.date.today().strftime('%d.%m.%Y')

if not (matchstring in div.text):
	log.write('error', 'email and inv date didnt appear')
	log.write('error', 'div text follows: '+div.text)
	log.write('error', 'matchstring is: '+matchstring)
	driver.close()
	sys.exit(1)

log.write('info', 'test PASSED')
driver.close()
sys.exit(0)

