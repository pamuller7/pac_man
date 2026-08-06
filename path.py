from pathlib import Path
import sys


def resource_path(relative_path: str) -> str:
    """
    Return the absolute path to a bundled resource.

    Works both when running from source and when packaged with
    PyInstaller.
    """
    base_path = Path(
        getattr(sys, "_MEIPASS", Path(__file__).resolve().parent)
    )
    return str(base_path / relative_path)
