"""Game configuration: reads and validates the JSON config file.

The file is plain JSON with one extra rule: `#`, `//` and `;` start a
comment that runs to the end of the line. What comes before it on the
line is kept, so a comment can sit after a value. Every key is optional,
the defaults below are used when a key is missing.

This module never imports pygame: the config must be readable (and the
program must be able to fail cleanly) before any window is opened.
"""

import json
import re

from typing import Self, Any
from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from .error import PacManError

COMMENT_RE = re.compile(r"#|//|;")


def get_int(data: dict[str, Any], key: str, default: int) -> int:
    value = data.get(key, default)

    try:
        return int(value)
    except (TypeError, ValueError):
        print(f"Warning for {key}, value '{value}' not an int. {key} set to {default}")
        return default


class ConfigError(PacManError):
    """Raised when the configuration file cannot be read or used."""


class Level(BaseModel):
    """One playable level of the game."""

    model_config = ConfigDict(extra="forbid")

    width: int = 15
    height: int = 15
    seed: int = 42

    @model_validator(mode="before")
    @classmethod
    def fallback(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        data = data.copy()

        width = get_int(data, "width", 15)
        data["width"] = max(15, min(width, 60))
        if data["width"] != width:
            print(f"Warning for 'width': {width} not between 15 and 60. \
'width' set to {data["width"]}")

        height = get_int(data, "height", 15)
        data["height"] = max(15, min(height, 30))
        if data["height"] != height:
            print(f"Warning for 'height': {height} not between 15 and 60.\
 'height' set to {data["height"]}")

        seed = get_int(data, "seed", 42)
        data["seed"] = seed if seed >= 0 else 42
        if data["seed"] != seed:
            print(f"Warning for 'seed': {seed} < 0. 'seed' set to {data["seed"]}")
        return data


class Config(BaseModel):
    """Whole content of the configuration file."""
    model_config = ConfigDict(extra="forbid")

    highscore_filename: str = "data/scores.json"
    lives: int = 3
    level_max_time: int = 90
    pacgum: int = -1
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
        lives = get_int(data, "lives", 3)
        data["lives"] = lives if lives > 0 else 3
        if data["lives"] != lives:
            print(f"Warning for 'lives': {lives} < 0. 'lives' set to {data["lives"]}")

        level_max_time = get_int(data, "level_max_time", 90)
        data["level_max_time"] = level_max_time if level_max_time >= 1 else 90
        if data["level_max_time"] != level_max_time:
            print(f"Warning for 'level_max_time': {level_max_time} < 1. \
'level_max_time' set to {data["level_max_time"]}")

        pacgum = get_int(data, "pacgum", -1)
        data["pacgum"] = pacgum if pacgum >= 1 else -1
        if data["pacgum"] != pacgum:
            print(f"Warning for 'pacgum': {pacgum} < 1. \
'pacgum' set to {data["pacgum"]}")

        points_per_pacgum = get_int(data, "points_per_pacgum", 10)
        data["points_per_pacgum"] = (points_per_pacgum
                                     if points_per_pacgum >= 0 else 10)
        if data["points_per_pacgum"] != points_per_pacgum:
            print(f"Warning for 'points_per_pacgum': \
{points_per_pacgum} < 0. 'points_per_pacgum' set \
to {data["points_per_pacgum"]}")

        points_per_super_pacgum = get_int(data, "points_per_super_pacgum", 50)
        data["points_per_super_pacgum"] = (
            points_per_super_pacgum if points_per_super_pacgum >= 0 else 50
        )
        if data["points_per_super_pacgum"] != points_per_super_pacgum:
            print(f"Warning for 'points_per_super_pacgum': \
{points_per_super_pacgum} < 0. 'points_per_super_pacgum' set \
to {data["points_per_super_pacgum"]}")

        points_per_ghost = get_int(data, "points_per_ghost", 200)
        data["points_per_ghost"] = (points_per_ghost
                                    if points_per_ghost >= 0 else 200)
        if data["points_per_ghost"] != points_per_ghost:
            print(f"Warning for 'points_per_ghost': \
{points_per_ghost} < 0. 'points_per_ghost' set \
to {data["points_per_ghost"]}")

        max_nb_level = get_int(data, "max_nb_level", 10)
        data["max_nb_level"] = max_nb_level if max_nb_level >= 1 else 10
        if data["max_nb_level"] != max_nb_level:
            print(f"Warning for 'max_nb_level': \
{max_nb_level} < 0. 'max_nb_level' set \
to {data["max_nb_level"]}")

        if not data.get("levels"):
            data["levels"] = [Level(width=20, height=20)]
        return data


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


def format_errors(exc: ValidationError) -> str:
    """Turns a pydantic error into one readable line per bad key."""
    lines = []
    for error in exc.errors():
        key = ".".join(str(part) for part in error["loc"])
        lines.append(f"  - {key or '<root>'}: {error['msg']}")
    return "\n".join(lines)


def load_config(path: str) -> Config:
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
    try:
        data = json.loads(strip_comments(raw))
    except json.JSONDecodeError as exc:
        raise ConfigError(
            f"{path}:{exc.lineno}: invalid JSON: {exc.msg}.") from exc
    if not isinstance(data, dict):
        raise ConfigError(
            f"{path}: expected a JSON object at the top level, "
            f"found {type(data).__name__}.")
    try:
        return Config.model_validate(data, extra="ignore")
    except ValidationError as exc:
        raise ConfigError(
            f"invalid configuration in {path}:\n{format_errors(exc)}"
        ) from exc
