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


def randomPhrase(length = len(phrases)):
	phrase = ''
	for index in range(length):
		phrase += ' '+phrases[index][random.randint(0, len(phrases))]

	return phrase.strip()

def randomNum(length):
	number = ''
	for index in range(length):
		number += str(random.randint(0, 9))

	return int(number)

def coin():
	return bool(random.randint(0,9) % 2)
