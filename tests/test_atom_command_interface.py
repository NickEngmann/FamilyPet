"""test_atom_command_interface.py — Unit tests for Command class.

Tests the atom_command_interface module which connects sound, wifi, and drive train interfaces.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, call
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestCommandClass:
    """Test suite for the Command class."""
    
    @pytest.fixture(autouse=True)
    def mock_dependencies(self):
        """Mock all hardware dependencies before each test."""
        with patch('atom_command_interface.adt') as mock_adt:
            with patch('atom_command_interface.mixer') as mock_mixer:
                with patch('atom_command_interface.time') as mock_time:
                    mock_drive = Mock()
                    mock_adt.Create2.return_value = mock_drive
                    mock_mixer.init.return_value = None
                    mock_mixer.music.set_volume.return_value = None
                    mock_mixer.music.load.return_value = None
                    mock_mixer.music.play.return_value = None
                    mock_time.sleep.return_value = None
                    
                    yield {
                        'mock_drive': mock_drive,
                        'mock_mixer': mock_mixer,
                        'mock_time': mock_time,
                        'mock_adt': mock_adt
                    }
    
    def test_command_initialization(self, mock_dependencies):
        """Test that Command initializes correctly with mocked dependencies."""
        from atom_command_interface import Command
        
        cmd = Command()
        
        # Verify drive interface was created
        assert mock_dependencies['mock_adt'].Create2.called
        # Verify mixer was initialized
        assert mock_dependencies['mock_mixer'].init.called
        # Verify volume was set
        assert mock_dependencies['mock_mixer'].music.set_volume.called
    
    def test_start_method(self, mock_dependencies):
        """Test the start method calls drive interface correctly."""
        from atom_command_interface import Command
        
        cmd = Command()
        cmd.start()
        
        # Verify start, safe, and wake were called on drive interface
        assert mock_dependencies['mock_drive'].start.called
        assert mock_dependencies['mock_drive'].safe.called
        assert mock_dependencies['mock_drive'].wake.called
    
    def test_stop_method(self, mock_dependencies):
        """Test the stop method calls drive interface correctly."""
        from atom_command_interface import Command
        
        cmd = Command()
        cmd.stop()
        
        # Verify stop was called on drive interface
        assert mock_dependencies['mock_drive'].stop.called
    
    def test_cleanUp_method(self, mock_dependencies):
        """Test the cleanUp method calls drive interface correctly."""
        from atom_command_interface import Command
        
        cmd = Command()
        cmd.cleanUp()
        
        # Verify clean was called on drive interface
        assert mock_dependencies['mock_drive'].clean.called
    
    def test_goHome_method(self, mock_dependencies):
        """Test the goHome method calls drive interface correctly."""
        from atom_command_interface import Command
        
        cmd = Command()
        cmd.goHome()
        
        # Verify seek_dock was called on drive interface
        assert mock_dependencies['mock_drive'].seek_dock.called
    
    def test_doTricks_method_trick1(self, mock_dependencies):
        """Test doTricks with trick 1 (drive forward/backward)."""
        from atom_command_interface import Command
        
        cmd = Command()
        cmd.doTricks(1)
        
        # Verify drive_straight was called with forward speed
        assert mock_dependencies['mock_drive'].drive_straight.call_count == 3
        # Check forward call
        calls = mock_dependencies['mock_drive'].drive_straight.call_args_list
        assert calls[0][0][0] == 100  # forward
        assert calls[1][0][0] == -100  # backward
        assert calls[2][0][0] == 0  # stop
        # Verify sleep was called twice
        assert mock_dependencies['mock_time'].sleep.call_count == 2
    
    def test_doTricks_method_trick2(self, mock_dependencies):
        """Test doTricks with trick 2 (turn clockwise)."""
        from atom_command_interface import Command
        
        cmd = Command()
        cmd.doTricks(2)
        
        # Verify turn_clockwise was called twice
        assert mock_dependencies['mock_drive'].turn_clockwise.call_count == 2
        calls = mock_dependencies['mock_drive'].turn_clockwise.call_args_list
        assert calls[0][0][0] == 100  # turn
        assert calls[1][0][0] == 0  # stop
        # Verify sleep was called once
        assert mock_dependencies['mock_time'].sleep.call_count == 1
    
    def test_doTricks_method_trick3(self, mock_dependencies):
        """Test doTricks with trick 3 (turn counter-clockwise)."""
        from atom_command_interface import Command
        
        cmd = Command()
        cmd.doTricks(3)
        
        # Verify turn_counter_clockwise was called twice
        assert mock_dependencies['mock_drive'].turn_counter_clockwise.call_count == 2
        calls = mock_dependencies['mock_drive'].turn_counter_clockwise.call_args_list
        assert calls[0][0][0] == 100  # turn
        assert calls[1][0][0] == 0  # stop
        # Verify sleep was called once
        assert mock_dependencies['mock_time'].sleep.call_count == 1
    
    def test_doTricks_method_trick4(self, mock_dependencies):
        """Test doTricks with trick 4 (play sound)."""
        from atom_command_interface import Command
        
        cmd = Command()
        cmd.doTricks(4)
        
        # Verify play was called on drive interface
        assert mock_dependencies['mock_drive'].play.called
        # Verify play was called with argument 2
        assert mock_dependencies['mock_drive'].play.call_args[0][0] == 2
    
    def test_speak_method(self, mock_dependencies):
        """Test the speak method loads and plays audio."""
        from atom_command_interface import Command
        
        cmd = Command()
        cmd.speak(5)
        
        # Verify mixer.music.load was called with correct path
        expected_path = '/home/pi/Desktop/FamilyPet/audio/5.mp3'
        assert mock_dependencies['mock_mixer'].music.load.called
        assert mock_dependencies['mock_mixer'].music.load.call_args[0][0] == expected_path
        # Verify mixer.music.play was called
        assert mock_dependencies['mock_mixer'].music.play.called


class TestCommandIntegration:
    """Integration tests for Command class workflow."""
    
    @pytest.fixture(autouse=True)
    def mock_dependencies(self):
        """Mock all hardware dependencies before each test."""
        with patch('atom_command_interface.adt') as mock_adt:
            with patch('atom_command_interface.mixer') as mock_mixer:
                with patch('atom_command_interface.time') as mock_time:
                    mock_drive = Mock()
                    mock_adt.Create2.return_value = mock_drive
                    mock_mixer.init.return_value = None
                    mock_mixer.music.set_volume.return_value = None
                    mock_mixer.music.load.return_value = None
                    mock_mixer.music.play.return_value = None
                    mock_time.sleep.return_value = None
                    
                    yield {
                        'mock_drive': mock_drive,
                        'mock_mixer': mock_mixer,
                        'mock_time': mock_time,
                        'mock_adt': mock_adt
                    }
    
    def test_full_workflow(self, mock_dependencies):
        """Test a complete workflow: start, do tricks, speak, stop."""
        from atom_command_interface import Command
        
        cmd = Command()
        
        # Start the robot
        cmd.start()
        assert mock_dependencies['mock_drive'].start.called
        
        # Do a trick
        cmd.doTricks(1)
        assert mock_dependencies['mock_drive'].drive_straight.called
        
        # Speak a message
        cmd.speak(10)
        assert mock_dependencies['mock_mixer'].music.load.called
        
        # Stop the robot
        cmd.stop()
        assert mock_dependencies['mock_drive'].stop.called
    
    def test_command_state_persistence(self, mock_dependencies):
        """Test that Command maintains state across multiple operations."""
        from atom_command_interface import Command
        
        cmd = Command()
        
        # Perform multiple operations
        cmd.start()
        cmd.goHome()
        cmd.doTricks(2)
        cmd.stop()
        
        # Verify all operations were called
        assert mock_dependencies['mock_drive'].start.called
        assert mock_dependencies['mock_drive'].seek_dock.called
        assert mock_dependencies['mock_drive'].turn_clockwise.called
        assert mock_dependencies['mock_drive'].stop.called
