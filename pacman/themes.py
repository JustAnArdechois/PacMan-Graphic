"""Immutable visual themes, independent of gameplay."""
from dataclasses import dataclass

Color = tuple[int, int, int]


@dataclass(frozen=True)
class Theme:
    name: str
    background: Color
    panel: Color
    foreground: Color
    accent: Color
    wall: Color
    style: str


THEMES = {
    'classic': Theme('Classic Arcade', (5, 6, 16), (18, 24, 48),
                     (240, 240, 255), (255, 220, 0), (65, 100, 255),
                     'double'),
    'neon': Theme('Neon Cyberpunk', (16, 7, 30), (36, 18, 55),
                  (247, 221, 255), (255, 235, 72), (223, 57, 255),
                  'glow'),
    'crt': Theme('Retro CRT', (12, 19, 14), (24, 38, 27),
                 (213, 230, 199), (200, 238, 128), (81, 158, 105),
                 'double'),
    'modern': Theme('Modern Minimalist', (32, 37, 46), (48, 55, 67),
                    (245, 244, 240), (255, 209, 125), (135, 155, 195),
                    'solid'),
    'tron': Theme('Tron Futuristic', (3, 20, 29), (9, 43, 59),
                  (213, 250, 255), (103, 246, 255), (0, 199, 239),
                  'glow'),
}
