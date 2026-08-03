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

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from .error import PacManError

COMMENT_RE = re.compile(r"#|//|;")


class ConfigError(PacManError):
    """Raised when the configuration file cannot be read or used."""


class Level(BaseModel):
    """One playable level of the game."""

    model_config = ConfigDict(extra="forbid")

    width: int = Field(20, gt=0, description="maze width, in cells")
    height: int = Field(10, gt=0, description="maze height, in cells")
    pacgum: int = Field(10000, gt=0, description="pacgums to eat to win")


class Config(BaseModel):
    """Whole content of the configuration file."""

    model_config = ConfigDict(extra="forbid")

    highscore_filename: str = "data/scores.json"
    level_max_time: int = Field(90, ge=1)
    pacgum: int = Field(1, ge=1)
    lives: int = Field(3, gt=0)
    points_per_pacgum: int = Field(10, ge=0)
    points_per_super_pacgum: int = Field(50, ge=0)
    points_per_ghost: int = Field(200, ge=0)
    levels: list[Level] = Field(
        default_factory=lambda: [Level()],
        min_length=1,
    )


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
