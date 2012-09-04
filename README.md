# AUTOTESTS

### deploy/
Deploy scripts, sometimes useful

### jmeter/ 
JMeter seems to be a 'not-too-bad' tool for load testing

### tsung/
tsung is another load test tool

### json\_lists/
JSON lists for links/edits/errors/results. Needed by most of my tests

### testlib/
##### testlib/testcase.py
Contains parent class for all of the scripts

##### testlib/logger.py
A nice logger

### main.py
The main script. Is simple and mostly reliable, also flexible

### test\_changepwd.py
Changes password. Uses the three basic cases:
* **positive** Just change password using the correct old password and the valid and matching new ones
* **negative** First of the two new passwords is wrong
* **negative** The new passwords don't match
* **positive** Changes passwd back to original

### test\_edit\_contacts.py
Edits contacts. One per pass. Might be really buggy and fucked-up

### test\_edit\_info.py
Edits userinfo. All in one.

### test\_feedback.py
Feedback. Supports some cases

Fuck this shit, I quit
