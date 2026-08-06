"""Score board: stores the scores of every player and ranks them.

Like `player`, this module never imports pygame: it only owns data and
its JSON file.
"""

import json
import os

from ..error import ScoreboardCorruptedError
from .player import Player

DEFAULT_PATH = "data/scores.json"


class Scoreboard:
    """Keeps the profiles and their scores, and saves them to a file.

    A missing file is not an error: it simply means an empty board.
    """

    def __init__(self, path: str = DEFAULT_PATH) -> None:
        self.path = path
        self.players: dict[str, Player] = {}
        self.scores: list[tuple[str, int]] = []

    def load(self) -> None:
        """Reads the file. Does nothing if it does not exist yet.

        Raises:
            ScoreboardCorruptedError: if the file is not readable JSON or
                does not have the expected shape.
        """
        if not os.path.exists(self.path):
            return
        try:
            with open(self.path, encoding="utf-8") as file:
                data = json.load(file)
            self.players = {
                entry["name"]: Player.from_dict(entry)
                for entry in data["players"]
            }
            self.scores = [(name, int(score))
                           for name, score in data["scores"]]
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            raise ScoreboardCorruptedError(self.path, str(exc)) from exc

    def save(self) -> None:
        """Writes the board to disk, creating the folder if needed.

        Writes to a temporary file first, so an interrupted save cannot
        leave a half-written score file behind.
        """
        folder = os.path.dirname(self.path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        players = [player.to_dict() for player in self.players.values()]
        players.sort(key=lambda x: x["best_score"])
        if len(players) > 10:
            players.pop(0)
        scores = sorted(self.scores, key=lambda entry: entry[1])
        if len(scores) > 10:
            scores.pop(0)
        data = {
            "players": players,
            "scores": scores,
        }
        tmp_path = f"{self.path}.tmp"
        with open(tmp_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
        print(data)
        os.replace(tmp_path, self.path)

    def get_player(self, name: str) -> Player:
        """Returns the profile named `name`, creating it if needed.

        Raises:
            InvalidNameError: if the name is empty or too long.
        """
        cleaned = Player.clean_name(name)
        if cleaned not in self.players:
            self.players[cleaned] = Player(cleaned)
        return self.players[cleaned]

    def add_score(self, player: Player, score: int) -> bool:
        """Records one game result. True if it is a personal record."""
        self.players.setdefault(player.name, player)
        self.scores.append((player.name, score))
        return player.record(score)

    def top(self, limit: int = 10) -> list[tuple[str, int]]:
        """Returns the `limit` best scores, highest first."""
        return sorted(self.scores, key=lambda entry: entry[1],
                      reverse=True)[:limit]

    def best_of(self, name: str) -> int:
        """Returns the best score of `name`, or 0 if unknown."""
        player = self.players.get(name)
        return player.best_score if player else 0
