PYTHON = python3

install:
	$(PYTHON) -m pip install pygame ./mazegenerator-2.1.0-py3-none-any.whl

run:
	$(PYTHON) affiche_maze.py
