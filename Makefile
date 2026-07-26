MODULE := src

SHELL := /bin/bash



install:
	uv sync


run:
	uv run pacman.py


debug:
	@echo "debugging..."


clean:
	@echo "cleaning..."
	@rm -rf src/__pycache__ src/*/__pycache__/ .venv


lint:
	@echo "linting..."


lint-strict:
	@echo "linting strictly..."


.PHONY: install run debug clean lint lint-strict
