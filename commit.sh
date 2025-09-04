#!/bin/bash

# Script para facilitar a criação de commits semânticos
# Uso: ./commit.sh

echo "🎯 Criador de Commits Semânticos"
echo "================================="
echo ""

# Verificar se há mudanças staged
if ! git diff --cached --quiet; then
    echo "✅ Mudanças detectadas no stage"
else
    echo "❌ Nenhuma mudança no stage. Execute 'git add .' primeiro"
    exit 1
fi

echo ""
echo "Selecione o tipo de commit:"
echo "1.  ✨ feat      - Nova funcionalidade"
echo "2.  🐛 fix       - Correção de bug"
echo "3.  📚 docs      - Documentação"
echo "4.  🎨 style     - Formatação de código"
echo "5.  ♻️  refactor - Refatoração"
echo "6.  🧪 test      - Testes"
echo "7.  🔧 chore     - Tarefas de manutenção"
echo "8.  📦 build     - Sistema de build"
echo "9.  🧱 ci        - Integração contínua"
echo "10. ⚡ perf      - Performance"
echo "11. 💥 revert    - Reversão"
echo ""

read -p "Digite o número (1-11): " choice

case $choice in
    1) type="feat" ;;
    2) type="fix" ;;
    3) type="docs" ;;
    4) type="style" ;;
    5) type="refactor" ;;
    6) type="test" ;;
    7) type="chore" ;;
    8) type="build" ;;
    9) type="ci" ;;
    10) type="perf" ;;
    11) type="revert" ;;
    *) echo "❌ Opção inválida"; exit 1 ;;
esac

echo ""
read -p "Escopo (opcional, ex: api, auth, ui): " scope
echo ""
read -p "Descrição do commit: " description

if [ -z "$description" ]; then
    echo "❌ Descrição é obrigatória"
    exit 1
fi

# Construir mensagem de commit
if [ -n "$scope" ]; then
    commit_msg="${type}(${scope}): ${description}"
else
    commit_msg="${type}: ${description}"
fi

echo ""
echo "📝 Mensagem do commit: $commit_msg"
echo ""
read -p "Confirmar commit? (y/N): " confirm

if [[ $confirm =~ ^[Yy]$ ]]; then
    git commit -m "$commit_msg"
    echo "✅ Commit realizado com sucesso!"
else
    echo "❌ Commit cancelado"
fi
