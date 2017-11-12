#! /usr/bin/python3
import atom_sound_interface as asi
from atom_drive_train import creat2api as adt
"""
This is the command interface. Connects to the sound, wifi, and drain train interfaces
"""

# initialize Firebase Application connection
class Command():
    def __init__(self):
        """
        Create an instance of Create2. This will automatically try to connect to your
        Roomba over serial
        """
        self._drive = adt.Create2()
        #Start the Create2
        self._drive.start()
        #Put the Create2 into 'safe' mode so we can drive it
        self._drive.safe()

		return self._drive