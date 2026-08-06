from pathlib import Path
import sys


def resource_path(relative_path: str) -> str:
    """
    small function to translate a relative path to into complete
    one for pyinstaller
    """
    base_path = Path(
        getattr(sys, "_MEIPASS", Path(__file__).resolve().parent)
    )
    return str(base_path / relative_path)
