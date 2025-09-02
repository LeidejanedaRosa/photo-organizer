#!/bin/bash

PYTHON_PATH=".venv/bin/python"

echo "🎨 Formatando código com Black..."
$PYTHON_PATH -m black --line-length=79 .

echo "📦 Organizando imports com isort..."
$PYTHON_PATH -m isort --profile=black --line-length=79 .

echo "🧹 Removendo importações não utilizadas com autoflake..."
$PYTHON_PATH -m autoflake --in-place --remove-all-unused-imports --remove-unused-variables --recursive src/

echo "🔍 Executando linting com flake8..."
$PYTHON_PATH -m flake8 src/

echo "🔎 Verificando argumentos não utilizados com pylint..."
$PYTHON_PATH -m pylint src/ --disable=all --enable=unused-import,unused-variable,unused-argument --reports=no

echo "🔍 Verificando código não utilizado com vulture..."
$PYTHON_PATH -m vulture src/ --min-confidence 80

echo "🔎 Verificando tipos com mypy..."
$PYTHON_PATH -m mypy src/

echo "✅ Formatação e linting concluídos!"
