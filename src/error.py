from typing import Tuple


class PacManError(Exception):
    """Base class for every error raised by the game."""


class MazeError(PacManError):
    """Base class for problems with the maze grid."""


class EmptyMazeError(MazeError):
    """Raised when a maze has no rows or no columns."""

    def __init__(self,
                 message: str = "Maze is empty (no rows or columns)."
                 ) -> None:
        super().__init__(message)


class MalformedMazeError(MazeError):
    """Raised when maze rows do not all share the same length."""

    def __init__(self, expected: int, found: int, row: int) -> None:
        super().__init__(
            f"Maze row {row} has length {found}, expected {expected} "
            "(maze must be rectangular)."
        )
        self.expected = expected
        self.found = found
        self.row = row


class Invalidwindow(MazeError):
    """Raised when the window size is invalid."""

    def __init__(self) -> None:
        super().__init__(
            "Window size is invalid."
        )


class InvalidCellError(MazeError):
    """
    Raised when a maze cell holds a value outside the 0..15 bitmask range.
    """

    def __init__(self, value: int, pos: Tuple[int, int]) -> None:
        super().__init__(
            f"Invalid maze cell value {value} at {pos}; "
            "expected a wall bitmask in range 0..15."
        )
        self.value = value
        self.pos = pos


class NoSpawnError(MazeError):
    """Raised when the maze has no walkable cell to spawn an entity on."""

    def __init__(self,
                 message: str = "No walkable cell found to spawn on."
                 ) -> None:
        super().__init__(message)


class OutOfBoundsError(MazeError):
    """Raised when a position falls outside the maze grid."""

    def __init__(self, pos: Tuple[int, int], size: Tuple[int, int]) -> None:
        super().__init__(
            f"Position {pos} is outside the maze of size {size}."
        )
        self.pos = pos
        self.size = size


class DirectionError(PacManError):
    """Raised when a direction is not one of 'N', 'E', 'S', 'W'."""

    def __init__(self, direction: str) -> None:
        super().__init__(
            f"Invalid direction {direction!r}; \
                expected one of 'N', 'E', 'S', 'W'."
        )
        self.direction = direction


class EntityError(PacManError):
    """Base class for problems with a game entity."""


class InvalidPositionError(EntityError):
    """Raised when an entity is created with negative coordinates."""

    def __init__(self, pos: Tuple[int, int]) -> None:
        super().__init__(
            f"Invalid entity position {pos}; coordinates must be >= 0."
        )
        self.pos = pos


class InvalidHealthError(EntityError):
    """Raised when an entity is created with non-positive hit points."""

    def __init__(self, hp: int) -> None:
        super().__init__(
            f"Invalid hit points {hp}; must be strictly positive."
        )
        self.hp = hp


class InvalidSpeedError(EntityError):
    """Raised when an entity is created with a non-positive speed."""

    def __init__(self, speed: int) -> None:
        super().__init__(
            f"Invalid speed {speed}; must be strictly positive."
        )
        self.speed = speed


class PathNotFoundError(EntityError):
    """Raised when no path exists between an entity and its target."""

    def __init__(self,
                 start: Tuple[int, int],
                 target: Tuple[int, int]) -> None:
        super().__init__(
            f"No path from {start} to {target}."
        )
        self.start = start
        self.target = target


class AssetError(PacManError):
    """Raised when a game asset (image, sound, font) cannot be loaded."""

    def __init__(self, path: str, reason: str = "") -> None:
        detail = f": {reason}" if reason else ""
        super().__init__(f"Failed to load asset {path!r}{detail}.")
        self.path = path
        self.reason = reason


class EngineError(PacManError):
    """Base class for engine / game-loop failures."""


class AssetNotFoundError(AssetError):
    """Raised specifically when an asset file does not exist on disk."""

    def __init__(self, path: str) -> None:
        super().__init__(path, reason="file not found")


class ProfileError(PacManError):
    """Base class for player profile / score board failures."""


class InvalidNameError(ProfileError):
    """Raised when a player name cannot be used as a profile name."""

    def __init__(self, name: str, reason: str = "") -> None:
        detail = f": {reason}" if reason else ""
        super().__init__(f"Invalid player name {name!r}{detail}.")
        self.name = name
        self.reason = reason


class ScoreboardCorruptedError(ProfileError):
    """Raised when the score file exists but cannot be read back."""

    def __init__(self, path: str, reason: str = "") -> None:
        detail = f": {reason}" if reason else ""
        super().__init__(f"Corrupted score board {path!r}{detail}.")
        self.path = path
        self.reason = reason
