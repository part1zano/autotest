#!/usr/bin/env python
# -*- coding: utf-8 -*-

from testlib import logger,functions

import string,sys,ConfigParser,codecs,re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,NoSuchElementException,WebDriverException
from selenium.webdriver.support.ui import WebDriverWait

log = logger.Log('tests.conf')

cnf = ConfigParser.ConfigParser()
cnf.read('tests.conf')
server = cnf.get('net-creds', 'server')
login = cnf.get('net-creds', 'login')
passwd = cnf.get('net-creds', 'passwd')

links = {
		'profile' : {
			'profile' : u'Наша компания', 
			'contacts' : u'Контакты'
			},
		'deposit' : {
			'deposit' : u'Депозит', 
			'deposit/topping-up' : u'Пополнить счет', 
			'deposit/payments' : u'Оплатить услуги'
			}, 
		'our_proposers': {
			'our_proposers' : u'Нас рекомендуют', 
			'we_recommend' : u'Мы рекомендуем', 
			'invites' : u'Приглашения'
			}, 
		'chat' : {
			'chat' : u'Мои диалоги'
			}
		}

driver = webdriver.Firefox()
driver.get(server)

if not functions.login(driver, login, passwd):
	log.write('error', 'failed to login: see above')
	driver.close()
	sys.exit(1)

link_arr = driver.current_url.split('/')
userid = link_arr[3]

for link, sublinks in links.iteritems():
	if (link == 'profile') or (link == 'our_proposers'):
		driver.get(server+'/'+userid+'/'+link)
	else:
		driver.get(server+'/'+link)
	log.write('debug', 'trying to go to '+link)
	try:
		WebDriverWait(driver, 10).until(lambda driver : link in driver.current_url)
		log.write('debug', 'aaaand went to profile')
	except TimeoutException:
		log.write('error', 'timeout waiting for shit to load trying to get to '+link)
		driver.close()
		sys.exit(1)

	for sublink, subtext in links[link].iteritems():
		try:
			driver.find_element_by_partial_link_text(subtext).click()
			log.write('debug', 'went to '+sublink+' by '+subtext)
		except NoSuchElementException:
			log.write('error', 'no such link or wrong link text')
			driver.close()
			sys.exit(1)

		try:
			WebDriverWait(driver, 10).until(lambda driver : sublink in driver.current_url)
			log.write('debug', 'got to sublink '+sublink)
		except TimeoutException:
			log.write('error', 'timeout waiting for shit to load trying to get to sublink '+sublink)
			driver.close()
			sys.exit(1)

		layername_arr = sublink.split('/')
		if len(layername_arr) > 1:
			del layername_arr[0]
		layername = layername_arr[0]
		
		if link == 'deposit': # FIXME :: dog-nail
			layername = re.sub('-', '_', layername)
		if link == 'chat': # TODO :: chat dummy
			log.write('warning', 'chat not tested yet')
			continue

		try:
			layer = driver.find_element_by_id(layername)
			log.write('info', 'found div with required id='+layername)
			log.write('debug', 'its content follows: '+layer.text)
		except NoSuchElementException:
			log.write('error', 'no such div id='+layername)
			driver.close()
			sys.exit(1)


log.write('info', 'test PASSED')
driver.close()
sys.exit(0)

