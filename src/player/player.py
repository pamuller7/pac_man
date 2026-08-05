"""Player profile: identity and per-player statistics.

This module is deliberately free of pygame so it can be unit tested
without opening a display.
"""

from datetime import datetime
from typing import Any, Dict

from ..error import InvalidNameError

NAME_MAX_LENGTH = 12


class Player:
    """One player profile.

    Holds the name and the stats that survive from one game to the next.
    Scores are stored by the `Scoreboard`, not here.
    """

    def __init__(self, name: str,
                 created_at: str | None = None,
                 games_played: int = 0,
                 best_score: int = 0) -> None:
        """Creates a profile.

        Raises:
            InvalidNameError: if the name is empty or too long.
        """
        self.name = self.clean_name(name)
        self.created_at = created_at or self.format_created_at()
        self.games_played = games_played
        self.best_score = best_score

    def format_created_at(self) -> str:
        self.created_at = datetime.now().isoformat(
            timespec="seconds")
        return datetime.fromisoformat(self.created_at).strftime(
            "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def clean_name(name: str) -> str:
        """Strips and validates a player name.

        Raises:
            InvalidNameError: if the name is empty or longer than
                NAME_MAX_LENGTH once stripped.
        """
        cleaned = name.strip()
        if not cleaned:
            raise InvalidNameError(name, "name is empty")
        if len(cleaned) > NAME_MAX_LENGTH:
            raise InvalidNameError(
                name, f"name is longer than {NAME_MAX_LENGTH} characters")
        return cleaned

    def record(self, score: int) -> bool:
        """Registers the result of one game. True if it is a new record."""
        self.games_played += 1
        if score > self.best_score:
            self.best_score = score
            return True
        return False

    def to_dict(self) -> Dict[str, Any]:
        """Returns the profile as a JSON-serialisable Dict."""
        return {
            "name": self.name,
            "created_at": self.created_at,
            "games_played": self.games_played,
            "best_score": self.best_score,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Player":
        """Rebuilds a profile from `to_dict` output.

        Raises:
            InvalidNameError: if the stored name is not usable.
        """
        return cls(
            data["name"],
            created_at=data.get("created_at"),
            games_played=data.get("games_played", 0),
            best_score=data.get("best_score", 0),
        )

    def __repr__(self) -> str:
        return f"Player({self.name!r}, best_score={self.best_score})"
