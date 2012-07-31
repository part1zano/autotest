#!/usr/bin/env python
# -*- coding: utf-8 -*-

from logger import log
import string,time,stabledict
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,NoSuchElementException,WebDriverException
from selenium.webdriver.support.ui import WebDriverWait

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
	except NoSuchEleementException:
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
	log.write('debug', 'waking up, returning True')
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

def get_browser(browser):
	if browser == 'firefox':
		return webdriver.Firefox()
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
	log.write('debug', 'woke up, returning true')
	return True

def get_our_info(driver, field_name):
	""" 
	assuming we're in our profile
	"""
	if field_name == 'id':
		return driver.current_url.split('/')[3]
	elif field_name == 'url':
		return driver.current_url
	try:
		value = driver.find_element_by_id(field_name).text
	except NoSuchElementException:
		log.write('error', 'no such field')
		return None

	return value		

def recommend_by_title(driver, title_fragment, new):
	"""
	goes to company profile assuming that it might be in search results
	"""

	our_bname = get_our_info(driver, 'brandName')
	our_url = get_our_info(driver, 'url')

	if new:
		give = u'Дать рекомендацию'
	else:
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

	if not find_link_and_click(driver, u'Рекомендации', 'our_proposers'):
		log.write('error', 'not going to our-proposers, see above')
		return False

	log.write('debug', 'checking if we are in list of proposers')
	
	try:
		div = driver.find_element_by_id('our_proposers')
	except NoSuchElementException:
		log.write('error', 'no recommendations div')
		return False

	if (our_bname in div.text) != new:
		log.write('error', 'wrong recommendation data')
		return False
	
	driver.get(our_url)
	log.write('debug', 'got to profile, sleeping for 2s')
	time.sleep(2)
	log.write('debug', 'woke up, whatcha next?')

	log.write('debug', 'in self.profile, tryin to go to recommendations')
	
	links = stabledict.StableDict(((u'Наши рекомендации', 'our_proposers'), (u'Мы рекомендуем', 'we_recommend')))
	for text, url in links.items():
		if not find_link_and_click(driver, text, url):
			log.write('error', 'no such link: '+url)
			return False
		log.write('debug', 'got to '+url)

	try:
		div = driver.find_element_by_id('we_recommend')
	except NoSuchElementException:
		log.write('error', 'no recommendations div')
		return False

	if (title_fragment in div.text) != new:
		log.write('error', 'wrong recommendation data')
		return False

	return True

def click_dict(driver, dict_):
	for text, url in dict_.items():
		log.write('debug', 'trying to visit '+url+' by clicking on '+text)
		if not find_link_and_click(driver, text, url):
			log.write('error', 'not going to '+url+', see above')
			return False
	
	return True


