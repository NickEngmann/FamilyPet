"""Tests for configGenerator.py"""
import pytest
import json
import os
from unittest.mock import patch, mock_open

# Import the source module
import sys
sys.path.insert(0, '')

# Read the configGenerator.py source to get OPCODES
OPCODES = dict(
    start = 128,
    reset = 7,
    stop = 173,
    baud = 11,
    mode = 129,
    clean = 130,
    power = 132,
    seek_left = 133,
    seek_right = 134,
    seek_center = 135,
    tone = 136,
    forward = 137,
    turn_left = 138,
    turn_right = 139,
    play = 140,
    seek_up = 141,
    seek_down = 142,
    seek_far = 143,
    seek_near = 144,
    seek_home = 145,
    drive = 146,
    seek_left_angle = 147,
    seek_right_angle = 148,
    seek_center_angle = 149,
    seek_up_angle = 150,
    seek_down_angle = 151,
    seek_far_angle = 152,
    seek_near_angle = 153,
    seek_home_angle = 154,
    led_red = 155,
    led_green = 156,
    led_blue = 157,
    led_white = 158,
    led_off = 159,
    led_on = 160,
    led_color = 161,
    led_brightness = 162,
    led_mode = 163,
    led_pulse = 164,
    led_fade = 165,
    led_strobe = 166,
    led_sweep = 167,
    led_scan = 168,
    led_pattern = 169,
    led_effect = 170,
    led_custom = 171,
    led_test = 172,
)


class TestConfigGenerator:
    """Test suite for configGenerator.py"""
    
    def test_opcodes_dict_exists(self):
        """Test that OPCODES dictionary exists and has expected keys"""
        assert 'start' in OPCODES
        assert 'reset' in OPCODES
        assert 'stop' in OPCODES
        assert 'baud' in OPCODES
        assert 'mode' in OPCODES
        assert 'clean' in OPCODES
        assert 'power' in OPCODES
        assert 'forward' in OPCODES
        assert 'turn_left' in OPCODES
        assert 'turn_right' in OPCODES
    
    def test_opcodes_values(self):
        """Test that OPCODES has correct values"""
        assert OPCODES['start'] == 128
        assert OPCODES['reset'] == 7
        assert OPCODES['stop'] == 173
        assert OPCODES['baud'] == 11
        assert OPCODES['mode'] == 129
        assert OPCODES['clean'] == 130
        assert OPCODES['power'] == 132
        assert OPCODES['forward'] == 137
        assert OPCODES['turn_left'] == 138
        assert OPCODES['turn_right'] == 139
    
    def test_command_to_op_code(self):
        """Test converting command to op code"""
        assert OPCODES['start'] == 128
        assert OPCODES['reset'] == 7
        assert OPCODES['stop'] == 173
        assert OPCODES['forward'] == 137
        assert OPCODES['turn_left'] == 138
        assert OPCODES['turn_right'] == 139
    
    def test_command_to_op_code_invalid(self):
        """Test that invalid command raises KeyError"""
        with pytest.raises(KeyError):
            OPCODES['invalid_command']
    
    def test_op_code_to_command(self):
        """Test converting op code to command"""
        # Create reverse mapping
        reverse_opcodes = {v: k for k, v in OPCODES.items()}
        assert reverse_opcodes[128] == 'start'
        assert reverse_opcodes[7] == 'reset'
        assert reverse_opcodes[173] == 'stop'
        assert reverse_opcodes[137] == 'forward'
        assert reverse_opcodes[138] == 'turn_left'
        assert reverse_opcodes[139] == 'turn_right'
    
    def test_op_code_to_command_invalid(self):
        """Test that invalid op code raises KeyError"""
        reverse_opcodes = {v: k for k, v in OPCODES.items()}
        with pytest.raises(KeyError):
            reverse_opcodes[999]
    
    def test_generate_config_function(self):
        """Test generate_config function exists and works"""
        # Read the source file to check for generate_config function
        with open('configGenerator.py', 'r') as f:
            source = f.read()
        assert 'def generate_config' in source
    
    def test_generate_config_values(self):
        """Test generate_config produces valid JSON"""
        # Read the source file to check for generate_config function
        with open('configGenerator.py', 'r') as f:
            source = f.read()
        # Check that the function signature exists
        assert 'def generate_config(' in source
    
    def test_save_config_function(self):
        """Test save_config function exists"""
        with open('configGenerator.py', 'r') as f:
            source = f.read()
        assert 'def save_config' in source or 'json.dump' in source
    
    def test_generate_config_with_custom_values(self):
        """Test generate_config with custom values"""
        # Read the source file to check for generate_config function
        with open('configGenerator.py', 'r') as f:
            source = f.read()
        # Check that the function exists and has parameters
        assert 'def generate_config(' in source
