# MARISOL.md — Pipeline Context for FamilyPet

## Pipeline History
- *2026-03-11* — Implement: Initial project setup with Roomba hardware control interfaces
- *2026-03-11* — Implement: Improve: test_atom_state_machine.py, atom_state_machine.py
- *2026-03-12* — Implement: Improve: test_atom_command_interface.py, test_atom_state_machine.py, embedded_mocks.py
- *2026-03-12* — Implement: All 19 tests pass

## Notes
- **Project**: A hacked Roomba pet project with Alexa integration, state machine, and hardware control interfaces
- **Docker image**: lotus-rpi-python:latest
- **Main components**:
  - atom_state_machine.py: State machine for Roomba control
  - atom_command_interface.py: Command interface connecting sound, wifi, and drive train
  - atom_drive_train.py: Create2 API for Roomba hardware control (1716 lines)
  - atom_sound_interface.py: Sound interface using pygame mixer
  - atom_alexa_interface.py: Alexa command control interface
  - configGenerator.py: Configuration file generator
- **Dependencies**: pygame, firebase, serial (pyserial)
- **Hardware**: Roomba Create 2 robot
- **Test framework**: pytest
- **Install deps**: pip install pytest

## Known Issues
- Tests failed after implementation attempts (see pipeline knowledge)
- Hardware mocks may be needed for testing without physical Roomba
- Some test files may have incomplete coverage

## Build & Run
- **Language**: Python 3.x
- **Framework**: None (custom Roomba control)
- **Docker image**: lotus-rpi-python:latest
- **Install deps**: pip install pytest
- **Run**: No runnable entry point (hardware-dependent)

## Testing
- **Test framework**: pytest
- **Test command**: pytest
- **Hardware mocks needed**: Yes (for testing without physical Roomba)
- **Known test issues**: Some tests failed after implementation changes

---

**CRITICAL: Test Infrastructure Rules**
- All tests require hardware mocks for Roomba Create 2 interface
- pytest is the primary test framework
- Test files should be in tests/ directory
- Mock architecture needed for CI/CD pipeline testing

**Mock Architecture**
- atom_drive_train.py uses serial communication with Roomba
- Tests should mock serial connections
- Use embedded_mocks.py for hardware simulation
- Firebase connections should be mocked in tests

**Python Build System**
- This project uses Python with Roomba Create 2 API
- No PlatformIO build system detected
- Focus on Python-based testing and deployment
