#! /usr/bin/python3
import atom_sound_interface as asi
import atom_drive_train as adt
import time
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
        
    def cleanUp(self):
        self._drive.clean()

    def goHome(self):
        self._drive.seek_dock()
	
    def doTricks(self, trick):
        if trick == 1:
            # Tell the Create2 to drive straight forward at a speed of 100 mm/s
            self._drive.drive_straight(100)
            # Wait for 4 seconds
            time.sleep(4)
            # Tell the Create2 to drive straight backward at a speed of 100 mm/s
            self._drive.drive_straight(-100)
            # Wait for 4 seconds
            time.sleep(4)
            # Stop the bot
            self._drive.drive_straight(0)
        elif trick == 2 :
            self._drive.turn_clockwise(100)
            # Wait for 4 seconds
            time.sleep(4)
            self._drive.turn_clockwise(0)
        elif trick == 3 :
            self._drive.turn_counter_clockwise(100)
            # Wait for 4 seconds
            time.sleep(4)
            self._drive.turn_counter_clockwise(0)
        elif trick == 4 :
            self._drive.play(2)

    def speak(self):
        self._drive.play(2)