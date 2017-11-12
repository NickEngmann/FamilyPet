#! /usr/bin/python3
 
import atom_command_interface as acmdi

from firebase import firebase

"""
The State machine> Takes inputs and outputs to necessary state depending
on the inputs
"""
def resetStatus():
    fb = firebase.FirebaseApplication("https://atom-pet.firebaseio.com", None)
    data = {'command':'standby'}
    result = fb.patch("/status", data)


class State(object):
    """
    We define a state object which provides some utility functions for the
    individual states within the state machine.
    """

    def __init__(self):
        print ('Processing current state:', str(self))

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
        if event['command'] == 'tricks':
            return Tricks()
        elif event['command'] == 'comeToMe':
            return comeToMe()
        elif event['command'] == 'cleanUp':
            return cleanUp()
        elif event['command'] == 'speak':
            return speak()
        return self


class Tricks(State):
    """
    The state which indicates that there are no limitations on device
    capabilities.
    """

    def on_event(self, event):
        # Do tricks, reset to default state and then return to standby
        print('Atom is doing some super cool tricks')
        resetStatus()
        return Standby()


class comeToMe(State):
    """
    The state which indicates that there are no limitations on device
    capabilities.
    """

    def on_event(self, event):
        # Do comeTome, reset to default state and then return to standby
        print('Atom is moving towards you')
        resetStatus()
        return Standby()


class cleanUp(State):
    """
    The state which indicates that there are no limitations on device
    capabilities.
    """

    def on_event(self, event):
        # Do cleanUp, reset to default state and then return to standby
        print('Atom is cleaning up')
        resetStatus()
        return Standby()


class speak(State):
    """
    The state which indicates that there are no limitations on device
    capabilities.
    """

    def on_event(self, event):
        # Do speak, reset to default state and then return to standby
        print('Atom is speaking')
        resetStatus()
        return Standby()


class StateMachine(object):
    """ 
    A simple state machine that mimics the functionality of a device from a 
    high level.
    """

    def __init__(self, state):
        """ Initialize the components. """
        self._atom_command_interface = acmdi.Atom()

        # Pass the defaults through
        self._state._atom_command_interface = acmdi.Command()
        self._state._atom_state = state

        # Start with a default state.
        self._state = Standby()


 
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