#!/usr/bin/python

import time
import uuid

try:
	# Python 3.6+
	from secrets import choice as _choice
except ImportError:
	# Python 2.7: SystemRandom se alimenta de os.urandom, la misma fuente que usa
	# secrets por dentro. No usar random.choice a secas, que es Mersenne Twister
	# y por lo tanto predecible.
	from random import SystemRandom
	_choice = SystemRandom().choice
 
class pyrandstring:
 
	length = 18
	seed = ''
	tmp_str =''
	file = ''
 
	def __init__(self):
		self.length = 18
		self.seed = 'all'

	def getStringUnique(self):
		return str(int(time.time())) + "_" + self.getString(16,'anum')

	def getUUID(self):
		return str(uuid.uuid4())

	def getStringList(self,quantity,length=None,seed=None):
		return [self.getString(length,seed) for a in range(int(quantity))]

 
	def getString(self,length=None,seed=None):

		if length is None:
			length = self.length

		if seed is None:
			seed = self.seed

		options = { 'abc': self.__abc, 'num': self.__num, 'anum': self.__anum , 'all': self.__all, 'bash': self.__bash, 'zsh': self.__bash}
		alphabet = options[seed]()

		return ''.join(_choice(alphabet) for a in range(int(length)))

	def __abc(self):
		return [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
		'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
 
	def __num(self):
		return ['0', '1' , '2', '3', '4', '5', '6', '7', '8', '9']
 
	def __anum(self):
		return [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
		'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
		'0', '1' , '2', '3', '4', '5', '6', '7', '8', '9']
 
	def __all(self):
 
		return [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
		'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
		'0', '1' , '2', '3', '4', '5', '6', '7', '8', '9',
		'!', '"', '#', '$', '%', '&', '(', ')', '*', '+', ',', '-', '.', '/', '{', '|', '}', '~', '@']

	def __bash(self):
 
		return [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
		'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
		'0', '1' , '2', '3', '4', '5', '6', '7', '8', '9',
		'!', '#', '$', '%', '&', '*', '+', ',', '-', '.', '/', '{', '|', '}', '~', '@']
 

