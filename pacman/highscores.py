"""Persistent validated top-ten leaderboard."""
import json
from pathlib import Path
from typing import Any


class Highscores:
    """Load and save a top-ten leaderboard."""

    def __init__(self, filename: str) -> None:
        """Read the leaderboard at game startup."""
        self.path = Path(filename)
        self.entries: list[dict[str, Any]] = []
        try:
            data = json.loads(self.path.read_text(encoding='utf-8'))
            if isinstance(data, list):
                for entry in data:
                    if (isinstance(entry, dict) and
                            self.valid_name(entry.get('name')) and
                            type(entry.get('score')) is int and
                            entry['score'] >= 0):
                        self.entries.append({'name': entry['name'],
                                             'score': entry['score']})
        except (OSError, UnicodeError, ValueError) as exc:
            if self.path.exists():
                print(f'[highscores] read error: {exc}')
        self.entries = self.sorted_entries()

    @staticmethod
    def valid_name(name: Any) -> bool:
        """Accept 1-10 ASCII letters, digits and spaces."""
        return (isinstance(name, str) and 1 <= len(name) <= 10 and
                bool(name.strip()) and
                all(c == ' ' or (c.isascii() and c.isalnum())
                    for c in name))

    def sorted_entries(self) -> list[dict[str, Any]]:
        """Sort and retain ten highest scores."""
        return sorted(self.entries, key=lambda e: e['score'],
                      reverse=True)[:10]

    def add(self, name: str, score: int) -> bool:
        """Validate, add and persist a score."""
        if not self.valid_name(name) or type(score) is not int or score < 0:
            return False
        self.entries.append({'name': name, 'score': score})
        self.entries = self.sorted_entries()
        try:
            self.path.write_text(json.dumps(self.entries, indent=2),
                                 encoding='utf-8')
            return True
        except OSError as exc:
            print(f'[highscores] save error: {exc}')
            return False
