# Photo Organizer

A Python application for organizing and managing photo collections.

## Features

- Photo organization by date, location, or custom criteria
- Duplicate detection and removal
- Metadata extraction and management
- Web interface for easy management

## Development Setup

### Using Docker (Recommended)

1. Build and run with Docker Compose:
```bash
docker-compose up --build
```

2. The application will be available at `http://localhost:8000`

### Local Development

1. Create and activate virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

4. Set up pre-commit hooks:
```bash
pre-commit install
```

5. Run the application:
```bash
python main.py
```

## Development Tools

This project uses the following tools for code quality:

- **Black**: Code formatter (equivalent to Prettier)
- **isort**: Import sorting
- **Flake8**: Linting (equivalent to ESLint)
- **Pre-commit**: Git hooks (equivalent to Husky)
- **pytest**: Testing framework

### Running Code Quality Tools

Format code:
```bash
black .
isort .
```

Run linting:
```bash
flake8
```

Run tests:
```bash
pytest
```

Run all checks:
```bash
pre-commit run --all-files
```

## Project Structure

```
photo-organizer/
├── main.py                 # Application entry point
├── photo_organizer/        # Main package
├── tests/                  # Test files
├── requirements.txt        # Python dependencies
├── pyproject.toml         # Project configuration
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
└── .pre-commit-config.yaml # Pre-commit hooks
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the test suite
5. Submit a pull request

## License

MIT License
