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
browser = cnf.get('browser', 'browser')

links = {}
for link in ['news', 'deposit', 'contractors', 'our_proposers', 'chat', 'newsfeed']:
	if ('news' in link) and ('feed' not in link):
		links['mc_sidebar_profile'] = [link, {}]
	else:
		links['mc_sidebar_'+link] = [link, {}]
	if ('news' in link) and ('feed' not in link):
		sublinks = ['news', 'profile', 'contacts']
	elif 'deposit' in link:
		sublinks = ['deposit', 'topping_up', 'payments']
	elif 'contractors' in link:
		sublinks = ['contractors_list', 'in_reqs', 'out_reqs']
	elif 'our_proposers' in link:
		sublinks = ['our_proposers', 'we_recommend', 'invites']
	elif 'chat' in link:
		sublinks = ['dialog_list']
	
	for sublink in sublinks:
		if ('news' in link) and ('feed' not in link):
			links['mc_sidebar_profile'][1]['link_'+sublink] = sublink
		elif 'contractors' in sublink:
			links['mc_sidebar_'+link][1]['link_'+sublink] = link
		elif '_reqs' in sublink:
			if 'in' in sublink:
				in_out = 'coming'
			else:
				in_out = 'going'
			links['mc_sidebar_'+link][1]['link_'+sublink] = re.sub('_reqs', in_out, sublink)
		elif 'chat' in link:
			links['mc_sidebar_'+link][1]['link_'+sublink] = link
		elif 'newsfeed' in link:
			links['mc_sidebar_'+link][1]['link_'+sublink] = 'news-feed'
		else:
			links['mc_sidebar_'+link][1]['link_'+sublink] = sublink


driver = functions.get_browser(browser)
driver.get(server)

if not functions.login(driver, login, passwd):
	log.write('error', 'failed to login: see above')
	driver.close()
	sys.exit(1)

log.write('info', 'login ok')

link_arr = driver.current_url.split('/')
userid = link_arr[3]

log.write('debug', 'login as userid '+userid)

for sidebar_id, tablinks in links.items():
	if not functions.find_link_by_id_and_click(driver, sidebar_id, tablinks[0]):
		log.write('error', 'no sidebar link id='+sidebar_id)
		driver.close()
		sys.exit(1)

	for tablink, taburl in tablinks[1].items():
		if 'deposit' in sidebar_id:
			taburl = re.sub('_', '-', taburl)
		if not functions.find_link_by_id_and_click(driver, tablink, taburl):
			log.write('error', 'no tablink id='+tablink)
			driver.close()
			sys.exit(1)
		
		layername = taburl
		if 'deposit' in sidebar_id:
			layername = re.sub('-', '_', layername)
		elif 'contractors' in sidebar_id:
			layername += 'list'
		elif 'chat' in sidebar_id:
			layername = re.sub('link_', '', tablink)

		if not functions.check_div(driver, layername):
			log.write('error', 'no layer id='+layername)
			driver.close()
			sys.exit(1)


log.write('info', 'test PASSED')
driver.close()
sys.exit(0)

