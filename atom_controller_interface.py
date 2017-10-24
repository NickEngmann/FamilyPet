#! /usr/bin/python3
 
import atom_state_machine as astm
import time
from firebase import firebase

"""
This is the main, establishes checker and updates the state machine 
"""



atom_state = astm.StateMachine()
fb = firebase.FirebaseApplication("https://atom-pet.firebaseio.com", None)

while(1)
    state = fb.get('/status', None)
    print state
    atom_state.on_event(state)
    time.sleep(1000) # check every second
