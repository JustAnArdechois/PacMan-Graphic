"""Application state machine with themed menus."""
import pygame
from .configuration import Settings
from .game import Game
from .highscores import Highscores
from .ui import Renderer
from .menus import Menus
from .preferences import Preferences

KEYS = {pygame.K_UP: 'U', pygame.K_w: 'U', pygame.K_z: 'U',
        pygame.K_DOWN: 'D', pygame.K_s: 'D', pygame.K_LEFT: 'L',
        pygame.K_a: 'L', pygame.K_q: 'L', pygame.K_RIGHT: 'R',
        pygame.K_d: 'R'}


class App:
    def __init__(self, settings: Settings) -> None:
        pygame.init()
        self.prefs = Preferences.load()
        self.screen = self.display()
        pygame.display.set_caption('Pac-Man 42')
        self.renderer = Renderer(self.screen, self.prefs)
        self.clock = pygame.time.Clock()
        self.settings = settings
        self.scores = Highscores(settings.highscore_filename)
        self.menus = Menus()
        self.state = 'menu'
        self.settings_return = 'menu'
        self.game: Game | None = None
        self.name = ''
        self.cheat_panel = False
        self.change('menu')

    def display(self) -> pygame.Surface:
        flags = pygame.SCALED
        if self.prefs.fullscreen:
            flags |= pygame.FULLSCREEN
        return pygame.display.set_mode((1100, 850), flags)

    def change(self, state: str) -> None:
        self.state = state
        self.menus.selected = 0
        self.menus.layout(state, self.prefs)

    def start(self) -> None:
        try:
            self.game = Game(self.settings)
            self.cheat_panel = False
            self.change('game')
        except Exception as exc:
            print(f'[maze] {exc}')
            self.change('error')

    def action(self, action: str) -> bool:
        if action == 'quit':
            return False
        if action in ('play', 'restart'):
            self.start()
        elif action == 'next_level' and self.game is not None:
            try:
                self.game.advance_level()
                self.change('game')
            except Exception as exc:
                print(f'[maze] {exc}')
                self.change('error')
        elif action == 'resume' and self.game is not None:
            self.game.paused = False
            self.change('game')
        elif action == 'settings':
            self.settings_return = self.state
            self.change('settings')
        elif action == 'back':
            destination = (self.settings_return
                           if self.state == 'settings' else 'menu')
            self.change(destination)
        elif action in ('menu', 'scores', 'instructions'):
            self.change(action)
        elif self.state == 'settings':
            if action.startswith('theme:'):
                self.prefs.theme = action.split(':', 1)[1]
            elif action == 'fps_limit':
                limits = (30, 60, 120, 144)
                current = limits.index(self.prefs.fps_limit)
                self.prefs.fps_limit = limits[(current+1) % 4]
            elif action in ('glow', 'particles', 'animations', 'scanlines',
                            'show_fps', 'fullscreen'):
                setattr(self.prefs, action, not getattr(self.prefs, action))
                if action == 'fullscreen':
                    try:
                        self.screen = self.display()
                    except pygame.error:
                        self.prefs.fullscreen = not self.prefs.fullscreen
                        self.screen = self.display()
                    self.renderer.screen = self.screen
            self.prefs.save()
            self.menus.layout('settings', self.prefs)
        return True

    def handle(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.QUIT:
            return False
        if self.state == 'game' and self.game is not None:
            if event.type != pygame.KEYDOWN:
                return True
            key = event.key
            if key == pygame.K_ESCAPE:
                self.game.paused = True
                self.change('pause')
            elif key == pygame.K_F1:
                self.cheat_panel = not self.cheat_panel
            elif self.cheat_panel and key in (pygame.K_1, pygame.K_2,
                                              pygame.K_3, pygame.K_4,
                                              pygame.K_5, pygame.K_6):
                self.game.cheat(pygame.key.name(key))
                if self.game.level_complete:
                    self.change('level_complete')
                elif self.game.finished:
                    self.name = ''
                    self.change('name')
            elif key in KEYS:
                self.game.player.wanted = KEYS[key]
        elif self.state == 'name':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.name = self.name[:-1]
                elif event.key == pygame.K_RETURN:
                    if (self.game is not None and
                            self.scores.valid_name(self.name)):
                        if self.scores.add(self.name, self.game.score):
                            self.change('menu')
                elif len(self.name) < 10:
                    char = event.unicode
                    if (len(char) == 1 and
                            (char == ' ' or
                             (char.isascii() and char.isalnum()))):
                        self.name += char
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == 'menu':
                        return False
                    return self.action(
                        'resume' if self.state == 'pause' else 'back')
                if (self.state == 'menu' and
                        event.key in (pygame.K_h, pygame.K_i)):
                    destination = ('scores' if event.key == pygame.K_h
                                   else 'instructions')
                    return self.action(destination)
                if self.state == 'pause' and event.key == pygame.K_m:
                    return self.action('menu')
            action = self.menus.handle(event)
            if action is not None:
                return self.action(action)
        return True

    def draw(self, dt: float) -> None:
        r = self.renderer
        r.background()
        if (self.state in ('game', 'pause', 'level_complete')
                and self.game is not None):
            r.game(self.game, dt)
            if self.cheat_panel:
                r.text(
                    'CHEATS: 1 invincible | 2 skip | 3 freeze | 4 life | '
                    '5 speed | 6 time',
                    836)
            if self.state == 'pause':
                r.overlay()
            elif self.state == 'level_complete':
                r.overlay(
                    'LEVEL COMPLETE!',
                    f'Level {self.game.index + 1} / '
                    f'{len(self.game.settings.levels)}  |  Score: '
                    f'{self.game.score}')
        elif self.state == 'menu':
            r.text('PAC-MAN', 105, True)
            r.text('42 MARSEILLE  /  ARCADE EDITION', 165)
            now = pygame.time.get_ticks() if self.prefs.animations else 0
            for i, name in enumerate(r.sprites.GHOST_NAMES):
                r.sprites.draw_ghost(self.screen, (460+i*60, 230), 45,
                                     name, 'R', 0, now)
            best = (self.scores.entries[0]['score']
                    if self.scores.entries else 0)
            r.text(f'BEST SCORE  {best:06d}', 680)
        elif self.state == 'settings':
            r.text('GRAPHIC SETTINGS', 80, True)
            r.text('Choose a theme and customize the effects', 145)
        elif self.state == 'scores':
            r.text('HALL OF FAME', 95, True)
            for i, entry in enumerate(self.scores.entries):
                r.text(
                    f"{i+1:02d}     {entry['name']}     "
                    f"{entry['score']:06d}",
                    190+i*49)
        elif self.state == 'instructions':
            r.text('HOW TO PLAY', 100, True)
            for i, line in enumerate(('ARROWS / WASD / ZQSD: move',
                                      'Eat every pellet to clear the level.',
                                      'Power pellets make ghosts edible.',
                                      ('ESC: pause   |   '
                                       'F1: reviewer controls'))):
                r.text(line, 245+i*75)
        elif self.state == 'name' and self.game is not None:
            r.text('VICTORY!' if self.game.won else 'GAME OVER', 180, True)
            r.text(f'Final score: {self.game.score}', 290)
            r.text('Enter your name (max 10 letters/digits/spaces)', 390)
            r.text(self.name+'_', 455, True)
            r.text('ENTER: save score', 550)
        elif self.state == 'error':
            r.text('GAME ERROR', 300, True)
            r.text('Check terminal output.', 400)
        if self.state not in ('game', 'name'):
            self.menus.draw(self.screen, r.font, r.theme)
        r.finish(self.clock.get_fps())
        pygame.display.flip()

    def run(self) -> None:
        running = True
        try:
            while running:
                dt = self.clock.tick(self.prefs.fps_limit)/1000.0
                for event in pygame.event.get():
                    if not self.handle(event):
                        running = False
                        break
                if not running:
                    break
                if self.state == 'game' and self.game is not None:
                    try:
                        self.game.update(dt)
                        if self.game.finished:
                            self.name = ''
                            self.change('name')
                        elif self.game.level_complete:
                            self.change('level_complete')
                    except Exception as exc:
                        print(f'[game] {exc}')
                        self.change('error')
                self.draw(dt)
        finally:
            pygame.quit()
