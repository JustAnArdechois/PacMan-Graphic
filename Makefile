PYTHON = python3

install:
	$(PYTHON) -m pip install pygame ./mazegenerator-2.1.0-py3-none-any.whl

install-bypass-pep_668:
	$(PYTHON) -m pip install --break-system-packages pygame ./mazegenerator-2.1.0-py3-none-any.whl

run:
	$(PYTHON) main.py
