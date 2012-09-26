# -*- coding: utf-8 -*-

from testlib import logger

log = logger.Log('tests.conf')

for level in ['info', 'error', 'warning', 'debug']:
	for line in ['dick vagina mdna', u'хуй пизда джигурда']:
		log.write(level, line)
