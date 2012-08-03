AUTOTESTS
---------

### main.py
Script that runs some automatic tests (maybe all of them). Is really simple.

### test-bug-208.py
Reproduces bug #208 

### test-contacts.py
Edit contacts form

### test-edit-profile.py
Edit info form

### test-feedback.py
Feedback form

### test-invite.py
Invite another company form

### test-login.py
Login

### test-logout.py
Logout

### test-profile-links.py
Clicks all of the links in a company's profile

### test-recommend.py
Recommends a company, checks whether info updated, unrecommends, checks again

### tests.conf
Config for teh tests

### test-settings-links.py
Clicks all the links in a user's settings. No modifications; one modification form == one test

### objlists/
Files with lists of objects with values to edit

### testlib/
#### functions.py
All needed functions: login/logout/find link and click it/etc
#### logger.py
A simple and nice logger w/levels. Was way, way too lazy to read about Python's logger

### javascript.py, sample-autotest.py
First steps in Selenium autotests

### jmeter/, tsung/
Load test utils: a test plan for jmeter and a xml config for tsung.
