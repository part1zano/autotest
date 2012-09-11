#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import time

driver = webdriver.Firefox()

driver.get("http://dev.rek1.ru")

logins = driver.find_elements_by_name("username")
for login in logins:
	login.send_keys("m.filimonov@rekvizitka.ru")

passwords = driver.find_elements_by_name("password")
for password in passwords:
	password.send_keys("fgihad5")

driver.find_element_by_name("login").click()

try:
	WebDriverWait(driver, 10).until(lambda driver : u'profile' in driver.current_url)

	for cookie in driver.get_cookies():
		print "%s -> %s" % (cookie['name'], cookie['value'])
finally:
	driver.quit()
