# -*- coding: utf-8 -*-

from testlib import myrandom

print myrandom.random_1lvl_domain()
print myrandom.random_domain()
print myrandom.random_login()
print myrandom.random_email(login_separator='.', login_len=1, domain_lvl=5, lvl1_length=4)
print myrandom.randomPhrase()
print myrandom.coin()

