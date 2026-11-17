"""Adapter for the assigned external A-Maze-ing package."""
from collections import deque
from typing import Any

MOVES = {'U': (0, -1), 'R': (1, 0), 'D': (0, 1), 'L': (-1, 0)}
WALLS = {'U': 1, 'R': 2, 'D': 4, 'L': 8}
OPPOSITE = {'U': 'D', 'R': 'L', 'D': 'U', 'L': 'R'}


class Maze:
    """A maze and its safe corridor queries."""

    def __init__(self, width: int, height: int, seed: int) -> None:
        """Generate a maze using the unmodified external package."""
        from mazegenerator import MazeGenerator  # type: ignore[import-untyped]
        source: Any = MazeGenerator(size=(width, height), seed=seed,
                                    perfect=False)
        self.grid: list[list[int]] = source.maze
        if (len(self.grid) != height or
                any(len(row) != width for row in self.grid)):
            raise ValueError('maze generator returned unexpected dimensions')
        self.width, self.height = width, height

    def open(self, cell: tuple[int, int], direction: str) -> bool:
        """Check both sides of a passage and the maze bounds."""
        x, y = cell
        dx, dy = MOVES[direction]
        nx, ny = x + dx, y + dy
        return (0 <= x < self.width and 0 <= y < self.height and
                0 <= nx < self.width and 0 <= ny < self.height and
                not self.grid[y][x] & WALLS[direction] and
                not self.grid[ny][nx] & WALLS[OPPOSITE[direction]])

    def directions(self, cell: tuple[int, int]) -> list[str]:
        """Return the directions available from a cell."""
        return [d for d in MOVES if self.open(cell, d)]

    def cells(self) -> list[tuple[int, int]]:
        """Return cells that are not completely enclosed."""
        return [(x, y) for y in range(self.height)
                for x in range(self.width) if self.directions((x, y))]

    def nearest(self, target: tuple[int, int]) -> tuple[int, int]:
        """Choose the nearest traversable cell to a desired position."""
        return min(self.cells(), key=lambda p:
                   abs(p[0] - target[0]) + abs(p[1] - target[1]))

    def reachable(self, start: tuple[int, int]) -> set[tuple[int, int]]:
        """Find the connected component containing start."""
        seen = {start}
        queue = deque([start])
        while queue:
            cell = queue.popleft()
            for direction in self.directions(cell):
                dx, dy = MOVES[direction]
                nxt = (cell[0] + dx, cell[1] + dy)
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
        return seen
