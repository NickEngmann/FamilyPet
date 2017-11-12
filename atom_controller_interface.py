#! /usr/bin/python3
 
import atom_state_machine as astm
import atom_alexa_interface as aai
import time


"""
This is the main, establishes checker and updates the state machine 
"""


atom_alexa = aai.Alexa()
atom_state = astm.StateMachine(atom_alexa._state)

while(1):
    status = atom_alexa.update_state()
    if status['command'] != 'standby':
        atom_state.on_event(status)

