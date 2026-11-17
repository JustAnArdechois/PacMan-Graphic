*This activity has been created as part of the 42 curriculum by nturcot and yaichi.*

# Pac-Man — object-oriented Python game

## Description
A graphical Pac-Man game with ten or more generated mazes, autonomous ghosts, pellets, lives, scores, pause, and a reviewer cheat mode. Written in Python 3.10+ with an object-oriented architecture.

## Instructions
Create a virtual environment (recommended), then run `make install` and `make run`, or directly `python3 pac-man.py config.json`. `make debug`, `make clean`, and `make lint` are also available. The provided A-Maze-ing wheel is installed unchanged.

Controls: arrow keys / WASD / ZQSD move; ESC pauses; ENTER resumes; M returns to menu while paused. F1 displays reviewer cheats; 1 toggles invulnerability, 2 skips a level, 3 freezes ghosts, 4 adds a life, 5 toggles speed boost. In the menu ENTER plays, H displays highscores, I shows instructions and ESC quits.

## Configuration
The JSON file accepts full-line `#` comments. Supply exactly one `.json` path as the command-line argument. Missing or invalid entries fall back to defaults and report a warning. Unknown keys are ignored. `levels` is an array of `{ "width": ..., "height": ... }` with at least ten entries; minimum 14×10 to accommodate the assigned generator's logo. `lives` defaults to 3, `pacgum` to 42 (maximum number of ordinary dots per level), `points_per_pacgum` to 10, `points_per_super_pacgum` to 50, `points_per_ghost` to 200, `seed` to 42, `level_max_time` to 90 seconds and `highscore_filename` to `highscores.json`. First maze uses the configured seed; subsequent mazes use random positive seeds.

## Highscore
Scores are stored as JSON in the configured path. Only non-negative integer scores and 1–10-character ASCII alphanumeric/space names are accepted. Scores are sorted descending, and only the top ten are saved. Read failures are nonfatal. At the end of a win or loss, the player enters a name; scores are visible in the main menu.

## Maze Generation
The external assigned `mazegenerator` package is used as-is with `MazeGenerator(size=(width,height), seed=seed, perfect=False)`. The adapter checks dimensions and wall bitmasks. No custom maze generation algorithm is used. The installed wheel must be available during review.

## Implementation
The main loop runs at 60 FPS with time-based movement. Ghosts use breadth-first search distances to chase or flee. A large pellet temporarily makes ghosts edible. Eaten ghosts respawn at their starting corners after a delay. The player keeps score and lives between levels; the timer resets each level. Timeout ends the game. The `pacgum` setting is interpreted as a per-level maximum of ordinary dots; this is a documented implementation choice.

## General Software Architecture
`pac-man.py` is the CLI entry point. `App` owns UI state and input; `Renderer` draws menus and the game; `Game` owns progression, score and collisions; `Maze` adapts the external generator; `Character` implements movement, and `Player` and `Ghost` inherit from it. `Settings` validates configuration and `Highscores` manages persistence.

## Project Management
See `project_management/` for implementation notes and a checklist. The original team members should update this section with their actual roles, timeline, decisions and review evidence.

## Resources
Python documentation, Pygame documentation, PEP 8, PEP 257, the assigned A-Maze-ing wheel, and the official 42 Pacman v1.5 subject. AI assistance was used to propose architecture, refactor gameplay, draft documentation and write initial tests. All generated code must be reviewed, understood and validated by the team before submission.

## Packaging
A public-platform build (e.g. Itch.io) and packaging specification are **not yet provided**; these require testing and publishing by the team. A packaging spec should be committed at the repository root before submission.

## Important limitations
The renderer uses basic Pygame primitives rather than the original uploaded sprites because those sprite assets were not all available in the provided uploads. MLX equivalence of all used Pygame calls must be reviewed with evaluators. No claim of complete subject compliance is made until linting, runtime testing, packaging and publishing are finished.

### Original sprites / SpriteManager

The `assets/` folder contains the original Pac-Man, four directional ghosts,
PacGum and Super_PacGum PNGs. `pacman/sprites.py` loads them once on startup,
caches scaled and rotated versions, and draws the original 3-frame Pac-Man
animation. The frightened blue/white ghost images in `assets/ghosts/frightened/`
are recolored variants of the supplied red ghost sprite, to match the art style.
All ghosts flash blue/white during the final 2 seconds of frightened mode.

The renderer (`pacman/ui.py`) delegates sprite drawing to `SpriteManager`.
Game rules, movement and ghost AI remain in their original classes.

https://www.photopea.com/
https://htmlcolorcodes.com/color-picker/
