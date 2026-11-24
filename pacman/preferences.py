"""Load and persist graphics preferences separately from game settings."""
from dataclasses import dataclass, asdict
from pathlib import Path
import json
from .themes import THEMES


@dataclass
class Preferences:
    theme: str = 'classic'
    glow: bool = True
    particles: bool = True
    animations: bool = True
    scanlines: bool = False
    show_fps: bool = False
    fullscreen: bool = False
    fps_limit: int = 60

    @classmethod
    def load(cls, path: Path = Path('preferences.json')) -> 'Preferences':
        prefs = cls()
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
            if not isinstance(data, dict):
                return prefs
            for key, default in asdict(prefs).items():
                value = data.get(key, default)
                if type(value) is type(default):
                    setattr(prefs, key, value)
            if prefs.theme not in THEMES:
                prefs.theme = 'classic'
            if prefs.fps_limit not in (30, 60, 120, 144):
                prefs.fps_limit = 60
        except (OSError, ValueError):
            pass
        return prefs

    def save(self, path: Path = Path('preferences.json')) -> None:
        try:
            path.write_text(json.dumps(asdict(self), indent=2) + '\n',
                            encoding='utf-8')
        except OSError as exc:
            print(f'[preferences] {exc}')
