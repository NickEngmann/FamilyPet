import pytest
from unittest.mock import patch, MagicMock, call
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from atom_command_interface import Command
import atom_drive_train as adt
import atom_sound_interface as asi


class TestCommand:
    """Test suite for Command class"""

    @pytest.fixture
    def mock_create2(self):
        """Mock Create2 object"""
        mock = MagicMock()
        mock.turn_clockwise.return_value = None
        mock.turn_counter_clockwise.return_value = None
        mock.stop.return_value = None
        mock.play.return_value = None
        mock.drive_straight.return_value = None
        mock.seek_dock.return_value = None
        mock.clean.return_value = None
        return mock

    @pytest.fixture
    def mock_mixer(self):
        """Mock mixer module"""
        mock = MagicMock()
        mock.music.load.return_value = None
        mock.music.play.return_value = None
        return mock

    @pytest.fixture
    def command_instance(self, mock_create2, mock_mixer):
        """Create a Command instance with all mocks"""
        with patch('atom_command_interface.adt.Create2', return_value=mock_create2):
            with patch('atom_command_interface.mixer', mock_mixer):
                with patch('atom_command_interface.time'):
                    cmd = Command()
                    yield cmd, mock_create2, mock_mixer

    def test_init(self, command_instance):
        """Test Command initialization"""
        cmd, mock_create2, mock_mixer = command_instance
        assert cmd is not None
        assert mock_create2 is not None

    def test_stop(self, command_instance):
        """Test stop method"""
        cmd, mock_create2, mock_mixer = command_instance
        cmd.stop()
        assert mock_create2.stop.called

    def test_cleanUp(self, command_instance):
        """Test cleanUp method"""
        cmd, mock_create2, mock_mixer = command_instance
        cmd.cleanUp()
        assert mock_create2.clean.called

    def test_goHome(self, command_instance):
        """Test goHome method"""
        cmd, mock_create2, mock_mixer = command_instance
        cmd.goHome()
        assert mock_create2.seek_dock.called

    def test_doTricks_trick1(self, command_instance):
        """Test doTricks with trick 1"""
        cmd, mock_create2, mock_mixer = command_instance
        cmd.doTricks(1)
        assert mock_create2.drive_straight.call_count == 3

    def test_doTricks_trick2(self, command_instance):
        """Test doTricks with trick 2"""
        cmd, mock_create2, mock_mixer = command_instance
        cmd.doTricks(2)
        assert mock_create2.turn_clockwise.call_count == 2

    def test_doTricks_trick3(self, command_instance):
        """Test doTricks with trick 3"""
        cmd, mock_create2, mock_mixer = command_instance
        cmd.doTricks(3)
        assert mock_create2.turn_counter_clockwise.call_count == 2

    def test_doTricks_trick4(self, command_instance):
        """Test doTricks with trick 4"""
        cmd, mock_create2, mock_mixer = command_instance
        cmd.doTricks(4)
        assert mock_create2.play.called

    def test_speak(self, command_instance, mock_mixer):
        """Test speak method"""
        cmd, mock_create2, mixer_mock = command_instance
        cmd.speak(5)
        
        assert mixer_mock.music.load.called
        assert mixer_mock.music.play.called
        # Check the audio file path
        expected_path = '/home/pi/Desktop/FamilyPet/audio/5.mp3'
        assert mixer_mock.music.load.call_args[0][0] == expected_path
