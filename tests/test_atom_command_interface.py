"""Tests for atom_command_interface.py"""

import pytest
from unittest.mock import patch, MagicMock, call


class TestCommandInterface:
    """Test suite for the Command class in atom_command_interface.py"""
    
    @pytest.fixture
    def mock_drive(self):
        """Create a mock drive interface"""
        mock = MagicMock()
        mock.start = MagicMock()
        mock.safe = MagicMock()
        mock.wake = MagicMock()
        mock.stop = MagicMock()
        mock.clean = MagicMock()
        mock.seek_dock = MagicMock()
        mock.drive_straight = MagicMock()
        mock.turn_clockwise = MagicMock()
        mock.turn_counter_clockwise = MagicMock()
        mock.play = MagicMock()
        return mock
    
    @pytest.fixture
    def mock_mixer(self):
        """Create a mock pygame mixer"""
        mock = MagicMock()
        mock.init = MagicMock()
        mock.music = MagicMock()
        mock.music.set_volume = MagicMock()
        mock.music.load = MagicMock()
        mock.music.play = MagicMock()
        return mock
    
    @pytest.fixture
    def command_interface(self, mock_drive, mock_mixer):
        """Create a Command instance with mocked dependencies"""
        with patch('atom_command_interface.adt.Create2', return_value=mock_drive):
            with patch('atom_command_interface.mixer', mock_mixer):
                from atom_command_interface import Command
                cmd = Command()
                cmd._drive = mock_drive
                cmd.mixer = mock_mixer
                yield cmd
    
    def test_init_initializes_drive_and_mixer(self, command_interface, mock_drive, mock_mixer):
        """Test that Command initializes drive and mixer correctly"""
        mock_drive.start.assert_called_once()
        mock_drive.safe.assert_called_once()
        mock_drive.wake.assert_called_once()
        mock_mixer.init.assert_called_once()
        mock_mixer.music.set_volume.assert_called_with(1.0)
    
    def test_start_method(self, command_interface, mock_drive):
        """Test the start method"""
        command_interface.start()
        mock_drive.start.assert_called()
        mock_drive.safe.assert_called()
        mock_drive.wake.assert_called()
    
    def test_stop_method(self, command_interface, mock_drive):
        """Test the stop method"""
        command_interface.stop()
        mock_drive.stop.assert_called_once()
    
    def test_cleanUp_method(self, command_interface, mock_drive):
        """Test the cleanUp method"""
        command_interface.cleanUp()
        mock_drive.clean.assert_called_once()
    
    def test_goHome_method(self, command_interface, mock_drive):
        """Test the goHome method"""
        command_interface.goHome()
        mock_drive.seek_dock.assert_called_once()
    
    def test_doTricks_trick_1(self, command_interface, mock_drive):
        """Test trick 1: drive forward, wait, drive backward, wait, stop"""
        command_interface.doTricks(1)
        mock_drive.drive_straight.assert_has_calls([
            call(100),
            call(-100),
            call(0)
        ])
    
    def test_doTricks_trick_2(self, command_interface, mock_drive):
        """Test trick 2: turn clockwise"""
        command_interface.doTricks(2)
        mock_drive.turn_clockwise.assert_has_calls([
            call(100),
            call(0)
        ])
    
    def test_doTricks_trick_3(self, command_interface, mock_drive):
        """Test trick 3: turn counter-clockwise"""
        command_interface.doTricks(3)
        mock_drive.turn_counter_clockwise.assert_has_calls([
            call(100),
            call(0)
        ])
    
    def test_doTricks_trick_4(self, command_interface, mock_drive, mock_mixer):
        """Test trick 4: play sound"""
        command_interface.doTricks(4)
        mock_drive.play.assert_called_with(2)
    
    def test_doTricks_invalid_trick(self, command_interface, mock_drive):
        """Test with invalid trick number - should do nothing"""
        command_interface.doTricks(99)
        # No methods should be called for invalid trick
        assert mock_drive.drive_straight.call_count == 0
        assert mock_drive.turn_clockwise.call_count == 0
        assert mock_drive.turn_counter_clockwise.call_count == 0
        assert mock_drive.play.call_count == 0
    
    def test_speak_method(self, command_interface, mock_mixer):
        """Test the speak method"""
        command_interface.speak(5)
        mock_mixer.music.load.assert_called_with('/home/pi/Desktop/FamilyPet/audio/5.mp3')
        mock_mixer.music.play.assert_called_once()
