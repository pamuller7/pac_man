MODULE := src

SHELL := /bin/bash

INSTALLED = .venv/.installed


install:
	uv sync

run: install
	uv run pac-man.py config.json



debug:
	@echo "debugging..."


clean:
	@echo "cleaning..."
	@rm -rf *__pycache__/ src/__pycache__ src/*/__pycache__/ .venv src/renderer/screen_menu/__pycache__ data .mypy_cache pac-man.spec
	@rm -rf corrupted_scores.txt
	@rm -rf dist build

clean-all: clean
	@rm -rf .venv

lint:
	@echo "linting..."
	uv run flake8 src pac-man.py
	uv run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs


lint-strict:
	@echo "linting strictly..."
	uv run flake8 src pac-man.py
	uv run mypy . --strict --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs


.PHONY: install run debug clean lint lint-strict clean-all
