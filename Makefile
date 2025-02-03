SHELL := /usr/bin/env bash
PYTHON := python
OS := $(shell python -c "import sys; print(sys.platform)")

ifeq ($(OS),win32)
	PYTHONPATH := $(shell python -c "import os; print(os.getcwd())")
    TEST_COMMAND := set PYTHONPATH=$(PYTHONPATH) && poetry run pytest -c pyproject.toml --cov-report=html --cov=gcop tests/
else
	PYTHONPATH := `pwd`
    TEST_COMMAND := PYTHONPATH=$(PYTHONPATH) poetry run pytest -c pyproject.toml --cov-report=html --cov=gcop tests/
endif

.PHONY: lock install  polish-codestyle formatting test check-codestyle lint docker-build docker-remove cleanup help

lock:
	poetry lock -n && poetry export --without-hashes > requirements.txt

install:
	poetry lock -n && poetry export --without-hashes > requirements.txt
	poetry install -n

polish-codestyle:
	poetry run ruff format --config pyproject.toml .
	poetry run ruff check --fix --config pyproject.toml .

format: polish-codestyle

test:
	$(TEST_COMMAND)

check-codestyle:
	poetry run ruff format --check --config pyproject.toml .
	poetry run ruff check --config pyproject.toml .

lint: test check-codestyle

run-docs:
	cd docs && npm run docs:dev

help:
	@echo "lock                                      Lock the dependencies."
	@echo "install                                   Install the project dependencies."
	@echo "polish-codestyle                          Format the codebase."
	@echo "test                                      Run the tests."
	@echo "format                                    Format the codebase."
	@echo "check-codestyle                           Check the codebase for style issues."
	@echo "lint                                      Run the tests and check the codebase for style issues."
