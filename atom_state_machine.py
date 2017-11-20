#!/usr/bin/python3

import atom_command_interface as acmdi
import datetime
from firebase import firebase
from random import *

""" 
The State machine> Takes inputs and outputs to necessary state depending
on the inputs
"""
def resetStatus(status):
    fb = firebase.FirebaseApplication("https://atom-pet.firebaseio.com", None)
    data = {'command':status}
    result = fb.patch("/status", data)

def resetTime():
    return datetime.datetime.utcnow()

class State(object):
    """ 
    We define a state object which provides some utility functions for the
    individual states within the state machine.
    """

    def __init__(self):
        print ('Processing current state:', str(self))
        self._started_at = datetime.datetime.utcnow()

    def on_event(self, event):
        """ 
        Handle events that are delegated to this State.
        """
        pass

    def __repr__(self):
        """
        Leverages the __str__ method to describe the State.
        """
        return self.__str__()

    def __str__(self):
        """
        Returns the name of the State.
        """
        return self.__class__.__name__


class Standby(State):
    """ 
    The state which indicates that there are limited device capabilities.
    """

    def on_event(self, event):
        if event['command'] != 'standby':
            # if going to active mode, turn on safe mode functionality
            self._atom_command_interface.start()
            self._atom_state._started_at = resetTime()
            return Active()
        return self

class Active(State):
    """
    The state which indicates that there are limited device capabilities.
    """
    def on_event(self, event):
        if event['command'] == 'tricks':
            return Tricks()
        elif event['command'] == 'comeToMe':
            return comeToMe()
        elif event['command'] == 'cleanUp':
            return cleanUp()
        elif event['command'] == 'speak':
            return speak()
        elif event['command'] == 'goHome':
            return goHome()
        elif event['command'] == 'stop':
            return Stop()

        time_passed = datetime.datetime.utcnow() - self._atom_state._started_at
        # if over 200 seconds have passed, place back in passive mode
        if time_passed.total_seconds() > 200:
            resetStatus('standby')
            self._atom_command_interface.stop()
            return Standby()
        return self

class Stop(State):
    """
    Stops whatever command is currently happening and return to standby.
    """
    def on_event(self, event):
        resetStatus('standby')
        self._atom_command_interface.stop()
        return Standby()
     
class Tricks(State):
    """ 
    The state which indicates that there are no limitations on device
    capabilities.
    """

    def on_event(self, event):
        # Do tricks, reset to default state and then return to standby
        print('Atom is doing some super cool tricks')
        x = randint(1, 4)    # Pick a random number between 1 and 4
        self._atom_command_interface.doTricks(x)
        self._atom_command_interface.speak(x)
        resetStatus('active')
        self._atom_state._started_at = resetTime()
        return Active()


class comeToMe(State):
    """
    The state which indicates that there are no limitations on device
    capabilities.
    """

    def on_event(self, event):
        # Do comeTome, reset to default state and then return to standby
        print('Atom is moving towards you')
        x = randint(1, 26)    # Pick a random number between 1 and 26
        self._atom_command_interface.speak(x)
        # TODO: Add in Danny's API to find and move towards
        resetStatus('active')
        self._atom_state._started_at = resetTime()
        return Active()

class goHome(State):
    """ 
    The state which indicates that there are no limitations on device
    capabilities.
    """

    def on_event(self, event):
        # Do goHome, reset to default state and then return to standby
        print('Atom is moving towards its charger')
        self._atom_command_interface.goHome()
        x = randint(1, 26)    # Pick a random number between 1 and 26
        self._atom_command_interface.speak(x)
        resetStatus('active')
        self._atom_state._started_at = resetTime()
        return Active()

class cleanUp(State):
    """
    The state which indicates that there are no limitations on device
    capabilities.
    """

    def on_event(self, event):
        # Do cleanUp, reset to default state and then return to standby
        print('Atom is starting to clean up')
        self._atom_command_interface.cleanUp()
        x = randint(1, 26)    # Pick a random number between 1 and 26
        self._atom_command_interface.speak(x)
        resetStatus('cleaning')
        self._atom_state._started_at = resetTime()
        return cleaning()

class cleaning(State):
    """
    The state which indicates that there are no limitations on device
    capabilities.
    """

    def on_event(self, event):
        print('Atom is cleaning up')
        if event['command'] == 'tricks' or event['command'] == 'comeToMe' or event['command'] == 'goHome':
            self._atom_command_interface.stop()
            return Standby()
        elif event['command'] == 'comeToMe':
            return comeToMe()
        elif event['command'] == 'goHome':
            return goHome()
        elif event['command'] == 'speak':
            return speak()
        elif event['command'] == 'stop':
            return Stop()
        time_passed = datetime.datetime.utcnow() - self._atom_state._started_at
        # if over 200 seconds have passed, place back in passive mode
        if time_passed.total_seconds() > 30:
            resetStatus('standby')
            self._atom_command_interface.stop()
            return Standby()
        return cleaning()


class speak(State):
    """
    The state which indicates that there are no limitations on device
    capabilities.
    """

    def on_event(self, event):
        # Do speak, reset to default state and then return to standby
        print('Atom is speaking')
        x = randint(1, 26)    # Pick a random number between 1 and 26
        self._atom_command_interface.speak(x)
        resetStatus('active')
        self._atom_state._started_at = resetTime()
        return Active()


class StateMachine(object):
    """ 
    A simple state machine that mimics the functionality of a device from a 
    high level.
    """

    def __init__(self, state):
        """ Initialize the components. """

        # Start with a default state.
        self._state = Standby()
        # Pass the defaults through
        self._state._atom_command_interface = acmdi.Command()
        x = randint(1, 26)    # Pick a random number between 1 and 26
        # Whenever loaded up speak a random command
        self._state._atom_command_interface.speak(x)
        self._state._atom_state = self._state


    def on_event(self, event):
        """
        This is the bread and butter of the state machine. Incoming events are
        delegated to the given states which then handle the event. The result is
        then assigned as the new state.
        """

        # The next state will be the result of the on_event function.
        next_state = self._state.on_event(event)
        # pass atom state between states
        next_state._atom_state = self._state._atom_state
        # pass atom command interface reference
        next_state._atom_command_interface = self._state._atom_command_interface

        # passes necessary information to the next state
        self._state = next_state
