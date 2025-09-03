import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from main import main  # noqa: E402


def test_main_function():
    try:
        main()
        assert True
    except Exception as e:
        assert False, f"main() function failed with error: {e}"
