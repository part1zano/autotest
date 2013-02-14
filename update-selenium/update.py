#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from HTMLParser import HTMLParser
import codecs
import commands
import re
import shutil
import os

def find_class(attrs):
	for attr in attrs:
		if attr[0] == 'class' and attr[1] == 'button green':
			return True
	return False

class VersionFinder(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.version = ''
		self.url = ''

	def handle_starttag(self, tag, attributes):
		if tag == 'a':
			href = ''
			if not find_class(attributes):
				return
			for attr in attributes:
				if attr[0] == 'href':
					href = attr[1]
			self.version = re.sub('.*selenium-', '', href)
			self.version = re.sub('.tar.gz', '', self.version)
			self.url = href
		return

status, output = commands.getstatusoutput('dpkg -l | grep python-selenium | awk "{print \$3}" | sed -e "s/\-[0-9].*//"')
version = output.strip()
if version:
	print 'python-selenium_%s found in system' % version
else:
	print 'python-selenium not found, trying to build and hoping for the best'

conn = urllib2.urlopen('http://pypi.python.org/pypi/selenium')
content = conn.read().strip()
parser = VersionFinder()
parser.feed(content)
if version == parser.version:
	print 'No updates found, exiting'
	exit(0)

conn = urllib2.urlopen(parser.url)
content = conn.read().strip()
try:
	open('selenium-%s.tar.gz' % parser.version, 'w').write(content)
except IOError:
	print 'failed writing tar.gz'
	exit(1)

status, output = commands.getstatusoutput('tar xf selenium-%s.tar.gz' % parser.version)
if status != 0:
	print 'unpacking tar.gz failed: %s' % output
	exit(2)
print 'unpacked selenium-%s' % parser.version

os.chdir('selenium-%s' % parser.version)
print 'cd selenium-%s' % parser.version

# what we do next:
# [DOEN] edit setup.py (?????)

try:
	shutil.copyfile('setup.py', 'setup.py.bak')
except IOError:
	print 'failed backing up setup.py'
	exit(3)

try:
	setup_content = open('setup.py', 'r').read()
except IOError, why:
	print 'failed to open setup.py for reading: %s' % why
	exit(3)

setup_content = re.sub('setup\(', 'setup(author="Maxim Kirenenko", author_email="part1zancheg@gmail.com",', setup_content)
try:
	open('setup.py', 'w').write(setup_content)
except IOError, why:
	print 'failed to write setup.py: %s' % why
	exit(3)
print 'edited setup.py'

# [] setup.py sdist (ok...)
result = commands.getstatusoutput('python setup.py sdist')[0]
if result != 0:
	print 'sdist failed'
	exit(4)
print 'successfully sdist-ed'

# [] cd dist && py2dsc selenium-%%VERSION%%.tar.gz (ok)
os.chdir('dist')

status, output = commands.getstatusoutput('py2dsc selenium-%s.tar.gz' % parser.version)
if status != 0:
	print 'py2dsc failed: %s' % output
	exit(5)
print 'successfully py2dsc-ed'
# [] cd deb_dist/selenium-%% && edit debian/control (s/-all//) && edit debian/changelog (s/unstable/precise/) (?????)
os.chdir('deb_dist/selenium-%s' % parser.version)
try:
	deb_content = open('debian/changelog').read()
except IOError, why:
	print 'failed opening deb/changelog: %s' % why
	exit(6)

deb_content = re.sub('unstable', 'precise', deb_content)
try:
	open('debian/changelog', 'w').write(deb_content)
except IOError, why:
	print 'writing deb/changelog failed: %s' % why
	exit(6)
print 'wrote to deb/changelog successfully'
# [] debuild -S (ok, but with some minor issues)
status, output = commands.getstatusoutput('debuild -S')
if status != 0:
	print 'debuild -S failed: %s' % output
	exit(7)
print 'debuild -S successful'
# [] cd .. && dput ppa:part1zancheg/selenium selenium_%%.changes (ok!)
os.chdir('..')
status, output = commands.getstatusoutput('dput ppa:part1zancheg/selenium *.changes')
if status != 0:
	print 'dput failed: %s' % output
	exit(8)
print 'dput successful, dance!'
# [] dance, sing, etc. (...)


