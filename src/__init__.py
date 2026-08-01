"""Package root.

Nothing heavy is imported here: `src.player` must stay usable (and
testable) without pulling pygame in through `src.engine`. The public
names below are resolved on first access instead (PEP 562).
"""

from importlib import import_module
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .config import Config, ConfigError, Level, load_config
    from .engine import Engine
    from .player import Player, Scoreboard
    from .renderer import press_start

_LAZY_NAMES = {
    "Engine": ".engine",
    "press_start": ".renderer",
    "Player": ".player",
    "Scoreboard": ".player",
    "Config": ".config",
    "ConfigError": ".config",
    "Level": ".config",
    "load_config": ".config",
}

__all__ = ["entities", "renderer", "engine", "player", "config",
           "Engine", "press_start", "Player", "Scoreboard",
           "Config", "ConfigError", "Level", "load_config"]


def __getattr__(name: str) -> Any:
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
