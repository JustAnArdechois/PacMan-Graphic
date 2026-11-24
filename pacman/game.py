"""Gameplay state, levels, collisions and progression."""
import random
from .configuration import Settings
from .entities import Player, Ghost
from .maze import Maze

COLORS = [(240, 65, 65), (255, 145, 205),
          (70, 200, 245), (255, 175, 70)]


class Game:
    """A complete game across multiple levels."""

    def __init__(self, settings: Settings) -> None:
        """Create game state and start the first level."""
        self.settings = settings
        self.score = 0
        self.lives = settings.lives
        self.index = 0
        self.finished = False
        self.won = False
        self.paused = False
        self.level_complete = False
        self.invincible = False
        self.freeze = False
        self.speed_boost = False
        self.load_level()

    def load_level(self) -> None:
        """Build a maze and distribute collectible items and ghosts."""
        width, height = self.settings.levels[self.index]
        seed = self.settings.seed if self.index == 0 else random.randint(1,
                                                                         2**31)
        self.maze = Maze(width, height, seed)
        center = self.maze.nearest((width // 2, height // 2))
        connected = self.maze.reachable(center)
        self.player = Player(center, 5.0)
        corners = [(0, 0), (width - 1, 0), (0, height - 1),
                   (width - 1, height - 1)]
        available = list(connected)
        homes = [min(available, key=lambda p: abs(p[0] - x) + abs(p[1] - y))
                 for x, y in corners]
        self.ghosts = [Ghost(pos, 3.0, color)
                       for pos, color in zip(homes, COLORS)]
        self.super_gums = set(homes)
        self.super_gums.discard(center)
        self.gums = connected - self.super_gums - {center}
        # 'pacgum' is the requested maximum count of ordinary pellets.
        if len(self.gums) > self.settings.pacgum:
            self.gums = set(random.sample(sorted(self.gums),
                                          self.settings.pacgum))
        self.remaining = float(self.settings.level_max_time)
        self.frightened = 0.0
        self.hit_cooldown = 1.5
        self.paused = False
        self.level_complete = False

    def next_level(self) -> None:
        """Advance or end the game after all pellets are eaten."""
        if self.finished or self.level_complete:
            return
        if self.index + 1 >= len(self.settings.levels):
            self.finished, self.won = True, True
        else:
            self.level_complete = True
            self.paused = True

    def advance_level(self) -> None:
        """Start the next level only after confirmation."""
        if self.level_complete and not self.finished:
            self.index += 1
            self.load_level()

    def update(self, dt: float) -> None:
        """Advance movement, timers, pickups and collisions."""
        if self.finished or self.paused:
            return
        dt = min(dt, 0.1)
        self.remaining -= dt
        self.frightened = max(0.0, self.frightened - dt)
        self.hit_cooldown = max(0.0, self.hit_cooldown - dt)
        if self.remaining <= 0:
            self.finished = True
            return
        self.player.speed = 8.0 if self.speed_boost else 5.0
        self.player.update(self.maze, dt)
        for ghost in self.ghosts:
            if ghost.respawn > 0:
                ghost.respawn = max(0.0, ghost.respawn - dt)
                continue
            if not self.freeze:
                ghost.decide(self.maze, self.player.cell,
                             self.frightened > 0)
                ghost.update(self.maze, dt)
        cell = self.player.cell
        if cell in self.gums:
            self.gums.remove(cell)
            self.score += self.settings.points_per_pacgum
        if cell in self.super_gums:
            self.super_gums.remove(cell)
            self.score += self.settings.points_per_super_pacgum
            self.frightened = 7.0
        for ghost in self.ghosts:
            if ghost.respawn > 0:
                continue
            if ((ghost.x - self.player.x) ** 2 +
                    (ghost.y - self.player.y) ** 2) >= 0.4:
                continue
            if self.frightened > 0:
                self.score += self.settings.points_per_ghost
                ghost.reset(ghost.home)
                ghost.respawn = 6.0
            elif not self.invincible and self.hit_cooldown == 0:
                self.lives -= 1
                self.hit_cooldown = 2.0
                if self.lives == 0:
                    self.finished = True
                    return
                self.player.reset(self.maze.nearest(
                    (self.maze.width // 2, self.maze.height // 2)))
                for other in self.ghosts:
                    other.reset(other.home)
                break
        if not self.gums and not self.super_gums:
            self.next_level()

    def cheat(self, key: str) -> None:
        """Apply reviewer cheats: invulnerability,
        skip, freeze, life, speed."""
        if key == '1':
            self.invincible = not self.invincible
        elif key == '2':
            self.next_level()
        elif key == '3':
            self.freeze = not self.freeze
        elif key == '4':
            self.lives += 1
        elif key == '5':
            self.speed_boost = not self.speed_boost
        elif key == '6':
            self.remaining += 30.0
