# Backend Test Specification

## 1. Testing Tools and Dependencies

### Pytest

Pytest is a Python testing framework used for writing and running test cases. It is concise, powerful, and supports plugins like `pytest-django` for Django integration and `pytest-cov` for coverage reports.

To install it and related dependencies:

```sh
pip install pytest pytest-django pytest-cov
```

(Already add) To configure Django settings, add a `pytest.ini` file in your project root:

```ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings
python_files = tests.py test_*.py *_tests.py
```

### unittest.mock

The `unittest.mock` module is used to mock out external dependencies such as email sending, transcription models, subprocesses (e.g., ffmpeg), and third-party services. It allows for isolation and simulation of behavior in unit tests.

You can also use `pytest-mock` for cleaner mocking syntax.

### Freezegun

Freezegun is used to "freeze" time during tests involving date comparisons (e.g., cleaning up old files):

```sh
pip install freezegun
```

## 2. Running Unit Tests

### Running All Tests

To run all tests across your backend project:

```sh
pytest
```

This will automatically discover all test files and execute them.

### Running a Specific Test File

To run only one test file:

```sh
pytest tests/test_tasks.py
```

### Viewing Test Coverage

To generate a coverage report:

```sh
pytest --cov=. --cov-report=term-missing --cov-fail-under=70
```

- This prints a terminal summary
- You can also generate an HTML version:

```sh
pytest --cov=. --cov-report=html
```

Open `htmlcov/index.html` in a browser to view a detailed report.

## 3. Unit Testing Goals

- **Ensure View Logic Works**: Verify Django views behave correctly with different inputs and request methods (GET, POST).
- **Mock External Services**: Test email sending, transcription, translation, and clustering without invoking real models or services.
- **Validate Error Handling**: Confirm proper responses for bad input, missing fields, or exceptions.
- **Isolate Components**: Keep tests modular by mocking out database, file system, subprocess, and API dependencies.
- **Enforce File Cleanups**: Confirm expired files or temporary attachments are deleted as expected.
- **Prevent Regressions**: Guard against bugs introduced by new changes using a reliable suite of unit tests.
