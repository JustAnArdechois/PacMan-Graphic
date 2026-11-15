from dataclasses import dataclass

from config_parser import get_int, get_str, load_config
from levels import get_levels


@dataclass
class Config:
    """Every setting the game needs, already parsed and validated."""
    highscore_filename: str
    levels: list[dict[str, int]]
    lives: int
    pacgum: int
    points_per_pacgum: int
    points_per_ghost: int
    points_per_super_pacgum: int
    seed: int
    level_max_time: int


def load_game_config(filename: str) -> Config:
    """Load the config file and return a Config object with all settings.

    This never raises. Every missing or invalid setting is replaced
    with a default and logged.

    Args:
        filename: The path to the config file.
    Returns:
        A Config object with all settings.
    """
    data = load_config(filename)
    return Config(
        highscore_filename=get_str(data, "highscore_filename",
                                   "highscores.json"),
        levels=get_levels(data),
        lives=get_int(data, "lives", 3, minimum=1),
        pacgum=get_int(data, "pacgum", 42, minimum=1),
        points_per_pacgum=get_int(data, "points_per_pacgum", 10, minimum=0),
        points_per_ghost=get_int(data, "points_per_ghost", 200, minimum=0),
        points_per_super_pacgum=get_int(data, "points_per_super_pacgum",
                                        50, minimum=0),
        seed=get_int(data, "seed", 42, minimum=1),
        level_max_time=get_int(data, "level_max_time", 90, minimum=1)
    )
