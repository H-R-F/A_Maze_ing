# =============================================================================
# Makefile — Had lfile kay-automatisi l'commandes li katst3mlhom bzzaf
# =============================================================================
#
# Chno khassek tdir fih:
#
#   Khtwa 1: 3rref l'variables f lfou9:
#            PYTHON = python3
#            VENV   = venv
#            PIP    = $(VENV)/bin/pip
#            PY     = $(VENV)/bin/python
#
#   Khtwa 2: Dir target "install" (LAZEM - talbo f l'subject):
#            - Sawb virtual environment:      $(PYTHON) -m venv $(VENV)
#            - Upgraddi pip:                  $(PIP) install --upgrade pip
#            - Installi l'dependencies:       $(PIP) install -r requirements.txt
#            - Installi l'projet editable:    $(PIP) install -e .
#
#   Khtwa 3: Dir target "run" (LAZEM):
#            - Khddem l'programme:  $(PY) a_maze_ing.py config.txt
#
#   Khtwa 4: Dir target "debug" (LAZEM):
#            - Khddem b debugger:   $(PY) -m pdb a_maze_ing.py config.txt
#
#   Khtwa 5: Dir target "lint" (LAZEM - b had l'flags bi dbt mn l'subject):
#            - Khddem flake8:  $(VENV)/bin/flake8 .
#            - Khddem mypy:    $(VENV)/bin/mypy . --warn-return-any
#                               --warn-unused-ignores --ignore-missing-imports
#                               --disallow-untyped-defs --check-untyped-defs
#
#   Khtwa 6: Dir target "lint-strict" (IKHTIYARI — machi lazem, walakin l'subject nss7 bih):
#            - Khddem flake8:  $(VENV)/bin/flake8 .
#            - Khddem mypy:    $(VENV)/bin/mypy . --strict
#
#   Khtwa 7: Dir target "clean" (LAZEM):
#            - Mssa7 __pycache__, .mypy_cache, .pytest_cache
#            - Mssa7 build/, dist/, *.egg-info
#            - Mssa7 ga3 l'fichiers .pyc
#
#   Khtwa 8: Dir target "test" (IKHTIYARI walakin mzyan):
#            - Khddem pytest:  $(PY) -m pytest tests/ -v
#
#   Khtwa 9: Dir target "build" (bach tsawb l'package):
#            - $(PY) -m build
#            - Had chi ghay3tik: dist/mazegen-1.0.0-py3-none-any.whl
#
#   Khtwa 10: F l'akhir, 3llen ga3 l'targets b .PHONY:
#             .PHONY: install run debug clean lint lint-strict test build
# =============================================================================


PYTHON = python3
VENV   = venv
PIP    = $(VENV)/bin/pip
PY     = $(VENV)/bin/python

install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	$(PY) a_maze_ing.py config.txt

debug:
	$(PY) -m pdb a_maze_ing.py config.txt

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache
	rm -rf build dist *.egg-info
	find . -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +

lint:
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

build:
	python3 -m build
	cp ./dist/mazegen-1.0.0-py3-none-any.whl ./
	rm -rf dist

.PHONY: install run debug clean lint