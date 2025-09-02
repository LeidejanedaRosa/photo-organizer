.PHONY: install format lint test clean help

PYTHON := python3
PIP := $(PYTHON) -m pip
VENV := venv
VENV_BIN := $(VENV)/bin
ACTIVATE := . $(VENV_BIN)/activate

help:
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements-dev.txt

format:
	@echo "🎨 Formatando código..."
	black --line-length=79 .
	isort --profile=black --line-length=79 .
	@echo "✅ Formatação concluída!"

lint:
	@echo "🔍 Executando linting..."
	flake8 .
	@echo "✅ Linting concluído!"

format-check:
	@echo "🔍 Verificando formatação..."
	black --check --line-length=79 .
	isort --check-only --profile=black --line-length=79 .

pre-commit-install:
	pre-commit install
	@echo "✅ Pre-commit hooks instalados!"

pre-commit-run:
	pre-commit run --all-files

test:
	@echo "🧪 Executando testes..."
	$(PYTHON) -m pytest tests/ -v

clean:
	@echo "🧹 Limpando arquivos temporários..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@echo "✅ Limpeza concluída!"

setup-dev: install pre-commit-install
	@echo "🚀 Ambiente de desenvolvimento configurado!"

check-all: format-check lint
	@echo "✅ Todas as verificações passaram!"

run:
	$(PYTHON) main.py
