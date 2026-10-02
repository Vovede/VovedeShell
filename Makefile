PYTHON := python3
export PYTHONPATH := src

.PHONY: run test clean

run:
	$(PYTHON) -m shell.main

test:
	$(PYTHON) -m unittest discover -s tests -v

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
