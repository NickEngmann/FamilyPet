import pytest
from unittest.mock import patch, MagicMock, call
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def mock_firebase():
    """Mock firebase module"""
    with patch('firebase.firebase') as mock_firebase:
        mock_firebase.Firebase = MagicMock()
        yield mock_firebase


@pytest.fixture
def mock_datetime():
    """Mock datetime module"""
    with patch('atom_state_machine.datetime') as mock_datetime:
        mock_datetime.datetime = MagicMock()
        mock_datetime.datetime.now = MagicMock(return_value=MagicMock())
        yield mock_datetime


@pytest.fixture
def mock_random():
    """Mock random module"""
    with patch('atom_state_machine.random') as mock_random:
        mock_random.randint = MagicMock(return_value=5)
        mock_random.choice = MagicMock(return_value='test_choice')
        yield mock_random


@pytest.fixture
def mock_atom_command_interface():
    """Mock atom_command_interface module"""
    with patch('atom_state_machine.acmdi') as mock_acmdi:
        mock_aci = MagicMock()
        mock_acmdi.AtomCommandInterface = MagicMock(return_value=mock_aci)
        yield mock_acmdi


@pytest.fixture
def mock_state():
    """Mock State class"""
    with patch('atom_state_machine.State') as mock_state:
        mock_state_instance = MagicMock()
        mock_state_instance.name = 'TestState'
        mock_state_instance.update = MagicMock(return_value=None)
        mock_state_instance.transition = MagicMock(return_value=None)
        mock_state.return_value = mock_state_instance
        yield mock_state


class TestStateClasses:
    """Tests for State classes"""
    
    def test_standby_state(self, mock_atom_command_interface, mock_firebase,
                          mock_datetime, mock_random):
        """Test Standby state initialization"""
        from atom_state_machine import Standby
        
        standby = Standby()
        
        # Verify state name is set
        assert standby.name == 'Standby'
        
    def test_active_state(self, mock_atom_command_interface, mock_firebase,
                         mock_datetime, mock_random):
        """Test Active state initialization"""
        from atom_state_machine import Active
        
        active = Active()
        
        # Verify state name is set
        assert active.name == 'Active'
        
    def test_dock_state(self, mock_atom_command_interface, mock_firebase,
                       mock_datetime, mock_random):
        """Test Dock state initialization"""
        from atom_state_machine import Dock
        
        dock = Dock()
        
        # Verify state name is set
        assert dock.name == 'Dock'
        
    def test_search_state(self, mock_atom_command_interface, mock_firebase,
                         mock_datetime, mock_random):
        """Test Search state initialization"""
        from atom_state_machine import Search
        
        search = Search()
        
        # Verify state name is set
        assert search.name == 'Search'
        
    def test_clean_state(self, mock_atom_command_interface, mock_firebase,
                         mock_datetime, mock_random):
        """Test Clean state initialization"""
        from atom_state_machine import Clean
        
        clean = Clean()
        
        # Verify state name is set
        assert clean.name == 'Clean'


class TestStateMachine:
    """Tests for StateMachine class"""
    
    def test_init_default_state(self, mock_atom_command_interface, mock_firebase,
                                mock_datetime, mock_random):
        """Test StateMachine initialization with default state"""
        from atom_state_machine import StateMachine
        
        sm = StateMachine()
        
        # Verify default state is Standby
        assert sm._state.name == 'Standby'
        
    def test_init_with_custom_state(self, mock_atom_command_interface, mock_firebase,
                                   mock_datetime, mock_random):
        """Test StateMachine initialization with custom state"""
        from atom_state_machine import StateMachine, Active
        
        sm = StateMachine(Active())
        
        # Verify custom state is set
        assert sm._state.name == 'Active'
        
    def test_update(self, mock_atom_command_interface, mock_firebase,
                   mock_datetime, mock_random):
        """Test StateMachine update method"""
        from atom_state_machine import StateMachine, Standby
        
        sm = StateMachine(Standby())
        sm.update()
        
        # Verify state update was called
        mock_atom_command_interface.AtomCommandInterface.assert_called()
        
    def test_transition(self, mock_atom_command_interface, mock_firebase,
                       mock_datetime, mock_random):
        """Test StateMachine transition method"""
        from atom_state_machine import StateMachine, Standby, Active
        
        sm = StateMachine(Standby())
        sm.transition(Active())
        
        # Verify state transition occurred
        assert sm._state.name == 'Active'
        
    def test_transition_updates_command_interface(self, mock_atom_command_interface,
                                                 mock_firebase, mock_datetime,
                                                 mock_random):
        """Test that transition updates command interface reference"""
        from atom_state_machine import StateMachine, Standby, Active
        
        sm = StateMachine(Standby())
        next_state = Active()
        sm.transition(next_state)
        
        # Verify command interface was passed to next state
        mock_atom_command_interface.AtomCommandInterface.assert_called()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
