"""Configuration parsing and validation."""
from dataclasses import dataclass
import json
import sys
from pathlib import Path
from typing import Any


@dataclass
class Settings:
    """Validated game settings."""
    levels: list[tuple[int, int]]
    lives: int = 3
    pacgum: int = 42
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 50
    points_per_ghost: int = 200
    seed: int = 42
    level_max_time: int = 90
    highscore_filename: str = 'highscores.json'


def warn(message: str) -> None:
    """Report a recoverable configuration problem."""
    print(f'[config] {message}', file=sys.stderr)


def integer(data: dict[str, Any], key: str, default: int,
            minimum: int) -> int:
    """Return a validated integer, falling back on defaults."""
    value = data.get(key, default)
    if type(value) is not int or value < minimum:
        warn(f'{key}: invalid value; using {default}')
        return default
    return value


def load_settings(path: str) -> Settings:
    """Read JSON with full-line hash comments and safe defaults."""
    if Path(path).suffix.lower() != '.json':
        warn('configuration must be a .json file; using defaults')
        data: Any = {}
    else:
        try:
            lines = Path(path).read_text(encoding='utf-8').splitlines()
            cleaned = '\n'.join('' if line.lstrip().startswith('#')
                                else line for line in lines)
            data = json.loads(cleaned)
        except (OSError, UnicodeError, ValueError) as exc:
            warn(f'cannot load {path}: {exc}; using defaults')
            data = {}
    if not isinstance(data, dict):
        warn('configuration root must be an object; using defaults')
        data = {}
    raw_levels = data.get('levels', [])
    if not isinstance(raw_levels, list):
        warn('levels must be a list; using defaults')
        raw_levels = []
    levels = []
    for i in range(max(10, len(raw_levels))):
        item = raw_levels[i] if i < len(raw_levels) else {}
        if not isinstance(item, dict):
            item = {}
        default = max(14, (i + 1) * 10)
        width = integer(item, 'width', default, 14)
        height = integer(item, 'height', max(10, (i + 1) * 10), 10)
        levels.append((width, height))
    filename = data.get('highscore_filename', 'highscores.json')
    if not isinstance(filename, str) or not filename.strip():
        warn('invalid highscore_filename; using default')
        filename = 'highscores.json'
    return Settings(
        levels=levels,
        lives=integer(data, 'lives', 3, 1),
        pacgum=integer(data, 'pacgum', 42, 1),
        points_per_pacgum=integer(data, 'points_per_pacgum', 10, 0),
        points_per_super_pacgum=integer(
            data, 'points_per_super_pacgum', 50, 0),
        points_per_ghost=integer(data, 'points_per_ghost', 200, 0),
        seed=integer(data, 'seed', 42, 1),
        level_max_time=integer(data, 'level_max_time', 90, 1),
        highscore_filename=filename)
