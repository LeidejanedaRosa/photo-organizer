set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info() { echo -e "${GREEN}[INFO]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; }

check_venv() {
    if [ ! -d ".venv" ]; then
        error "Virtual environment not found. Please run 'make setup' first."
        exit 1
    fi
}

activate_venv() {
    source .venv/bin/activate
}

case "$1" in
    "setup")
        info "Setting up development environment..."
        python3 -m venv .venv
        activate_venv
        pip install --upgrade pip
        pip install -r requirements.txt
        pip install -e ".[dev]"
        pre-commit install
        info "Development environment ready!"
        ;;

    "test")
        info "Running tests..."
        check_venv
        activate_venv
        pytest tests/ -v --cov=photo_organizer
        ;;

    "lint")
        info "Running linters..."
        check_venv
        activate_venv
        flake8
        info "Linting passed!"
        ;;

    "format")
        info "Formatting code..."
        check_venv
        activate_venv
        black .
        isort .
        info "Code formatted!"
        ;;

    "check")
        info "Running all checks..."
        check_venv
        activate_venv
        black --check .
        isort --check-only .
        flake8
        pytest tests/ -v
        info "All checks passed!"
        ;;

    "docker-build")
        info "Building Docker image..."
        docker build -t photo-organizer .
        info "Docker image built successfully!"
        ;;

    "docker-run")
        info "Running application in Docker..."
        docker run --rm -p 8000:8000 photo-organizer
        ;;

    "docker-compose")
        info "Starting with Docker Compose..."
        docker-compose up --build
        ;;

    "clean")
        info "Cleaning up..."
        rm -rf .pytest_cache
        rm -rf htmlcov
        rm -rf .coverage
        rm -rf __pycache__
        find . -name "*.pyc" -delete
        find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
        info "Cleanup completed!"
        ;;

    *)
        echo "Photo Organizer Development Script"
        echo ""
        echo "Usage: $0 {setup|test|lint|format|check|docker-build|docker-run|docker-compose|clean}"
        echo ""
        echo "Commands:"
        echo "  setup           - Set up development environment"
        echo "  test            - Run tests"
        echo "  lint            - Run linters"
        echo "  format          - Format code with black and isort"
        echo "  check           - Run all checks (format, lint, test)"
        echo "  docker-build    - Build Docker image"
        echo "  docker-run      - Run application in Docker"
        echo "  docker-compose  - Start with Docker Compose"
        echo "  clean           - Clean up temporary files"
        exit 1
        ;;
esac
