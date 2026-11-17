"""Application state machine and graphical user interface."""
import pygame
from .configuration import Settings
from .game import Game
from .highscores import Highscores
from .ui import Renderer, BLACK, WHITE, YELLOW

KEYS = {pygame.K_UP: 'U', pygame.K_w: 'U', pygame.K_z: 'U',
        pygame.K_DOWN: 'D', pygame.K_s: 'D',
        pygame.K_LEFT: 'L', pygame.K_a: 'L', pygame.K_q: 'L',
        pygame.K_RIGHT: 'R', pygame.K_d: 'R'}


class App:
    """Run the menu, game, pause, instructions and score entry."""

    def __init__(self, settings: Settings) -> None:
        """Initialize graphics and persistent scores."""
        pygame.init()
        self.screen = pygame.display.set_mode((1100, 850))
        pygame.display.set_caption('Pac-Man 42')
        self.renderer = Renderer(self.screen)
        self.clock = pygame.time.Clock()
        self.settings = settings
        self.scores = Highscores(settings.highscore_filename)
        self.state = 'menu'
        self.game: Game | None = None
        self.name = ''
        self.cheat_panel = False

    def start(self) -> None:
        """Create a new game, reporting generation errors cleanly."""
        try:
            self.game = Game(self.settings)
            self.state = 'game'
        except Exception as exc:
            print(f'[maze] unable to generate level: {exc}')
            self.state = 'error'

    def handle(self, event: pygame.event.Event) -> bool:
        """Process one input event; return False to exit."""
        if event.type == pygame.QUIT:
            return False
        if event.type != pygame.KEYDOWN:
            return True
        key = event.key
        if self.state == 'menu':
            if key == pygame.K_RETURN:
                self.start()
            elif key == pygame.K_h:
                self.state = 'scores'
            elif key == pygame.K_i:
                self.state = 'instructions'
            elif key == pygame.K_ESCAPE:
                return False
        elif self.state in ('scores', 'instructions', 'error'):
            if key in (pygame.K_ESCAPE, pygame.K_RETURN):
                self.state = 'menu'
        elif self.state == 'game' and self.game is not None:
            if key == pygame.K_ESCAPE:
                self.game.paused = not self.game.paused
            elif self.game.paused:
                if key == pygame.K_RETURN:
                    self.game.paused = False
                elif key == pygame.K_m:
                    self.state = 'menu'
            elif key == pygame.K_F1:
                self.cheat_panel = not self.cheat_panel
            elif self.cheat_panel and key in (
                    pygame.K_1, pygame.K_2, pygame.K_3,
                    pygame.K_4, pygame.K_5, pygame.K_6):
                self.game.cheat(pygame.key.name(key))
            elif key in KEYS:
                self.game.player.wanted = KEYS[key]
        elif self.state == 'name':
            if key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]
            elif key == pygame.K_RETURN:
                if self.game is not None and self.scores.valid_name(self.name):
                    self.scores.add(self.name, self.game.score)
                    self.state = 'menu'
            elif len(self.name) < 10:
                char = event.unicode
                if (len(char) == 1 and
                        (char == ' ' or (char.isascii() and char.isalnum()))):
                    self.name += char
        return True

    def draw(self) -> None:
        """Render the currently selected screen."""
        r = self.renderer
        if self.state == 'menu':
            r.menu(self.scores.entries)
        elif self.state == 'game' and self.game is not None:
            r.game(self.game)
            if self.cheat_panel:
                r.text('CHEATS: 1 invincible  2 skip  3 freeze  '
                       '4 life  5 speed  6 time',
                       self.screen.get_height() - 18,
                       color=YELLOW)
        else:
            self.screen.fill(BLACK)
            if self.state == 'instructions':
                r.text('INSTRUCTIONS', 140, True, YELLOW)
                for i, line in enumerate((
                        'Move: arrows, WASD or ZQSD',
                        'Eat every dot to finish a level.',
                        'Large dots let you eat ghosts temporarily.',
                        'Avoid ghosts otherwise. ESC pauses.',
                        'F1 shows reviewer cheat controls.',
                        'ENTER / ESC: return to menu')):
                    r.text(line, 250 + 55 * i)
            elif self.state == 'scores':
                r.text('TOP 10', 120, True, YELLOW)
                for i, entry in enumerate(self.scores.entries):
                    r.text(f"{i + 1}. {entry['name']}  {entry['score']}",
                           200 + 45 * i)
                r.text('ESC: menu', 750)
            elif self.state == 'name' and self.game is not None:
                r.text('VICTORY!' if self.game.won else 'GAME OVER',
                       180, True, YELLOW)
                r.text(f'Final score: {self.game.score}', 290)
                r.text('Enter your name (max 10 letters/digits/spaces):', 390)
                r.text(self.name + '_', 455, True)
                r.text('ENTER: save score and return to menu', 550)
            elif self.state == 'error':
                r.text('Maze generation failed.', 300, True, YELLOW)
                r.text('Check terminal output. ENTER: menu', 400, color=WHITE)
        pygame.display.flip()

    def run(self) -> None:
        """Execute the event/update/render loop at 60 FPS."""
        running = True
        try:
            while running:
                dt = self.clock.tick(60) / 1000.0
                for event in pygame.event.get():
                    if not self.handle(event):
                        running = False
                if self.state == 'game' and self.game is not None:
                    try:
                        self.game.update(dt)
                    except Exception as exc:
                        print(f'[game] error: {exc}')
                        self.state = 'error'
                    if self.game.finished:
                        self.name = ''
                        self.state = 'name'
                self.draw()
        finally:
            pygame.quit()
