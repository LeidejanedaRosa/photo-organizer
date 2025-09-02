#!/bin/bash

echo "🎨 Formatando código com Black..."
black --line-length=79 .

echo "📦 Organizando imports com isort..."
isort --profile=black --line-length=79 .

echo "🔍 Executando linting com flake8..."
flake8 .

echo "🔎 Verificando tipos com mypy..."
mypy src/

echo "✅ Formatação e linting concluídos!"
