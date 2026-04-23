## Dev environment 
- Ensure you have Python 3.12 or higher installed.
- Install required packages using `pip install -r requirements.txt`.
- Set up your virtual environment with `python -m venv venv` and activate it.
- Run tests with `pytest -q` to ensure everything is working correctly.

## Testing instructions
- Run unit tests with `pytest -q` to validate individual components.
- Run integration tests with `pytest -v` to ensure system-level functionality.
- Use coverage reports with `pytest --cov` to assess test comprehensiveness.

## PR Instructions
- Ensure all new code is covered by unit tests.
- Review code for adherence to PEP 8 standards.
- Ensure documentation is updated for new features or changes.
- Address any linting errors reported by `flake8`.
- Ensure code is compatible with Python 3.12 and above.