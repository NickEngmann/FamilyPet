#! /usr/bin/python3

from firebase import firebase
from time import gmtime, strftime, localtime

"""
This is the command interface. Connects to the sound, wifi, and drain train interfaces
"""

# initialize Firebase Application connection
class Atom():
	def __init__(self, location=None, user=None, command=None):
		self._fb = firebase.FirebaseApplication("https://atom-pet.firebaseio.com", None)

		# Initial State
		time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		data = {'state':'initialize', 'location':location, 'timestamp':time ,'user':user, 'command': command}
		result = self._fb.patch("/status", data)

		self._state = data
