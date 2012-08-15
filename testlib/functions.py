#!/usr/bin/env python
# -*- coding: utf-8 -*-

from logger import log
import string,time,stabledict
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,NoSuchElementException,WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

def login(driver, loginstr, passwordstr, other=False):
	try:
		logins = driver.find_elements_by_name('username')
	except NoSuchElementException:
		log.write('error', 'no login elements')
		return False
	for login in logins:
		log.write('debug', 'found a login element')
		login.send_keys(loginstr)
		log.write('debug', 'sent ' + loginstr + ' into it')
	try:
		passwords = driver.find_elements_by_name('password')
	except NoSuchElementException:
		log.write('error', 'no password elements')
		return False
	for password in passwords:
		log.write('debug', 'found a password element')
		password.send_keys(passwordstr)
		log.write('debug', 'sent ' + passwordstr + ' into it')
	
	if other:
		try:
			foreign = driver.find_element_by_id('publicpc')
		except NoSuchElementException:
			log.write('error', 'no foreign computer checkbox')
			return False
		try:
			foreign.click()
			log.write('debug', 'foreign computer checkbox clicked')
		except WebDriverException:
			log.write('warning', 'foreign computer checkbox unclickable')
#			return False
	try:
		driver.find_element_by_name('login').click()
	except NoSuchElementException:
		log.write('error', 'No login button')
		return False
	log.write('debug', 'clicked "login"')

	try:
		WebDriverWait(driver, 10).until(lambda driver : u'profile' in driver.current_url)
		log.write('debug', 'logged in, visited profile')
	except TimeoutException:
		log.write('error', 'timeout waiting for shit to load')
		return False
	
	log.write('debug', 'sleeping for 2s waiting for shit to load')
	time.sleep(2)
	log.write('debug', 'woke up, will now check divs')

	if not check_page(driver):
		log.write('error', 'some divs missing, see above')
		return False
	log.write('debug', 'divs ok')

	for cookie in driver.get_cookies():
		if bool(u'sessionid' in string.lower(cookie['name'])) != bool(other):
			log.write('debug', 'Cookies ok')
			return True
	log.write('error', 'Cookies not ok')
	return False

def edit_control(driver, control, value, ctl_type):
	try:
		ctl = driver.find_element_by_id(control)
		log.write('debug', 'found element ' + control)
	except NoSuchElementException:
		log.write('error', 'no such element: ' + control)
		return False
	old_value = ctl.get_attribute('value')
	log.write('debug', 'old value for '+control+' is: '+old_value)
	log.write('debug', 'old value for '+control+' is')
	if u'text' in ctl_type:
		log.write('debug', 'the element is a textarea or so')
		
		ctl.send_keys(value)
		log.write('debug', 'sent info into it')
		if (string.lower(ctl.get_attribute('value')) == string.lower(old_value+value)) or (len(ctl.get_attribute('value')) == 80):
			log.write('debug', 'values match, its ok')
		else:
			log.write('error', 'values dont match before submit: NOK')
			log.write('error', 'new value SHOULD BE '+old_value+value)
			log.write('error', 'new value = '+ctl.get_attribute('value'))
			return False
	elif u'popup' in ctl_type:
		log.write('debug', 'the element is a drop-down menu or so')
		try:
			all_options = ctl.find_elements_by_name('option')
			log.write('debug', 'found ' + len(all_options) + ' options in element ' + control)
		except NoSuchElementException:
			log.write('error', 'no options in element ' + control)
			return False
		for option in all_options:
			log.write('debug', 'found option' + option + ' in control ' + control)
			if value in option.get_attribute('value'):
				log.write('debug', 'clicked requested option ' + value)
				option.click()
	else:
		log.write('error', 'unknown element type')
		return False
	return True

def check_edited(driver, control, value, ctl_type):
	try: 
		ctl = driver.find_element_by_id(control)
		log.write('debug', 'found requested element '+control)
	except NoSuchElementException:
		log.write('error', 'control id='+control+' not found')
		return False
	old_value = ctl.get_attribute('value')
	if edit_control(driver, control, value, ctl_type):
		log.write('info', 'edited element id='+control+' successfully, trying to submit')
		try:
			driver.find_element_by_partial_link_text(u'Сохранить').click()
			log.write('debug', 'submit successfully clicked')
		except NoSuchElementException:
			log.write('error', 'No submit button or wrong link text')
			return False

		new_value = old_value+value
		return check_value(driver, control, new_value)
		
	else:
		return False
	return True

def check_value(driver, control, value):
	try:
		label = driver.find_element_by_id(control)
		log.write('debug', 'found label for '+control)
	except NoSuchElementException:
		log.write('error', 'no such control in presend window')
		return False

	log.write('debug', control+' value is: '+label.text)
	if (string.lower(value) == string.lower(label.text)) or (len(label.text) == 80):
		log.write('info', 'element '+control+' value is ok')
		log.write('debug', 'it is '+value)
		return True
	log.write('error', 'element '+control+' value NOK')
	log.write('error', 'it is '+string.lower(label.text))
	log.write('error', 'while it should be: '+string.lower(value))
	return False

def check_div(driver, div_id):
	try:
		div = driver.find_element_by_id(div_id)
		log.write('debug', 'found div id='+div_id)
		log.write('debug', 'its content follows: '+div.text)
	except NoSuchElementException:
		log.write('error', 'no such div id='+div_id)
		return False

	return True

def get_value(driver, control):
	try:
		ctl = driver.find_element_by_id(control)
		log.write('debug', 'got element '+control+' for extracting value')
	except NoSuchElementException:
		log.write('error', 'no such element '+control)
		return None

	if ctl.get_attribute('value') != None:
		log.write('debug', 'its an edit or so, and its value is: '+ctl.get_attribute('value'))
		return ctl.get_attribute('value')
	else:
		log.write('debug', 'its a label or so, and its value is: '+ctl.text)
		return ctl.text

def logout(driver):
	try:
		logout = driver.find_element_by_partial_link_text(u'Выйти')
		log.write('debug', 'found logout link')
	except NoSuchElementException:
		log.write('error', 'no logout link or wrong link text')
		return False

	logout.click()
	try:
		WebDriverWait(driver, 10).until(lambda driver : u'profile' not in driver.current_url)
		log.write('info', 'logged out successfully')
	except TimeoutException:
		log.write('error', 'timeout waiting for shit to load')
		return False
	return True

def find_link_by_id_and_click(driver, id_text, url):
	try:
		driver.find_element_by_id(id_text).click()
		log.write('debug', 'link id='+id_text+', url='+url+' clicked')
	except NoSuchElementException:
		log.write('error', 'no such link id='+id_text)
		return False

	try:
		WebDriverWait(driver, 10).until(lambda driver : url in driver.current_url)
	except TimeoutException:
		log.write('error', 'not going to '+url+' by id='+id_text+' due to timeout')
		return False

	log.write('debug', 'finally got to '+url+' by link id='+id_text)
	log.write('debug', 'sleep for 2s')
	time.sleep(2)
	log.write('debug', 'woke up, checkin divs')

	return check_page(driver)

def find_link_and_click(driver, link_text, url):
	try:
		driver.find_element_by_partial_link_text(link_text).click()
		log.write('debug', link_text+' clicked')
		log.write('debug', url+' clicked')
	except NoSuchElementException:
		log.write('error', 'no '+link_text+' link or wrong link text')
		log.write('error', 'no link for '+url+'s link_text')
		return False

	try:
		WebDriverWait(driver, 10).until(lambda driver : url in driver.current_url)
	except TimeoutException:
		log.write('error', 'timeout waiting for shit to load or not going to url containing '+url)
		return False

	log.write('debug', 'finally got to '+link_text+' and url contains '+url)
	log.write('debug', 'finally got to '+url)
	log.write('debug', 'sleep for 2s after getting here')
	time.sleep(2)
	log.write('debug', 'waking up, checkin divs')
	return check_page(driver)

def clear_element(driver, control):
	try:
		ctl = driver.find_element_by_id(control)
		log.write('debug', control+' element found for clearing')
	except NoSuchElementException:
		log.write('error', control+' not found')
		return False

	ctl.clear()
	return True

def click_submit(driver, link_text): # TODO :: needed or not?
	try:
		driver.find_element_by_partial_link_text(link_text).click()
		log.write('debug', link_text+' submit clicked')
		log.write('debug', 'submit clicked')
	except NoSuchElementException:
		log.write('error', 'no submit button or wrong link text')
		return False
	return True

def get_ff_proxy(proxy_host, proxy_port):
	fp = webdriver.FirefoxProfile()

	fp.set_preference('network.proxy.type', 1)

	for proto in ['http', 'ftp', 'ssl']:
		fp.set_preference('network.proxy.'+proto, proxy_host)
		fp.set_preference('network.proxy.'+proto+'_port', proxy_port)

	fp.set_preference('network.proxy.no_proxies_on', '')

	return webdriver.Firefox(firefox_profile = fp)

def get_browser(browser, proxy_host=None, proxy_port=None):
	"""
	doesn't work with chrome
	"""
	if proxy_port is None:
		proxy_port = 8090
	if browser == 'firefox':
		if proxy_host is None:
			return webdriver.Firefox()
		return get_ff_proxy(proxy_host, proxy_port)
	elif browser == 'chrome':
		return webdriver.Chrome()
	else:
		return None

def check_page(driver):
	divs = ['content']
	if 'feedback' in driver.current_url:
		divs.append('feedback')
	else:
		divs.append('tabs_container')
		divs.append('tabs')
		divs.append('left-sidebar')
		if 'chat' in driver.current_url:
			divs.append('employee-header')
		else:
			divs.append('company-header')

	for divname in divs:
		if not check_div(driver, divname):
			log.write('error', 'no such div: '+divname)
			return False
		log.write('debug', 'found '+divname)

	return True

def find_stuff(driver, stuff):
	try:
		search = driver.find_element_by_name('q')
	except NoSuchElementException:
		log.write('error', 'no search form')
		return False
	search.clear()
	search.send_keys(stuff)
	search.submit()
	try:
		WebDriverWait(driver, 10).until(lambda driver : 'q' in driver.current_url)
	except TimeoutException:
		log.write('error', 'timeout waiting for search results to load')
		return False
	log.write('debug', 'at the search results page, sleeping for 2s')
	time.sleep(2)
	log.write('debug', 'woke up, checkin divs')
	try:
		searchdiv = driver.find_element_by_id('global-search-result')
	except NoSuchElementException:
		log.write('error', 'no search results div')
		return False
	if stuff in searchdiv.text:
		log.write('info', 'even found stuff in div!')
		log.write('debug', 'stuff was: '+stuff)
	else:
		log.write('warning', 'no stuff in div!')
		log.write('warning', 'stuff was: '+stuff)
	return True

def get_our_info(driver, field_name):
	""" 
	assuming we're in our profile
	"""
	if field_name == 'id':
		return driver.current_url.split('/')[3]
	if field_name == 'url':
		return driver.current_url
	try:
		value = driver.find_element_by_id(field_name).text
	except NoSuchElementException:
		log.write('error', 'no such field')
		return None

	return value		

def add_contractor_by_title(driver, their_title, do=True):
	if not find_stuff(driver, their_title):
		log.write('error', 'error finding their title, see above')
		return False

	if not find_link_and_click(driver, their_title, 'profile'):
		log.write('error', 'needed link not in search results, see above')
		return False

	try:
		driver.find_element_by_id('sidebar_contractor_action').click()
	except NoSuchElementException:
		log.write('no contractor-action button')
		return False

	try:
		info_text = driver.find_element_by_id('informer-text').text
		log.write('error', 'error adding')
		log.write('error', 'error is: '+info-text)
		return False
	except NoSuchElementException:
		log.write('info', 'adding w/o errors, ok')
	
	log.write('debug', 'clicked sidebar-contractor-action, sleeping for 2s')
	time.sleep(2)
	log.write('debug', 'woke up, where is my approve-btn?')

	for oktext in ['OK', u'ОК']:
		try:
			ok = driver.find_element_by_partial_link_text(oktext)
		except NoSuchElementException:
			log.write('warning', oktext+' button not found')

	try:
		ok.click()
	except NameError:
		log.write('error', 'no informer or no ok button or wrong link text')
		return False
	log.write('info', 'add_contractor_by_name returning True')
	return True	

def check_request_contractor_by_name(driver, name):
	links = stabledict.StableDict((('mc_sidebar_contractors', 'contractors'), ('link_out_reqs', 'outgoing'))) # FIXME :: link_out_reqs

	for link_id, link_url in links.items():
		if not find_link_by_id_and_click(driver, link_id, link_url):
			log.write('error', 'error visiting '+link_url+'via link id='+link_id+', see above')
			return False

		if not check_div(driver, link_url+'list'):
			log.write('error', 'no such div: '+link_url+'list')
			return False

	try:
		title = driver.find_element_by_partial_link_text(name)
	except NoSuchElementException:
		log.write('erorr', name+' doesnt seem to be in list')
		return False

	log.write('debug', 'found title: '+name)

	hover = ActionChains(driver).move_to_element(title)
	hover.perform()
	log.write('debug', 'mouse over title:'+name)

	for btn in [u'Написать сообщение', u'Отменить']:
		try:
			button = driver.find_element_by_partial_link_text(btn)
		except NoSuchElementException:
			log.write('error', 'no '+btn+' button')
			return False
	
	log.write('info', 'found all buttons for'+name)
	log.write('info', 'check_request returning True')
	return True
	

def approve_application_by_title(driver, their_title, do=True):
	pass

def recommend_by_title(driver, title_fragment, new, recommend=True):
	"""
	goes to company profile assuming that it might be in search results
	"""
	
	our_bname = get_our_info(driver, 'brandName')
	if len(our_bname) > 30:
		our_bname = our_bname[:18]
	our_url = get_our_info(driver, 'url')

	if new:
		if recommend:
			recommend_btn = u'Дать рекомендацию'
		else:
			recommend_btn = u'Отмена'	
		give = u'Дать рекомендацию'
	else:
		if recommend:
			recommend_btn = u'Да'
		else:
			recommend_btn = u'Нет'
		give = u'Отозвать рекомендацию'
	
	if not find_stuff(driver, title_fragment):
		log.write('error', 'some shit with search, see above')
		return False

	if not find_link_and_click(driver, title_fragment, 'profile'):
		log.write('error', 'no link or no such company')
		return False

	log.write('debug', 'in company profile, trying to recommend')

	try:
		driver.find_element_by_partial_link_text(give).click()
	except NoSuchElementException:
		log.write('error', 'no recommend link or wrong recommendation direction')
		return False
	# clicked link in profile, a window appears
	log.write('debug', 'clicked '+give)
	log.write('debug', 'waiting for window, sleep for 2s')
	time.sleep(2)
	log.write('debug', 'woke up, wheres my win?')

	try:
		for btn in driver.find_elements_by_partial_link_text(recommend_btn):
			btn.click()
			log.write('debug', recommend_btn+' clicked')
	except NoSuchElementException:
		log.write('error', 'no btn')
		return False

	log.write('debug', 'clicked recommend_btn, sleeping for 2s')
	time.sleep(2)
	log.write('debug', 'woke up, going to check')

	if not find_link_by_id_and_click(driver, 'mc_sidebar_our_proposers', 'our_proposers'):
		log.write('error', 'not going to our-proposers, see above')
		return False

	log.write('debug', 'checking if we are in list of proposers')
	
	try:
		div = driver.find_element_by_id('our_proposers')
	except NoSuchElementException:
		log.write('error', 'no recommendations div in their profile')
		return False

	if (new == recommend) != (our_bname in div.text):
		log.write('error', 'wrong recommendation data in their profile')
		return False
	
	driver.get(our_url)
	log.write('debug', 'got our to profile, sleeping for 2s')
	time.sleep(2)
	log.write('debug', 'woke up, whatcha next?')

	log.write('debug', 'in self.profile, tryin to go to recommendations')
	
	links = stabledict.StableDict((('mc_sidebar_our_proposers', 'our_proposers'), ('link_we_recommend', 'we_recommend')))
	for text, url in links.items():
		if not find_link_by_id_and_click(driver, text, url):
			log.write('error', 'no such link: '+url)
			return False
		log.write('debug', 'got to '+url)

	try:
		div = driver.find_element_by_id('we_recommend')
	except NoSuchElementException:
		log.write('error', 'no recommendations div in our profile')
		return False

	if (new == recommend) != (title_fragment in div.text):
		log.write('error', 'wrong recommendation data in our profile')
		return False

	return True

