"""Themed rendering and cached maze geometry."""
import math
import pygame  # type: ignore[import-not-found]
from .game import Game
from .sprites import SpriteManager
from .preferences import Preferences
from .themes import THEMES, Theme
from .widgets import text, bar
from .effects import ParticleSystem, scanlines


class Renderer:
    def __init__(self, screen: pygame.Surface, prefs: Preferences) -> None:
        self.screen = screen
        self.prefs = prefs
        self.font = pygame.font.Font(None, 30)
        self.big = pygame.font.Font(None, 82)
        self.small = pygame.font.Font(None, 22)
        self.sprites = SpriteManager()
        self.particles = ParticleSystem()
        self.crt = scanlines(screen)
        self.maze_key: tuple[object, ...] | None = None
        self.maze_layer = pygame.Surface(screen.get_size())
        self.previous_maze: object = None
        self.previous_gums: set[tuple[int, int]] = set()

    @property
    def theme(self) -> Theme:
        return THEMES[self.prefs.theme]

    def text(self, message: str, y: int, big: bool = False) -> None:
        text(self.screen, self.big if big else self.font, message,
             (550, y), self.theme.accent if big else self.theme.foreground)

    def background(self) -> None:
        self.screen.fill(self.theme.background)
        if self.prefs.theme == 'tron':
            for x in range(0, 1100, 40):
                pygame.draw.line(
                    self.screen, self.theme.panel, (x, 0), (x, 850)
                )
            for y in range(0, 850, 40):
                pygame.draw.line(
                    self.screen, self.theme.panel, (0, y), (1100, y)
                )

    def geometry(self, game: Game) -> tuple[float, float, float]:
        maze = game.maze
        scale = min(1020 / maze.width, 650 / maze.height)
        y = 145 + (650 - maze.height * scale) / 2
        return scale, (1100 - maze.width * scale) / 2, y

    def walls(self, game: Game, scale: float, ox: float, oy: float) -> None:
        key = (game.maze, self.prefs.theme, self.prefs.glow)
        if key != self.maze_key:
            self.maze_key = key
            layer = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            segments = set()
            for row, cells in enumerate(game.maze.grid):
                for col, bits in enumerate(cells):
                    x, y = col, row
                    for bit, a, b in ((1, (x, y), (x+1, y)),
                                      (2, (x+1, y), (x+1, y+1)),
                                      (4, (x, y+1), (x+1, y+1)),
                                      (8, (x, y), (x, y+1))):
                        if bits & bit:
                            segments.add((a, b))
            width = max(1, round(scale * .12))
            t = self.theme
            passes = []
            if t.style == 'glow' and self.prefs.glow:
                passes.extend([(max(2, width*3), tuple(c//5 for c in t.wall)),
                               (max(2, width*2), tuple(c//2 for c in t.wall))])
            passes.append((width, t.wall))
            if t.style == 'double' and width >= 5:
                passes.append((max(1, width//3), t.background))
            for thickness, color in passes:
                for a, b in segments:
                    p = (round(ox+a[0]*scale), round(oy+a[1]*scale))
                    q = (round(ox+b[0]*scale), round(oy+b[1]*scale))
                    pygame.draw.line(layer, color, p, q, thickness)
                    if thickness > 2:
                        pygame.draw.circle(layer, color, p, thickness//2)
                        pygame.draw.circle(layer, color, q, thickness//2)
            self.maze_layer = layer
        self.screen.blit(self.maze_layer, (0, 0))

    def game(self, game: Game, dt: float) -> None:
        self.background()
        t = self.theme
        scale, ox, oy = self.geometry(game)
        self.walls(game, scale, ox, oy)
        stats = [('SCORE', f'{game.score:06d}'), ('LIVES', str(game.lives)),
                 ('LEVEL', f'{game.index+1}/{len(game.settings.levels)}'),
                 ('TIME', f'{max(0, math.ceil(game.remaining))} s')]
        for i, (label, value) in enumerate(stats):
            x = 40 + i * 260
            pygame.draw.rect(
                self.screen, t.panel, (x, 20, 240, 75), border_radius=9
            )
            text(self.screen, self.small, label, (x+120, 37), t.foreground)
            text(self.screen, self.font, value, (x+120, 66), t.accent)
        bar(self.screen, pygame.Rect(40, 108, 1020, 8),
            game.remaining / game.settings.level_max_time, t)
        if game.frightened > 0:
            bar(self.screen, pygame.Rect(40, 122, 1020, 6),
                game.frightened/7, t)

        def center(x: float, y: float) -> tuple[float, float]:
            return ox+(x+.5)*scale, oy+(y+.5)*scale
        now = pygame.time.get_ticks() if self.prefs.animations else 0
        gums = game.gums | game.super_gums
        if self.previous_maze is not game.maze:
            self.particles.items.clear()
        elif self.prefs.particles and not game.paused:
            for x, y in self.previous_gums - gums:
                self.particles.burst(*center(x, y))
        self.previous_maze = game.maze
        self.previous_gums = set(gums)
        for x, y in game.gums:
            self.sprites.draw_gum(self.screen, center(x, y), scale)
        for x, y in game.super_gums:
            pulse = 1 + .12 * math.sin(now / 180)
            self.sprites.draw_gum(self.screen, center(x, y), scale*pulse, True)
        size = max(2, round(scale*.8))
        p = game.player
        self.sprites.draw_pacman(
            self.screen, center(p.x, p.y), size, p.direction, now
        )
        for ghost, name in zip(game.ghosts, self.sprites.GHOST_NAMES):
            if ghost.respawn <= 0:
                self.sprites.draw_ghost(
                    self.screen, center(ghost.x, ghost.y), size,
                    name, ghost.direction, game.frightened,
                    pygame.time.get_ticks()
                )
        if self.prefs.particles:
            if not game.paused:
                self.particles.update(dt)
            self.particles.draw(self.screen, t.accent)
        text(self.screen, self.small, 'ESC: pause   |   F1: reviewer controls',
             (550, 810), t.foreground)

    def overlay(self, title: str = 'PAUSED', subtitle: str = '') -> None:
        shade = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        shade.fill((0, 0, 0, 185))
        self.screen.blit(shade, (0, 0))
        pygame.draw.rect(
            self.screen, self.theme.panel, (310, 175, 480, 425),
            border_radius=14
        )
        self.text(title, 235, True)
        if subtitle:
            self.text(subtitle, 290)

    def finish(self, fps: float) -> None:
        if self.prefs.scanlines or self.prefs.theme == 'crt':
            self.screen.blit(self.crt, (0, 0))
        if self.prefs.show_fps:
            text(
                self.screen, self.small, f'{fps:.0f} FPS',
                (1040, 10), self.theme.accent
            )
