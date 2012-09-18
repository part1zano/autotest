# -*- coding: utf-8 -*-
import sys,re,random

phrases = [
['The', 'Le', 'Our', 'Their', 'This', 'My', 'Your', 'That', 'Obvious', 'Hilarious', 'Slutty'],
['quick', 'slow', 'crazy', 'sane', 'lazy', 'hard-working', 'telepathic', 'pathetic', 'apathetic', 'weird', 'unnamed'],
['fox', 'dog', 'plane', 'pencil', 'drawer', 'roll', 'dice', 'mother', 'son', 'father', 'daughter'],
['is', 'gets', 'likes', 'fakes', 'loves', 'hates', 'dislikes', 'can in', 'cannot in', 'flames', 'changes'],
['cake', 'love', 'god', 'math', 'physics', 'orgasm', 'mud', 'dirt', 'bitches', 'whores', 'sluts'],
['in', 'inside of', 'outside of', 'by', 'at', 'near', 'before', 'after', 'before', 'near', 'at'],
['plague', 'shadow', 'shade', 'the dark', 'the box', 'bed', 'shower', 'work', 'town', 'city', 'village']
]

alphabet = 'qwertyuiopasdfghjklzxcvbnm'

def random_login(words=3, separator='_'):
	login = ''
	for i in range(words):
		index = random.randint(1, len(phrases)-1)
		login += re.sub(' ', separator, phrases[index][random.randint(0, len(phrases[index])-1)])+separator

	login = re.sub(separator+'$', '', login)
	
	return login

def random_1lvl_domain(length=2):
	domain = ''
	for i in range(length):
		domain += alphabet[random.randint(0, len(alphabet)-1)]
	
	return domain

def random_domain(lvl=2, lvl1_length=2):
	domain = ''
	for i in range(lvl-1):
		index = random.randint(1, len(phrases)-1)
		domain += re.sub(' ', '-', phrases[index][random.randint(0, len(phrases[index])-1)])+'.'

	domain += random_1lvl_domain(lvl1_length)
	return domain

def random_email(login_len=3, login_separator='_', domain_lvl=2, lvl1_length=2):
	return random_login(login_len, login_separator)+'@'+random_domain(domain_lvl, lvl1_length)

def randomPhrase(length = len(phrases)):
	phrase = ''
	for index in range(length):
		rnd_2 = random.randint(0, len(phrases[index])-1)
		phrase += ' '+phrases[index][random.randint(0, rnd_2)]

	return phrase.strip()

def randomNum(length):
	number = ''
	for index in range(length):
		number += str(random.randint(0, 9))

	return int(number)

def coin():
	return bool(random.randint(0,9) % 2)
