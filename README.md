*This activity has been created as part of the 42 curriculum by nturcot, yaichi.*

# Pac-Man — Arcade Edition

## Description

Pac-Man is a single-player arcade game written in Python using Pygame and an object-oriented architecture. The goal is to collect all pellets in each generated maze, avoid four autonomous ghosts and complete at least ten levels while achieving the highest possible score. Power pellets temporarily allow the player to eat ghosts.

The game includes animated sprites, a persistent top-ten leaderboard, reviewer controls, a pause menu, a level-completion menu and five selectable graphical themes. Gameplay and rendering are separated so that visual preferences do not change the game rules.

## Instructions

### Installation

Requirements: Linux (target environment), Python 3.10+ with a compatible Pygame release, pip, GNU Make and the supplied A-Maze-ing wheel. Python 3.13 is recommended for Pygame 2.6.1. Python 3.15 failed to compile that release on a 42 workstation; do not assume every newer Python version is compatible.

From the repository root, using an available compatible interpreter:

```sh
python3.13 -m venv .venv
source .venv/bin/activate
make install
make run
```

`make install` installs the Python requirements and the assigned maze-generator wheel. No separate compilation of the game is required. Alternatively, after installation:

```sh
python3 pac-man.py config.json
```

| Command | Purpose |
|---|---|
| `make install` | Install dependencies and the supplied wheel |
| `make run` | Launch the game with `config.json` |
| `make debug` | Launch under Python's `pdb` debugger; use `c` to continue, `n` to step over, `s` to step into and `p expression` to inspect values |
| `make clean` | Remove Python and analysis caches |
| `make lint` | Run flake8 and mypy |
| `make lint-strict` | Run flake8 and strict mypy checks |
| `python3 -m pytest` | Run the available automated tests |

### Controls

| Context | Controls |
|---|---|
| Gameplay | Arrow keys, WASD or ZQSD |
| Menus | Up/down arrows and Enter, or left mouse click |
| Main menu | H: highscores; I: instructions; Esc: quit |
| Pause | Esc: pause/resume; M: return to main menu; buttons: resume, restart, settings, main menu |
| Level complete | Next Level, Graphic Settings or Main Menu |
| Final victory/defeat | Enter a valid name and press Enter to save the score |

After a non-final level, the game waits for confirmation before generating the next maze. Returning from graphical settings restores the previous menu. Returning to the main menu abandons the current run; a new game starts from level one. Completing the last configured level opens the final victory screen.

### Reviewer controls

Press F1 during gameplay to toggle the cheat panel. With the panel enabled: `1` toggles invulnerability, `2` completes/skips the current level, `3` freezes ghosts, `4` adds a life, `5` toggles speed boost and `6` adds 30 seconds. Skipping a non-final level opens the same level-completion menu.

## Configuration

The program expects exactly one configuration path. The file is a JSON object with support for full-line `#` comments. Invalid values fall back to defaults with warnings; unknown keys are ignored. Unreadable or malformed configuration files use defaults.

| Key | Default | Meaning |
|---|---|---|
| `levels` | 14×10, 20×20, …, 100×100 | Array of objects containing integer `width` and `height`; at least ten levels are supplied by filling missing entries. Minimum dimensions: 14×10. |
| `lives` | 3 | Initial lives |
| `pacgum` | 42 | Maximum ordinary pellets per level |
| `points_per_pacgum` | 10 | Points per ordinary pellet |
| `points_per_super_pacgum` | 50 | Points per power pellet |
| `points_per_ghost` | 200 | Points per eaten ghost |
| `seed` | 42 | First maze seed |
| `level_max_time` | 90 | Time per level, in seconds |
| `highscore_filename` | `highscores.json` | Leaderboard file path |

For example, a minimal configuration can override the first level and leave remaining values at their defaults:

```json
{
  "levels": [{"width": 14, "height": 10}],
  "lives": 3,
  "seed": 42,
  "level_max_time": 90
}
```

### Graphical preferences

`preferences.json` is created when settings are changed. It is independent of the gameplay configuration.

| Option | Default |
|---|---|
| `theme` | `classic` |
| `glow`, `particles`, `animations` | `true` |
| `scanlines`, `show_fps`, `fullscreen` | `false` |
| `fps_limit` | 60 (choices: 30, 60, 120, 144) |

Themes: Classic Arcade (`classic`), Neon Cyberpunk (`neon`), Retro CRT (`crt`), Modern Minimalist (`modern`) and Tron Futuristic (`tron`). Retro CRT applies scanlines automatically. Preferences are loaded on startup and saved when changed. Missing or invalid preferences use defaults.

## Highscore

`Highscores` stores a local JSON array of name/score pairs in the configured file. Names must contain 1–10 ASCII letters, digits or spaces and cannot be whitespace-only. Scores must be non-negative integers. Entries are sorted in descending order and truncated to ten; malformed entries are ignored. Read errors are nonfatal, and write errors are reported in the terminal.

```json
[
  {"name": "Player42", "score": 2830},
  {"name": "Pacman", "score": 1140}
]
```

The player enters a name after final victory or defeat. The leaderboard is available from the main menu. JSON was chosen because it is human-readable, supported by Python's standard library and sufficient for a small local ranking without a database or network service. It is not a tamper-resistant competitive leaderboard.

## Maze Generation

The assigned `mazegenerator-2.1.0-py3-none-any.whl` is installed unchanged. `Maze` wraps the external package:

```python
MazeGenerator(size=(width, height), seed=seed, perfect=False)
```

The adapter checks the returned dimensions and interprets the wall bits (north=1, east=2, south=4, west=8). Passage checks verify both neighboring cells and maze bounds. Breadth-first search identifies reachable cells for placement. Pac-Man starts near the center, and ghosts start near the corners. The first maze uses the configured seed; subsequent levels use random positive seeds. The seed controls maze generation, not necessarily every random gameplay decision.

## Implementation

The Pygame event loop processes input, updates the game with elapsed time and renders the current screen. Movement uses fractional cell coordinates and buffered direction changes. Ghosts use breadth-first search distances to chase or flee; the four ghosts share the same general decision algorithm. Power pellets activate frightened mode for seven seconds; eaten ghosts return to their starting positions and remain absent for six seconds. Score and lives carry over between levels, while the timer resets. Running out of time or lives ends the game.

Ordinary pellets are sampled from reachable cells, up to the configured `pacgum` maximum. A non-final level completion sets `level_complete` and pauses the engine; `advance_level()` generates the next maze only after confirmation.

The renderer uses theme palettes, cached wall surfaces, animated PNG sprites, HUD progress bars, particles and optional visual effects. `SpriteManager` loads assets once and caches scaled/oriented surfaces. The three Pac-Man frames follow the sequence 1–2–3–2; frightened ghosts alternate blue and white during the final two seconds when animations are enabled. The default frame limit is 60 FPS and can be changed in settings.

## General Software Architecture

| Module | Main responsibility |
|---|---|
| `pac-man.py` | CLI entry point |
| `pacman/configuration.py` | `Settings` and configuration validation |
| `pacman/app.py` | `App`: event loop, screen states and actions |
| `pacman/game.py` | `Game`: rules, score, collisions, timers and level progression |
| `pacman/maze.py` | `Maze`: external generator adapter and passage queries |
| `pacman/entities.py` | `Character`, `Player`, `Ghost`: movement and ghost AI |
| `pacman/highscores.py` | `Highscores`: leaderboard persistence |
| `pacman/ui.py` | `Renderer`: maze, HUD, overlays and visual cache |
| `pacman/sprites.py` | `SpriteManager`: PNG assets and animation |
| `pacman/themes.py` | Immutable `Theme` definitions |
| `pacman/widgets.py` | `Button`, text and progress-bar helpers |
| `pacman/menus.py` | `Menus`: layouts and keyboard/mouse navigation |
| `pacman/effects.py` | `Particle`, `ParticleSystem` and scanlines |
| `pacman/preferences.py` | `Preferences`: graphical settings persistence |

```text
pac-man.py -> Settings -> App
                          |-- Game -> Maze -> A-Maze-ing
                          |       -> Player / Ghost (inherit Character)
                          |-- Highscores
                          |-- Menus -> Button
                          |-- Preferences -> Theme definitions
                          `-- Renderer -> SpriteManager / ParticleSystem
```

The application coordinates the engine and presentation. The renderer reads game state rather than owning game rules. Menu actions are returned to `App`, which handles state transitions.

## Project Management

- **yaichi:** initial game skeleton, ghost AI, scoring, level management, random maze generation and placement logic.
- **nturcot:** Pygame integration, controls, graphical rendering, sprite animations, menus, themes and visual preferences.
- **Both:** integration, review, debugging, testing and delivery.

See [project management](project_management/) and the [development timeline and validation plan](project_management/PLAN.md) for milestones, risks and outstanding checks.

## Resources

- [Python documentation](https://docs.python.org/3/), including [pdb](https://docs.python.org/3/library/pdb.html) and [venv](https://docs.python.org/3/library/venv.html).
- [Pygame documentation](https://www.pygame.org/docs/).
- [PEP 8](https://peps.python.org/pep-0008/) and [PEP 257](https://peps.python.org/pep-0257/).
- [Flake8](https://flake8.pycqa.org/), [mypy](https://mypy.readthedocs.io/) and [pytest](https://docs.pytest.org/).
- Official 42 Pac-Man subject and assigned A-Maze-ing package.
- [Photopea](https://www.photopea.com/) and [HTML Color Codes](https://htmlcolorcodes.com/color-picker/) for graphical assets and palettes.

### AI assistance

ChatGPT was used to explain the maze representation, Python/OOP and debugging; propose and generate refactoring code for the engine and graphical integration; assist with sprite artwork, animation and caching; design and generate the themed UI modules and level-completion changes; diagnose installation errors; draft initial tests; and revise the README and project management plan. These contributions include generated code, not only conceptual advice. The team remains responsible for reviewing, understanding, testing and validating the resulting implementation. The original division of work refers to the initial student-developed subsystems, not exclusive authorship of every line in the refactored version.

## Packaging and validation status

The earlier graphical version was demonstrated in screenshots. The latest themed interface and level-completion patch have passed syntax checks but still require runtime regression testing. Full linting, subject compliance (including Pygame/MLX equivalence), packaging specification and public-platform publication remain to be confirmed. No completed public release is claimed here.
