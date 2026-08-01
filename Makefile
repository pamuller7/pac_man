MODULE := src

SHELL := /bin/bash



install:
	uv sync
	uv pip install mazegenerator-2.1.0-py3-none-any.whl


run:
	uv run pac-man.py config.json


debug:
	@echo "debugging..."


clean:
	@echo "cleaning..."
	@rm -rf src/__pycache__ src/*/__pycache__/ .venv src/renderer/screen_menu/__pycache__ data .mypy_cache


lint:
	@echo "linting..."
	flake8 src
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs


lint-strict:
	@echo "linting strictly..."


.PHONY: install run debug clean lint lint-strict
