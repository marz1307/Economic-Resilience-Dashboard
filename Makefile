PY ?= python

.PHONY: help install validate lint format test clean

help:
	@echo "Targets:"
	@echo "  install   Install package + dev extras (editable)"
	@echo "  validate  Run scripts/validate_data.py against data/"
	@echo "  lint      Run ruff and black --check on Python sources"
	@echo "  format    Apply black formatting"
	@echo "  test      Run pytest"
	@echo "  clean     Remove caches and build artefacts"

install:
	$(PY) -m pip install -e ".[dev]"

validate:
	$(PY) scripts/validate_data.py --data-dir data

lint:
	ruff check .
	black --check .

format:
	black .
	ruff check . --fix

test:
	pytest

clean:
	rm -rf build dist *.egg-info .pytest_cache .ruff_cache .mypy_cache
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
