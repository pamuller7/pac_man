"""Package root.

Nothing heavy is imported here: `src.player` must stay usable (and
testable) without pulling pygame in through `src.engine`. The public
names below are resolved on first access instead (PEP 562).
"""

from importlib import import_module
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # for type checkers only, never at runtime
    from .engine import Engine  # noqa: F401
    from .player import Player, Scoreboard  # noqa: F401
    from .renderer import press_start  # noqa: F401

_LAZY_NAMES = {
    "Engine": ".engine",
    "press_start": ".renderer",
    "Player": ".player",
    "Scoreboard": ".player",
}

__all__ = ["entities", "renderer", "engine", "player",
           "Engine", "press_start", "Player", "Scoreboard"]


def __getattr__(name: str):
    """Imports the owning submodule the first time `name` is used.

    Raises:
        AttributeError: if `name` is not one of the exported names.
    """
    module = _LAZY_NAMES.get(name)
    if module is None:
        raise AttributeError(
            f"module {__name__!r} has no attribute {name!r}")
    value = getattr(import_module(module, __name__), name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(__all__)
