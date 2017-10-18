#! /usr/bin/python3

from firebase import firebase
from time import gmtime, strftime, localtime

# initialize Firebase Application connection
class Atom(self):
	def __init__(self):
		self._fb = firebase.FirebaseApplication("https://atom-pet.firebase.io.com", None)

		# Initial State
		time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		data = {'state':'initialize', 'location':None, 'timestamp':time ,'user':None, 'command': None}
		result = self._fb.patch("/status", data)
