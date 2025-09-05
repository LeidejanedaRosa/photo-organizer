#!/bin/bash

# Script para facilitar desenvolvimento com Docker

set -e

COMMAND=${1:-help}

case $COMMAND in
    "build")
        echo "🔨 Construindo imagem Docker..."
        docker compose build dev
        ;;

    "shell")
        echo "🐚 Iniciando shell interativo no container..."
        docker compose run --rm dev /bin/bash
        ;;

    "run")
        shift
        echo "🚀 Executando comando no container: $@"
        docker compose run --rm dev "$@"
        ;;

    "test")
        echo "🧪 Executando testes no container..."
        docker compose run --rm dev python -m pytest tests/ -v
        ;;

    "lint")
        echo "🔍 Executando verificações de código..."
        docker compose run --rm dev flake8 .
        docker compose run --rm dev black --check .
        docker compose run --rm dev isort --check-only .
        ;;

    "format")
        echo "✨ Formatando código..."
        docker compose run --rm dev black .
        docker compose run --rm dev isort .
        ;;

    "install")
        shift
        echo "📦 Instalando pacote: $@"
        docker compose run --rm dev pip install "$@"
        echo "⚠️  Lembre-se de atualizar requirements.txt!"
        ;;

    "start")
        echo "🚀 Iniciando aplicação..."
        docker compose up photo-organizer
        ;;

    "logs")
        echo "📄 Mostrando logs..."
        docker compose logs -f photo-organizer
        ;;

    "stop")
        echo "🛑 Parando containers..."
        docker compose down
        ;;

    "clean")
        echo "🧹 Limpando containers e imagens do projeto..."
        docker compose down -v
        echo "Removendo containers parados..."
        docker container prune -f
        echo "Removendo imagens dangling..."
        docker image prune -f --filter "dangling=true"
        echo "Removendo cache de build..."
        docker builder prune -f

        # Limpeza agressiva apenas com confirmação
        if [ "${FORCE_PRUNE:-}" = "true" ]; then
            echo "⚠️  FORCE_PRUNE=true detectado - executando limpeza agressiva..."
            docker system prune -f --volumes
        else
            echo ""
            echo "💡 Para limpeza mais agressiva (remove TUDO não usado), execute:"
            echo "   FORCE_PRUNE=true $0 clean"
        fi
        ;;

    "help"|*)
        echo "🐳 Docker Development Helper"
        echo "=============================="
        echo ""
        echo "Uso: $0 <comando>"
        echo ""
        echo "Comandos disponíveis:"
        echo "  build     - Constrói a imagem Docker"
        echo "  shell     - Abre shell interativo no container"
        echo "  run       - Executa comando no container"
        echo "  test      - Executa testes"
        echo "  lint      - Verifica qualidade do código"
        echo "  format    - Formata código com black/isort"
        echo "  install   - Instala pacote Python"
        echo "  start     - Inicia a aplicação"
        echo "  logs      - Mostra logs da aplicação"
        echo "  stop      - Para containers"
        echo "  clean     - Limpa containers e imagens dangling (seguro)"
        echo "  help      - Mostra esta ajuda"
        echo ""
        echo "Exemplos:"
        echo "  $0 shell                    # Shell interativo"
        echo "  $0 run python main.py       # Executa a aplicação"
        echo "  $0 test                     # Executa testes"
        echo "  $0 install requests         # Instala biblioteca"
        echo "  $0 clean                    # Limpeza segura"
        echo "  FORCE_PRUNE=true $0 clean   # Limpeza agressiva"
        ;;
esac
