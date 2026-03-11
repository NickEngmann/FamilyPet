"""Tests for atom_state_machine.py"""

import pytest
from unittest.mock import patch, MagicMock, call
import datetime


class TestStateClasses:
    """Test suite for state machine classes in atom_state_machine.py"""
    
    @pytest.fixture
    def mock_command_interface(self):
        """Create a mock command interface"""
        mock = MagicMock()
        mock.start = MagicMock()
        mock.stop = MagicMock()
        return mock
    
    @pytest.fixture
    def mock_firebase(self):
        """Create a mock firebase interface"""
        mock = MagicMock()
        mock.patch = MagicMock(return_value={})
        return mock
    
    @pytest.fixture
    def mock_state_machine(self, mock_command_interface, mock_firebase):
        """Create a state machine with mocked dependencies"""
        with patch('atom_state_machine.acmdi.Command', return_value=mock_command_interface):
            with patch('atom_state_machine.firebase', mock_firebase):
                from atom_state_machine import StateMachine, Standby, Active, Stop, Tricks
                yield mock_command_interface, mock_firebase
    
    def test_resetStatus_function(self, mock_firebase):
        """Test resetStatus function"""
        with patch('atom_state_machine.firebase.FirebaseApplication', return_value=mock_firebase):
            from atom_state_machine import resetStatus
            resetStatus('standby')
            mock_firebase.patch.assert_called_with('/status', {'command': 'standby'})
    
    def test_resetTime_function(self):
        """Test resetTime function returns current datetime"""
        with patch('atom_state_machine.datetime') as mock_datetime:
            mock_datetime.utcnow.return_value = datetime.datetime(2024, 1, 1, 12, 0, 0)
            from atom_state_machine import resetTime
            result = resetTime()
            assert result == datetime.datetime(2024, 1, 1, 12, 0, 0)
    
    def test_state_base_class(self):
        """Test base State class"""
        from atom_state_machine import State
        state = State()
        assert state.on_event('test') is None
        assert 'State' in str(state)
    
    def test_standby_state_on_event_standby(self, mock_command_interface):
        """Test Standby state when event is standby"""
        from atom_state_machine import Standby
        standby = Standby()
        standby._atom_command_interface = mock_command_interface
        standby._atom_state = MagicMock()
        standby._atom_state._started_at = datetime.datetime.utcnow()
        
        result = standby.on_event({'command': 'standby'})
        assert result is standby
    
    def test_standby_state_on_event_active(self, mock_command_interface):
        """Test Standby state transitions to Active"""
        from atom_state_machine import Standby, Active
        standby = Standby()
        standby._atom_command_interface = mock_command_interface
        standby._atom_state = MagicMock()
        standby._atom_state._started_at = datetime.datetime.utcnow()
        
        result = standby.on_event({'command': 'active'})
        assert isinstance(result, Active)
        mock_command_interface.start.assert_called_once()
    
    def test_active_state_on_event_tricks(self, mock_command_interface):
        """Test Active state transitions to Tricks"""
        from atom_state_machine import Active, Tricks
        active = Active()
        active._atom_command_interface = mock_command_interface
        active._atom_state = MagicMock()
        active._atom_state._started_at = datetime.datetime.utcnow()
        
        result = active.on_event({'command': 'tricks'})
        assert isinstance(result, Tricks)
    
    def test_active_state_on_event_cometome(self, mock_command_interface):
        """Test Active state transitions to comeToMe"""
        from atom_state_machine import Active
        active = Active()
        active._atom_command_interface = mock_command_interface
        active._atom_state = MagicMock()
        active._atom_state._started_at = datetime.datetime.utcnow()
        
        result = active.on_event({'command': 'comeToMe'})
        # Should return a state (comeToMe is a function that returns a state)
        assert result is not None
    
    def test_active_state_on_event_cleanup(self, mock_command_interface):
        """Test Active state transitions to cleanUp"""
        from atom_state_machine import Active
        active = Active()
        active._atom_command_interface = mock_command_interface
        active._atom_state = MagicMock()
        active._atom_state._started_at = datetime.datetime.utcnow()
        
        result = active.on_event({'command': 'cleanUp'})
        assert result is not None
    
    def test_active_state_on_event_speak(self, mock_command_interface):
        """Test Active state transitions to speak"""
        from atom_state_machine import Active
        active = Active()
        active._atom_command_interface = mock_command_interface
        active._atom_state = MagicMock()
        active._atom_state._started_at = datetime.datetime.utcnow()
        
        result = active.on_event({'command': 'speak'})
        assert result is not None
    
    def test_active_state_on_event_gohome(self, mock_command_interface):
        """Test Active state transitions to goHome"""
        from atom_state_machine import Active
        active = Active()
        active._atom_command_interface = mock_command_interface
        active._atom_state = MagicMock()
        active._atom_state._started_at = datetime.datetime.utcnow()
        
        result = active.on_event({'command': 'goHome'})
        assert result is not None
    
    def test_active_state_on_event_stop(self, mock_command_interface):
        """Test Active state transitions to Stop"""
        from atom_state_machine import Active, Stop
        active = Active()
        active._atom_command_interface = mock_command_interface
        active._atom_state = MagicMock()
        active._atom_state._started_at = datetime.datetime.utcnow()
        
        result = active.on_event({'command': 'stop'})
        assert isinstance(result, Stop)
    
    def test_active_state_timeout(self, mock_command_interface):
        """Test Active state timeout after 200 seconds"""
        from atom_state_machine import Active, Standby
        active = Active()
        active._atom_command_interface = mock_command_interface
        active._atom_state = MagicMock()
        # Set started_at to 201 seconds ago
        active._atom_state._started_at = datetime.datetime.utcnow() - datetime.timedelta(seconds=201)
        
        result = active.on_event({'command': 'test'})
        assert isinstance(result, Standby)
        mock_command_interface.stop.assert_called_once()
    
    def test_stop_state_on_event(self, mock_command_interface):
        """Test Stop state transitions to Standby"""
        from atom_state_machine import Stop, Standby
        stop = Stop()
        stop._atom_command_interface = mock_command_interface
        
        result = stop.on_event({'command': 'test'})
        assert isinstance(result, Standby)
        mock_command_interface.stop.assert_called_once()


class TestStateMachine:
    """Test suite for the StateMachine class"""
    
    @pytest.fixture
    def mock_command_interface(self):
        """Create a mock command interface"""
        mock = MagicMock()
        mock.start = MagicMock()
        mock.stop = MagicMock()
        return mock
    
    @pytest.fixture
    def mock_firebase(self):
        """Create a mock firebase interface"""
        mock = MagicMock()
        mock.patch = MagicMock(return_value={})
        return mock
    
    def test_state_machine_initialization(self, mock_command_interface, mock_firebase):
        """Test StateMachine initialization"""
        with patch('atom_state_machine.acmdi.Command', return_value=mock_command_interface):
            with patch('atom_state_machine.firebase', mock_firebase):
                from atom_state_machine import StateMachine
                sm = StateMachine()
                assert sm._atom_command_interface is mock_command_interface
                assert sm._atom_state is not None
    
    def test_state_machine_handle_event(self, mock_command_interface, mock_firebase):
        """Test StateMachine handle_event method"""
        with patch('atom_state_machine.acmdi.Command', return_value=mock_command_interface):
            with patch('atom_state_machine.firebase', mock_firebase):
                from atom_state_machine import StateMachine
                sm = StateMachine()
                sm.handle_event({'command': 'test'})
                # Should process the event without error
                assert True
    
    def test_state_machine_handle_event_transition(self, mock_command_interface, mock_firebase):
        """Test StateMachine handles state transitions"""
        with patch('atom_state_machine.acmdi.Command', return_value=mock_command_interface):
            with patch('atom_state_machine.firebase', mock_firebase):
                from atom_state_machine import StateMachine, Standby, Active
                sm = StateMachine()
                # Start in standby
                assert isinstance(sm._atom_state, Standby)
                
                # Transition to active
                sm.handle_event({'command': 'active'})
                assert isinstance(sm._atom_state, Active)
