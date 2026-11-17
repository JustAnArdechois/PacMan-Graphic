"""Object-oriented player and ghost movement and AI."""
import random
from collections import deque
from .maze import Maze, MOVES, OPPOSITE


class Character:
    """A character interpolating between adjacent maze cells."""

    def __init__(self, cell: tuple[int, int], speed: float,
                 direction: str = 'L') -> None:
        """Create a character at the centre of a cell."""
        self.cell = cell
        self.x, self.y = float(cell[0]), float(cell[1])
        self.speed = speed
        self.direction = direction
        self.wanted = direction
        self.target: tuple[int, int] | None = None

    def reset(self, cell: tuple[int, int]) -> None:
        """Return the character to its starting position."""
        self.cell = cell
        self.x, self.y = float(cell[0]), float(cell[1])
        self.target = None

    def update(self, maze: Maze, dt: float) -> None:
        """Move by a frame-rate-independent distance along corridors."""
        distance = self.speed * min(dt, 0.1)
        while distance > 0:
            if self.target is None:
                if maze.open(self.cell, self.wanted):
                    self.direction = self.wanted
                if not maze.open(self.cell, self.direction):
                    break
                dx, dy = MOVES[self.direction]
                self.target = (self.cell[0] + dx, self.cell[1] + dy)
            tx, ty = self.target
            remaining = abs(tx - self.x) + abs(ty - self.y)
            step = min(distance, remaining)
            self.x += (1 if tx > self.x else -1 if tx < self.x else 0) * step
            self.y += (1 if ty > self.y else -1 if ty < self.y else 0) * step
            distance -= step
            if step + 1e-7 >= remaining:
                self.x, self.y = float(tx), float(ty)
                self.cell = self.target
                self.target = None
            else:
                break


class Player(Character):
    """The keyboard-controlled Pac-Man."""


class Ghost(Character):
    """A ghost that chases or flees and can be temporarily eaten."""

    def __init__(self, cell: tuple[int, int], speed: float,
                 color: tuple[int, int, int]) -> None:
        """Create a ghost with its own home and color."""
        super().__init__(cell, speed)
        self.home = cell
        self.color = color
        self.respawn = 0.0

    def decide(self, maze: Maze, player: tuple[int, int],
               frightened: bool) -> None:
        """Use BFS distances to chase or flee at each junction."""
        if self.target is not None or self.respawn > 0:
            return
        options = maze.directions(self.cell)
        if not options:
            return
        distances = {player: 0}
        queue = deque([player])
        while queue:
            current = queue.popleft()
            for direction in maze.directions(current):
                dx, dy = MOVES[direction]
                nxt = (current[0] + dx, current[1] + dy)
                if nxt not in distances:
                    distances[nxt] = distances[current] + 1
                    queue.append(nxt)
        scores = {}
        for direction in options:
            dx, dy = MOVES[direction]
            nxt = (self.cell[0] + dx, self.cell[1] + dy)
            scores[direction] = distances.get(nxt, 10 ** 9)
        best = (max(scores.values()) if frightened else
                min(scores.values()))
        choices = [d for d in options if scores[d] == best]
        no_reverse = [d for d in choices if d != OPPOSITE[self.direction]]
        self.wanted = random.choice(no_reverse or choices)
