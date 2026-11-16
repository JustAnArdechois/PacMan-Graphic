from typing import Any

from config_parser import get_int, log_error

LEVEL_COUNT = 10
# The maze package draws its 7x5 '42' pattern only if the maze is at
# least twice as big (mazegenerator.py, _add_42_to_maze). Below that,
# it prints a warning and silently skips the pattern.
MIN_WIDTH = 14
MIN_HEIGHT = 10


def default_level(index: int) -> dict[str, int]:
    """Build the default level for a position in the level list.

    Args:
        index: The position of the level, starting at 0.
    Returns:
        A dict with the default width and height for that level.
    """
    # Levels get bigger each time: 10, 20, 30... never below the
    # minimum size.
    size = 10 * (index + 1)
    return {"width": max(size, MIN_WIDTH), "height": max(size, MIN_HEIGHT)}


def parse_level(raw: Any, index: int) -> dict[str, int]:
    """Read one level from the config, falling back to its default.

    Args:
        raw: The level as json.loads gave it. Expected to be a dict.
        index: The position of the level, starting at 0.
    Returns:
        A dict with a valid width and height.
    """
    default = default_level(index)
    if not isinstance(raw, dict):
        log_error(f"level {index + 1} is not an object, using default")
        return default
    width = get_int(raw, "width", default["width"], minimum=MIN_WIDTH)
    height = get_int(raw, "height", default["height"], minimum=MIN_HEIGHT)
    return {"width": width, "height": height}


def get_levels(config: dict[str, Any]) -> list[dict[str, int]]:
    """Read the levels from the config, filling in defaults as needed.

    Args:
        config: The parsed config.
    Returns:
        A list of level dicts, each with a width and height.
    """
    raw_levels: list[Any] = []
    if "levels" in config:
        if isinstance(config["levels"], list):
            raw_levels = config["levels"]
        else:
            log_error("config key 'levels' must be a list, using defaults")
    # Keep the config's levels (fixed one by one if invalid), then
    # add default levels until there are LEVEL_COUNT.
    levels = [parse_level(raw, i) for i, raw in enumerate(raw_levels)]
    missing = LEVEL_COUNT - len(levels)
    if missing > 0:
        log_error(f"config is missing {missing} levels, using defaults")
    for i in range(len(levels), LEVEL_COUNT):
        levels.append(default_level(i))
    return levels
