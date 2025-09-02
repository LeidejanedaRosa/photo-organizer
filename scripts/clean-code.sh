#!/bin/bash

# Script para limpeza rápida do código
PYTHON_PATH=".venv/bin/python"

echo "🧹 Limpando código automaticamente..."

echo "🎨 Formatando com Black..."
$PYTHON_PATH -m black --line-length=79 .

echo "📦 Organizando imports com isort..."
$PYTHON_PATH -m isort --profile=black --line-length=79 .

echo "🗑️ Removendo imports não utilizados..."
$PYTHON_PATH -m autoflake --in-place --remove-all-unused-imports --remove-unused-variables --recursive src/

echo "✅ Limpeza concluída!"
echo "💡 Execute './scripts/format-and-lint.sh' para verificação completa."
