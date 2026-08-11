import json
import random
import re
from src.renderer.display import CELL_SIZE
from typing import Any
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    model_validator,
    ValidationInfo)

from .error import PacManError

COMMENT_RE = re.compile(r"#|//|;")

SEED_MIN = 1
SEED_MAX = 9999999


def random_seed() -> int:
    """Draws a seed the maze generator accepts.

    Used whenever a level comes without a usable 'seed', so two levels
    of the same size do not end up on the very same maze.
    """
    return random.randint(SEED_MIN, SEED_MAX)


# ------------------------------------------------------------#

def get_int(data: dict[str, Any], key: str, default: int) -> int:
    value = data.get(key, default)

    try:
        return int(value)
    except (TypeError, ValueError):
        print(f"\033[33m[Warning]\033[0m {key}, value '{value}' not an int. \
{key} set to {default}")
        return default

# ------------------------------------------------------------#


class ConfigError(PacManError):
    """Raised when the configuration file cannot be read or used."""


# ------------------------------------------------------------#

class DuplicateConfigKeyError(ConfigError):
    """Raised when a JSON object in the config repeats the same key."""

    def __init__(self, path: str, key: str) -> None:
        super().__init__(
            f"{path}: duplicate key {key!r} in configuration "
            "(e.g. two 'width' or two 'height' entries in the same level)."
        )
        self.path = path
        self.key = key

# ------------------------------------------------------------#


def check_int(
    data: dict[str, Any],
    key: str,
    default: int,
    minimum: int | None = None,
    maximum: int | None = None,
    *,
    clamp: bool = False,
    note: str = "",
) -> None:
    """Lit `key` comme un int, le remet dans les bornes, prévient si besoin.

    Hors bornes, la valeur retombe sur `default`, ou sur la borne franchie
    si `clamp`. `note` est ajouté en fin d'avertissement.
    """
    value = get_int(data, key, default)
    too_low = minimum is not None and value < minimum
    too_high = maximum is not None and value > maximum
    if too_low:
        new_value = minimum if clamp else default
    elif too_high:
        new_value = maximum if clamp else default
    else:
        new_value = value
    data[key] = new_value
    if new_value != value:
        bound = f"< {minimum}" if too_low else f"> {maximum}"
        print(f"\033[33m[Warning]\033[0m '{key}': {value} {bound}. "
              f"'{key}' set to {new_value}{note}")


def check_str(data: dict[str, Any], key: str, default: str) -> None:
    value = data.get(key, default)
    if not isinstance(value, str):
        print(f"\033[33m[Warning]\033[0m '{key}': '{value}' not a str. "
              f"'{key}' set to '{default}'")
        value = default
    data[key] = value


# ------------------------------------------------------------#


class Level(BaseModel):
    """One playable level of the game."""

    model_config = ConfigDict(extra="forbid")

    width: int = 20
    height: int = 20
    seed: int = Field(default_factory=random_seed, ge=SEED_MIN)
    pacgum: int = -1

    @model_validator(mode="before")
    @classmethod
    def fallback(cls, data: Any, info: ValidationInfo) -> Any:
        if not isinstance(data, dict):
            return data

        data = data.copy()
        context = info.context or {}
        screen_width = context.get("screen_width", 1280)
        if screen_width < 1280:
            screen_width = 1280
        screen_height = context.get("screen_height", 720)
        if screen_height < 720:
            screen_height = 720
        max_width = screen_width // CELL_SIZE - 4
        max_height = screen_height // CELL_SIZE - 4
        check_int(data, "width", 20, 10, max_width, clamp=True)
        check_int(data, "height", 20, 10, max_height, clamp=True)
        nb_pacgum = data["width"] * data["height"]
        pacgum = get_int(data, "pacgum", nb_pacgum)
        data["pacgum"] = pacgum if pacgum >= 1 else nb_pacgum
        if data["pacgum"] != pacgum:
            print(f"\033[33m[Warning]\033[0m 'pacgum': {pacgum} < 1 \
defaul behevior(100% of the maze)")
        return data

# ------------------------------------------------------------#


class Config(BaseModel):
    """Whole content of the configuration file."""
    model_config = ConfigDict(extra="forbid")

    highscore_filename: str = "data/scores.json"
    lives: int = 3
    level_max_time: int = 120
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 50
    points_per_ghost: int = 200
    max_nb_level: int = 10
    levels: list[Level] = Field(default_factory=lambda: [Level()])

    @model_validator(mode="before")
    @classmethod
    def fallback(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        data = data.copy()
        check_str(data, "highscore_filename", "data/scores.json")
        check_int(data, "lives", 3, minimum=1)
        check_int(data, "level_max_time", 120, minimum=1)
        check_int(data, "points_per_pacgum", 10, minimum=0)
        check_int(data, "points_per_super_pacgum", 50, minimum=0)
        check_int(data, "points_per_ghost", 200, minimum=0)
        check_int(data, "max_nb_level", 10, minimum=1)
        if not data.get("levels"):
            data["levels"] = [Level(width=20, height=20)]
        return data

# ------------------------------------------------------------#


def strip_comments(text: str) -> str:
    """Cuts every line at its first comment marker.

    Lines are never removed, only shortened, so the line numbers reported
    by the JSON parser still point at the right line of the file. What is
    left is not checked here: `json.loads` is the one that decides
    whether the result is still valid JSON.
    """
    return "\n".join(
        COMMENT_RE.split(line, maxsplit=1)[0]
        for line in text.splitlines()
    )


# ------------------------------------------------------------#

def format_errors(exc: ValidationError) -> str:
    """Turns a pydantic error into one readable line per bad key."""
    lines = []
    for error in exc.errors():
        key = ".".join(str(part) for part in error["loc"])
        lines.append(f"  - {key or '<root>'}: {error['msg']}")
    return "\n".join(lines)


# ------------------------------------------------------------#

def load_config(path: str, screen_width: int,
                screen_height: int) -> Config:
    """Reads `path` and returns the validated configuration.

    Raises:
        ConfigError: if the file is missing, unreadable, not valid JSON,
            or holds a value the game cannot use. The message always says
            which key is wrong.
    """
    try:
        with open(path, encoding="utf-8") as file:
            raw = file.read()
    except OSError as exc:
        raise ConfigError(
            f"cannot open {path!r}: {exc.strerror}.") from exc

    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict[str, Any]:
        seen: set[str] = set()
        result = {}
        for key, value in pairs:
            if key in seen:
                print(f"\033[33m[Warning]\033[0m \
Duplicate key '{key}' detected, '{key}': {value} ignored")
            else:
                seen.add(key)
                result[key] = value
        return result

    try:
        data = json.loads(
            strip_comments(raw), object_pairs_hook=reject_duplicates)
    except json.JSONDecodeError as exc:
        raise ConfigError(
            f"{path}:{exc.lineno}: invalid JSON: {exc.msg}.") from exc
    if not isinstance(data, dict):
        raise ConfigError(
            f"{path}: expected a JSON object at the top level, "
            f"found {type(data).__name__}.")
    try:
        return Config.model_validate(
            data,
            context={
                "screen_width": screen_width,
                "screen_height": screen_height,
            },
            extra="ignore",
        )
    except ValidationError as exc:
        raise ConfigError(
            f"invalid configuration in {path}:\n{format_errors(exc)}"
        ) from exc
