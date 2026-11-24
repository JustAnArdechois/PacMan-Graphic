"""Cosmetic effects; never change gameplay state."""
from dataclasses import dataclass
import math
import random
import pygame
from .themes import Color


@dataclass
class Particle:
    x: float
    y: float
    vx: float
    vy: float
    life: float = .45


class ParticleSystem:
    def __init__(self) -> None:
        self.items: list[Particle] = []
        self.rng = random.Random()

    def burst(self, x: float, y: float) -> None:
        for _ in range(12):
            angle = self.rng.uniform(0, math.tau)
            self.items.append(Particle(x, y, math.cos(angle) * 85,
                                       math.sin(angle) * 85))
        self.items = self.items[-240:]

    def update(self, dt: float) -> None:
        for p in self.items:
            p.x += p.vx * dt
            p.y += p.vy * dt
            p.life -= dt
        self.items = [p for p in self.items if p.life > 0]

    def draw(self, screen: pygame.Surface, color: Color) -> None:
        for p in self.items:
            pygame.draw.circle(screen, color, (round(p.x), round(p.y)),
                               max(1, round(p.life * 7)))


def scanlines(screen: pygame.Surface) -> pygame.Surface:
    layer = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    for y in range(0, screen.get_height(), 4):
        pygame.draw.line(layer, (0, 0, 0, 45), (0, y),
                         (screen.get_width(), y))
    return layer
