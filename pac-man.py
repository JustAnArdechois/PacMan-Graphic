"""Pac-Man executable: python3 pac-man.py config.json."""
import sys
from pacman.configuration import load_settings


def main() -> int:
    """Validate CLI arguments and launch the application."""
    if len(sys.argv) != 2:
        print('Usage: python3 pac-man.py config.json', file=sys.stderr)
        return 1
    try:
        from pacman.app import App
        App(load_settings(sys.argv[1])).run()
    except Exception as exc:
        print(f'[fatal] {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
