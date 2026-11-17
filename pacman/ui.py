"""Pygame rendering using basic MLX-equivalent primitives."""
import math
from typing import Any
import pygame
from .game import Game
from .sprites import SpriteManager

BLACK = (8, 9, 24)
WHITE = (240, 240, 240)
YELLOW = (255, 220, 0)
BLUE = (50, 95, 245)


class Renderer:
    """Draw the game and simple text-based screens."""

    def __init__(self, screen: pygame.Surface) -> None:
        """Prepare screen and fonts."""
        self.screen = screen
        self.font = pygame.font.Font(None, 32)
        self.big = pygame.font.Font(None, 75)
        self.sprites = SpriteManager()

    def text(self, message: str, y: int, big: bool = False,
             color: tuple[int, int, int] = WHITE) -> None:
        """Draw a horizontally centered text line."""
        font = self.big if big else self.font
        surface = font.render(message, True, color)
        self.screen.blit(surface, surface.get_rect(
            center=(self.screen.get_width() // 2, y)))

    def menu(self, entries: list[dict[str, Any]]) -> None:
        """Draw the main menu with high scores."""
        self.screen.fill(BLACK)
        self.text('PAC-MAN', 105, True, YELLOW)
        self.text('ENTER: PLAY   H: HIGHSCORES', 220)
        self.text('I: INSTRUCTIONS   ESC: EXIT', 260)
        self.text('TOP 10', 350, color=YELLOW)
        for i, entry in enumerate(entries[:10]):
            self.text(f"{i + 1}. {entry['name']} - {entry['score']}",
                      390 + i * 32)

    def game(self, game: Game) -> None:
        """Draw maze, pellets, ghosts, player and always-visible HUD."""
        self.screen.fill(BLACK)
        maze = game.maze
        w, h = self.screen.get_size()
        scale = min((w - 60) / maze.width, (h - 160) / maze.height)
        ox = (w - maze.width * scale) / 2
        oy = 110 + (h - 160 - maze.height * scale) / 2
        self.text(f'SCORE {game.score}    LIVES {game.lives}    '
                  f'LEVEL {game.index + 1}/{len(game.settings.levels)}'
                  f'    TIME {max(0, math.ceil(game.remaining))}', 35)
        self.text('ESC: pause  |  F1: cheats  |  arrows/WASD: move', 72)
        for row, cells in enumerate(maze.grid):
            for col, bits in enumerate(cells):
                x, y = ox + col * scale, oy + row * scale
                if bits & 1:
                    pygame.draw.line(self.screen, BLUE, (x, y),
                                     (x + scale, y), 2)
                if bits & 2:
                    pygame.draw.line(self.screen, BLUE, (x + scale, y),
                                     (x + scale, y + scale), 2)
                if bits & 4:
                    pygame.draw.line(self.screen, BLUE, (x, y + scale),
                                     (x + scale, y + scale), 2)
                if bits & 8:
                    pygame.draw.line(self.screen, BLUE, (x, y),
                                     (x, y + scale), 2)
        elapsed_ms = pygame.time.get_ticks()
        for x, y in game.gums:
            center = (ox + (x + .5) * scale,
                      oy + (y + .5) * scale)
            self.sprites.draw_gum(self.screen, center, scale)
        for x, y in game.super_gums:
            center = (ox + (x + .5) * scale,
                      oy + (y + .5) * scale)
            self.sprites.draw_gum(self.screen, center, scale,
                                  super_gum=True)
        player = game.player
        center = (ox + (player.x + .5) * scale,
                  oy + (player.y + .5) * scale)
        sprite_size = max(2, round(scale * .8))
        self.sprites.draw_pacman(self.screen, center, sprite_size,
                                 player.direction, elapsed_ms)
        for ghost, name in zip(game.ghosts, self.sprites.GHOST_NAMES):
            if ghost.respawn > 0:
                continue
            center = (ox + (ghost.x + .5) * scale,
                      oy + (ghost.y + .5) * scale)
            self.sprites.draw_ghost(self.screen, center, sprite_size,
                                    name, ghost.direction,
                                    game.frightened, elapsed_ms)
        if game.paused:
            self.text('PAUSED - ENTER: resume / M: menu', h // 2,
                      True, YELLOW)
