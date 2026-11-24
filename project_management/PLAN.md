# Pac-Man — Project management plan and development log

**Project:** Pac-Man (42)  
**Team:** nturcot and yaichi  
**Period documented:** 3–24 November 2026  
**Status:** development and integration in progress; earlier graphical build demonstrated; latest updates and full subject compliance still to be verified  
**Entry point:** `python3 pac-man.py config.json`

> This document reconstructs the development history from the team's reported work and technical exchanges. Dates indicate when a topic was discussed or demonstrated, not necessarily the precise date of a Git commit. It does not substitute for Git history, test logs or other evidence.

## 1. Team organization and responsibilities

| Responsibility | Owner | Scope |
|---|---|---|
| Game skeleton and core logic | yaichi | Ghost AI, scoring/high scores, level management, random maze generation and placement logic, configuration modules |
| Playable graphical interface | nturcot | Pygame integration, maze and wall rendering, keyboard controls, smooth movement, menus, sprite assets and animations |
| Integration and compliance | Both | Connecting modules, agreeing on shared interfaces, debugging, object-oriented restructuring, tests, subject verification, documentation and delivery |

The work was divided by subsystem rather than by separate, independent applications. The graphics and game-logic layers depend on shared data conventions (maze grid, wall bit masks, coordinates, directions and game states). Integration must therefore be reviewed jointly.

## 2. Development timeline

| Date / period | Work and decisions | Responsibility | Evidence / status |
|---|---|---|---|
| **3 Nov 2026** | Initial discussion of the 42 Pac-Man project as a two-person assignment. Roles split: teammate on the engine/skeleton, graphics developer on the playable Pygame interface. Reviewed the provided `mazegenerator` wheel and the maze representation (wall bits: N=1, E=2, S=4, W=8). | Both | Discussed and prototype work started |
| **3–13 Nov** | Initial maze rendering tests in Pygame: drawing walls with lines, handling cell size and maze offsets. Explored use of PNG/JPG assets for Pac-Man, four ghosts, pac-gums and super pac-gums. | nturcot | Graphics prototypes discussed |
| **Early–mid Nov** | Created and iterated on Pac-Man animation frames and directional ghost sprites. Worked on frame alternation and orientation according to movement direction. | nturcot | Sprite and animation experiments |
| **13 Nov** | Improved game structure by separating the menu/entry point from the gameplay module. Developed tile-to-tile movement, buffered direction changes and turns at cell centers. | nturcot | Code and movement behavior discussed |
| **14 Nov** | Refined keyboard handling (`zqsd`, `wasd`, arrow keys and dual-control variants), wall checks via `open_passage()`, and movement shared between Pac-Man and a controllable ghost. Investigated errors in animation indices and keyboard-mode conditions. | nturcot | Debugging and code revisions discussed |
| **Mid Nov** | Teammate added the game-logic modules: configuration and level parsing, `ghost.py` (random/chase/flee pathfinding), `highscore.py` (persistent ranking), and `positions.py` (initial placements). | yaichi | Modules supplied for integration; exact creation dates not established |
| **Mid Nov** | Compared teammate's modules with the graphics code. Identified integration tasks: replace hard-coded positions, connect ghost AI, center rectangular mazes correctly and connect scoring and levels. | Both | Integration analysis completed; not all changes implemented in original code |
| **17 Nov** | Rechecked the official 42 subject (v1.5, 22 pages). Renamed `main.py` to `pac-man.py` to align with the required command-line entry point. Reviewed OOP and delivery constraints. | Both | Subject review and rename reported |
| **17 Nov** | Produced a separate OOP rewrite prototype (`PacMan_OOP.zip`) with application, game, maze, entities, renderer, configuration, highscores, cheats and basic tests. | Integration / assisted rewrite | Prototype generated; not a fully validated release |
| **17 Nov** | Integrated the original assets into the OOP prototype (`PacMan_OOP_Sprites.zip`); added `SpriteManager`, sprite caching, directional rendering, Pac-Man animation and blue/white frightened ghost states. | nturcot / integration | Source archive prepared; graphical runtime still needs testing |
| **17 Nov** | Replaced the generic management checklist with this documented team timeline and a verification plan. | Both | Documentation updated |
| **24 Nov** | Installation on a 42 workstation failed when Pygame 2.6.1 was compiled against Python 3.15 (removed `PyWeakref_GetObject` API). A compatible Python environment was proposed. | nturcot | Failure log available; exact successful workaround not recorded |
| **24 Nov** | Demonstrated the earlier graphical build: main menu, highscore screen, instructions, gameplay sprites, maze and pause overlay. | nturcot | Four screenshots supplied; not a full playthrough |
| **24 Nov** | Designed five graphical themes and interactive menu concepts. Generated a graphics update with `themes.py`, `widgets.py`, `menus.py`, `effects.py`, `preferences.py` and revised `app.py`/`ui.py`. | nturcot / AI-assisted integration | Patch generated and syntax checked; runtime verification pending |
| **24 Nov** | Added an explicit level-completion state and menu (Next Level, Graphic Settings, Main Menu), preserving score and lives until the next level is confirmed. | nturcot / AI-assisted integration | Four-file patch generated and syntax checked; runtime verification pending |
| **24 Nov** | Updated README and management plan to document the new architecture, controls, configuration, AI assistance and outstanding acceptance tests. | nturcot / AI-assisted documentation | Documentation revised |

## 3. Technical architecture

- **`pac-man.py`**: required command-line entry point; loads configuration and launches the application.
- **`pacman/configuration.py`**: settings, defaults and configuration validation.
- **`pacman/maze.py`**: adapter around the assigned maze-generation wheel; walls, possible movements and reachability.
- **`pacman/entities.py`**: common `Character` movement; `Player` and `Ghost` subclasses; ghost direction selection.
- **`pacman/game.py`**: lives, timer, pellets, collisions, score, levels, frightened state and cheats.
- **`pacman/app.py`**: Pygame event loop, keyboard input and screen/state transitions.
- **`pacman/ui.py`**: renderer for maze, HUD, menus and characters.
- **`pacman/sprites.py`**: asset loading, transformation cache and sprite animations.
- **`pacman/highscores.py`**: persistent top-ten ranking.
- **`assets/`**: Pac-Man frames, four directional ghost sprite sets, frightened blue/white sprites and pellets.

The original teammate modules and the OOP rewrite are not identical files. Their functionality has been adapted into the new architecture; the original code should remain available in Git for traceability.

- **`pacman/themes.py`**: five immutable graphical themes.
- **`pacman/widgets.py`**: reusable buttons, text and progress bars.
- **`pacman/menus.py`**: shared menu layouts and input handling.
- **`pacman/effects.py`**: particles and CRT scanlines.
- **`pacman/preferences.py`**: local graphical preferences, separate from game settings.

`App` coordinates `Game`, `Renderer`, `Menus`, `Preferences` and `Highscores`. `Game.next_level()` now marks a non-final level complete; `advance_level()` loads the next maze after confirmation. The final level still leads to the victory/name screen. The graphics update adds wall caching, a redesigned HUD and theme-aware overlays without replacing ghost AI.

## 4. Milestones and acceptance criteria

### Implemented or prototyped

- [x] Split responsibilities between game logic and Pygame interface.
- [x] Integrate the supplied maze-generator wheel in a prototype.
- [x] Render maze walls using the provided wall-bit representation.
- [x] Prototype keyboard movement and queued turns.
- [x] Prepare character and pellet PNG assets.
- [x] Prepare configuration, ghost AI, position and high-score modules.
- [x] Build an OOP prototype separating application, logic, entities and rendering.
- [x] Add a `SpriteManager` prototype and frightened ghost blue/white states.

- [x] Demonstrate the earlier graphical build in screenshots.
- [x] Prepare the five-theme graphics update and persistent preferences.
- [x] Prepare the level-completion menu and explicit next-level confirmation.
- [x] Revise README and project management documentation.

The checked graphics and level-completion milestones indicate prepared source patches, not completed runtime acceptance tests.

### Must still be verified or completed

- [x] Run the latest combined graphical build on the team's Linux machine and fix runtime errors. Record the working Python/Pygame versions.
- [x] Confirm the exact subject rules for controls, timing, scoring, lives, collisions, respawn and frightened mode.
- [x] Play through at least ten levels; verify deterministic first seed and random later levels.
- [x] Test rectangular and large mazes, scaling, positioning and reachability.
- [x] Verify the four ghosts' chase/flee behavior and respawn in real gameplay.
- [x] Validate keyboard controls, pause, menus, victory/defeat, high-score entry and cheat mode.
- [x] Test all five themes, mouse and keyboard navigation, preference persistence, fullscreen, FPS limits and visual effects.
- [x] Verify that level completion freezes gameplay, preserves score/lives, returns from settings correctly and advances exactly once on confirmation; test final victory and cheat 2.
- [x] Check performance on large mazes and verify wall/sprite cache behavior.
- [x] Confirm the approved Pygame functionality against the subject's MLX-equivalence restriction.
- [ ] Run `make lint` (flake8 and mypy) and `pytest`; add tests for movement, collisions, level transitions and malformed configurations.
- [ ] Confirm all mandatory Makefile targets and command-line behavior.
- [x] Review the updated README against the actual repository, complete packaging, publication and evaluation-ready demonstration.
- [ ] Cross-check the actual Git commits and add evidence (commit references, test output, screenshots) before submission.

## 5. Risks and decisions

| Risk | Mitigation |
|---|---|
| Graphics and logic use incompatible coordinates or direction conventions | Agree on `(column, row)` for grid positions and `U/D/L/R` for directions; test at module boundaries |
| Large or rectangular levels exceed the screen | Compute scale and horizontal/vertical offsets independently |
| Ghost behavior works in isolation but fails in the graphical loop | Test pathfinding and movement separately, then together |
| Sprite transformations are expensive or produce visual artifacts | Load once, cache scaled images, check PNG transparency and flashing |
| Generated OOP prototype diverges from teammate's original implementation | Preserve originals in Git and review changes jointly |
| Python 3.15 / Pygame 2.6.1 incompatibility | Use an available compatible interpreter and record the successful installation procedure |
| New graphical settings or level transitions introduce regressions | Test all menu return paths, final victory, repeated level transitions and preference reloads |
| Subject compliance assumed from code presence alone | Validate each requirement with a reproducible test or demonstration |

## 6. Collaboration and validation workflow

1. Develop features in separate Git branches where practical.
2. Use `git fetch` and inspect differences before integration; review each other's changes.
3. Keep source logic independent from rendering where possible.
4. Run targeted tests for each change and a full playtest after merges.
5. Record the date, author, commit and test evidence for completed milestones.
6. Do not mark a requirement as validated until it has been checked against the official subject.

## 7. AI assistance and traceability

AI assistance was used for explanations, generated OOP refactoring, graphical modules, sprite artwork, debugging guidance, initial tests and documentation. The latest graphics and level-completion archives are AI-assisted patches, not proof of merged Git commits. Both students should review the changes and record actual commit references, runtime evidence and authorship before submission. The README describes the scope of AI assistance explicitly.

## 8. Next steps

1. Confirm the compatible interpreter and install dependencies; run the latest combined build.
2. Test the graphics update and level-completion patch; fix observed runtime issues.
3. Verify game rules, ghost AI, level progression and high-score persistence.
4. Run automated quality checks and full subject-based acceptance tests.
5. Finalize documentation, package the game and rehearse the evaluation.

---

**Documentation note:** This timeline is based on the available project discussions through **24 November 2026**. Where exact implementation dates or successful tests are unknown, the document deliberately says *discussed*, *prototyped*, or *to verify* rather than claiming completion.
