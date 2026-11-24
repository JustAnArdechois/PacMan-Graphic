"""Menu layouts and shared keyboard/mouse navigation."""
import pygame
from .widgets import Button
from .themes import Theme, THEMES
from .preferences import Preferences


class Menus:
    def __init__(self) -> None:
        self.selected = 0
        self.buttons: list[Button] = []

    def layout(self, state: str, prefs: Preferences) -> None:
        options: list[tuple[str, str]] = []
        if state == 'menu':
            options = [('play', 'PLAY GAME'), ('scores', 'HIGH SCORES'),
                       ('settings', 'GRAPHIC SETTINGS'),
                       ('instructions', 'HOW TO PLAY'), ('quit', 'QUIT')]
        elif state == 'pause':
            options = [('resume', 'RESUME'), ('restart', 'RESTART'),
                       ('settings', 'GRAPHIC SETTINGS'), ('menu', 'MAIN MENU')]
        elif state == 'level_complete':
            options = [('next_level', 'NEXT LEVEL'),
                       ('settings', 'GRAPHIC SETTINGS'),
                       ('menu', 'MAIN MENU')]
        elif state == 'settings':
            options = [(f'theme:{k}', t.name +
                        ('  [ACTIVE]' if k == prefs.theme else ''))
                       for k, t in THEMES.items()]
            options += [(k, f'{label}: {"ON" if getattr(prefs, k) else "OFF"}')
                        for k, label in [('glow', 'Glow'),
                                         ('particles', 'Particles'),
                                         ('animations', 'Animations'),
                                         ('scanlines', 'Scanlines'),
                                         ('show_fps', 'FPS counter'),
                                         ('fullscreen', 'Fullscreen')]]
            options += [('fps_limit', f'FPS limit: {prefs.fps_limit}'),
                        ('back', 'BACK')]
        else:
            options = [('back', 'BACK TO MENU')]
        start = 190 if state == 'settings' else 300
        if state in ('scores', 'instructions', 'error'):
            start = 740
        if state == 'level_complete':
            start = 340
        step = 43 if state == 'settings' else 65
        self.buttons = [
            Button(action, label,
                   pygame.Rect(350, start + i * step, 400, step - 7))
            for i, (action, label) in enumerate(options)
        ]
        self.selected %= len(self.buttons)

    def handle(self, event: pygame.event.Event) -> str | None:
        if not self.buttons:
            return None
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                self.selected = (
                    self.selected +
                    (1 if event.key == pygame.K_DOWN else -1)
                ) % len(self.buttons)
            elif event.key == pygame.K_RETURN:
                return self.buttons[self.selected].action
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button.rect.collidepoint(event.pos):
                    return button.action
        return None

    def draw(self, screen: pygame.Surface, font: pygame.font.Font,
             theme: Theme) -> None:
        for i, button in enumerate(self.buttons):
            button.draw(screen, font, theme, i == self.selected)
