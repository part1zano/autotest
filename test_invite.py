#!/usr/bin/env python
# -*- coding: utf-8 -*-

from testlib import logger,functions

import string,sys,ConfigParser,codecs,re,time,stabledict,datetime
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

objlists = []

for obj_file in ['invite-pos.conf', 'invite-neg-empty-email.conf', 'invite-neg-empty-msg.conf', 'invite-neg-reg-email.conf']:
	objfile = codecs.open('./objlists/invite/text/'+obj_file, encoding='utf-8')
	objlists.append(objfile.read())
	objfile.close()

driver = functions.get_browser(browser)
driver.get(server)

if not functions.login(driver, login, passwd):
	log.write('error', 'failed to login: see above')
	driver.close()
	sys.exit(1)

log.write('info', 'login ok')

links = stabledict.StableDict((('mc_sidebar_our_proposers', 'our_proposers'), ('link_invites', 'invite')))

our_bname = functions.get_our_info(driver, 'brandName')
our_id = functions.get_our_info(driver, 'id')

for link_text, url in links.items():
	if not functions.find_link_by_id_and_click(driver, link_text, url):
		log.write('error', 'not going to '+link_text+' and url '+url+', see above')
		log.write('error', 'not going to '+url+', see above')
		driver.close()
		sys.exit(1)

objlist_index = 0

msgs = ['', u'введите корректный адрес электронной почты', u'введите ваше сообщение', u'компания уже зарегистрирована']

log.write('info', 'finally in invites')
for objlist_str in objlists:
	objlist_str = objlist_str.rstrip()
	objlist = objlist_str.split("\n")
	for line in objlist:
		if re.match('^#', line):
			continue

		line = line.rstrip()

		objname, value = line.split('~!~')

		if (objlist_index == 3):
			value = login

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
	if (objlist_index == 0) or (objlist_index == 3):
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
		if objlist_index == 0:
			matchstring = email+u' - Отправлено '+datetime.date.today().strftime('%d.%m.%Y')

			if not (matchstring in div.text):
				log.write('error', 'email and inv date didnt appear')
				log.write('error', 'div text follows: '+div.text)
				log.write('error', 'matchstring is: '+matchstring)
				driver.close()
				sys.exit(1)
	else:
		try:
			info = driver.find_element_by_id('informer-text')
		except NoSuchElementException:
			log.write('error', 'case '+str(objlist_index)+' no informer')
			driver.close()
			sys.exit(1)
		
		if not (msgs[objlist_index] in info.text):
			log.write('error', 'wrong informer text for case '+str(objlist_index))
			log.write('error', 'it should contain: '+msgs[objlist_index])
			log.write('error', 'but doesnt')
			driver.close()
			sys.exit(1)

	log.write('info', 'case '+str(objlist_index)+' ok')

	objlist_index += 1
	driver.get(driver.current_url)

log.write('info', 'test PASSED')
driver.close()
sys.exit(0)

