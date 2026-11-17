"""Pure-Python regression checks for configuration and highscores."""
from pacman.configuration import load_settings
from pacman.highscores import Highscores


def test_invalid_config_uses_defaults(tmp_path: object) -> None:
    """An unreadable configuration should not crash."""
    settings = load_settings('/nonexistent/config.json')
    assert len(settings.levels) >= 10
    assert settings.lives == 3


def test_highscores_top_ten(tmp_path: object) -> None:
    """Scores are sorted, validated and limited to ten."""
    from pathlib import Path
    path = Path(str(tmp_path)) / 'scores.json'
    scores = Highscores(str(path))
    for n in range(12):
        assert scores.add(f'P{n}', n)
    assert len(scores.entries) == 10
    assert scores.entries[0]['score'] == 11
    assert not scores.add('invalid!', 100)
    assert len(Highscores(str(path)).entries) == 10
