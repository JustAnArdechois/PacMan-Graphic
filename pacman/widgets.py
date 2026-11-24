"""Reusable Pygame interface primitives."""
from dataclasses import dataclass
import pygame
from .themes import Theme


def text(screen: pygame.Surface, font: pygame.font.Font, message: str,
         center: tuple[int, int], color: tuple[int, int, int]) -> None:
    image = font.render(message, True, color)
    screen.blit(image, image.get_rect(center=center))


@dataclass
class Button:
    action: str
    label: str
    rect: pygame.Rect

    def draw(self, screen: pygame.Surface, font: pygame.font.Font,
             theme: Theme, selected: bool) -> None:
        active = selected or self.rect.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(screen, theme.accent if active else theme.panel,
                         self.rect, border_radius=8)
        pygame.draw.rect(screen, theme.wall, self.rect, 2, border_radius=8)
        text(screen, font, self.label, self.rect.center,
             theme.background if active else theme.foreground)


def bar(screen: pygame.Surface, rect: pygame.Rect, fraction: float,
        theme: Theme) -> None:
    pygame.draw.rect(screen, theme.panel, rect, border_radius=4)
    width = round(rect.width * max(0., min(1., fraction)))
    if width:
        pygame.draw.rect(screen, theme.accent,
                         (rect.x, rect.y, width, rect.height), border_radius=4)
