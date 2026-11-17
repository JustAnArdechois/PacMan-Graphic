PYTHON = python3
CONFIG = config.json

.PHONY: install run debug clean lint lint-strict
install:
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install ./mazegenerator-2.1.0-py3-none-any.whl
run:
	$(PYTHON) pac-man.py $(CONFIG)
debug:
	$(PYTHON) -m pdb pac-man.py $(CONFIG)
clean:
	find . -type d \( -name __pycache__ -o -name .mypy_cache -o -name .pytest_cache \) -prune -exec rm -rf {} +
lint:
	flake8 . --exclude=__pycache__,.mypy_cache,.pytest_cache,.venv
	mypy . --exclude=__pycache__,.mypy_cache,.pytest_cache,.venv
lint-strict:
	flake8 . --exclude=__pycache__,.mypy_cache,.pytest_cache,.venv
	mypy . --strict --exclude=__pycache__,.mypy_cache,.pytest_cache,.venv
