MODULE := src

SHELL := /bin/bash



install:
	uv sync
	uv pip install mazegenerator-2.1.0-py3-none-any.whl


run: install
	uv run pac-man.py config.json


debug:
	@echo "debugging..."


clean:
	@echo "cleaning..."
	@rm -rf src/__pycache__ src/*/__pycache__/ .venv src/renderer/screen_menu/__pycache__ data .mypy_cache


lint:
	@echo "linting..."
	flake8 src pac-man.py
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs


lint-strict:
	@echo "linting strictly..."
	mypy . --strict --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs


.PHONY: install run debug clean lint lint-strict
