#!/usr/bin/python3
 
import atom_state_machine as astm
import atom_alexa_interface as aai
import time


"""
This is the main, establishes checker and updates the state machine 
"""

# starts the Alexa/Firebase connection
atom_alexa = aai.Alexa()
atom_state = astm.StateMachine(atom_alexa._state)

while(1):
    # polls the update_state and starts events
    status = atom_alexa.update_state()
    atom_state.on_event(status)

