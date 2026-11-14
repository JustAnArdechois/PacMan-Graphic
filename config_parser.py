import json
import sys
from typing import Any


def strip_comments(text: str) -> str:
    """Blank out every line whose first non-space character is '#'.

    Comment lines are emptied, not removed, so the line numbers in
    json error messages still match the original file. A '#' in the
    middle of a line is left alone.

    Args:
        text: The raw content of the configuration file.
    Returns:
        The text with its comment lines replaced by empty lines.
    """

    kept_lines: list[str] = []
    for line in text.splitlines():
        if line.lstrip().startswith("#"):
            kept_lines.append("")
        else:
            kept_lines.append(line)
    return "\n".join(kept_lines)


def log_error(message: str) -> None:
    """Print a config error on stderr, prefixed with '[config]'.

    Args:
        message: The message to print.
    """
    print(f"[config] {message}", file=sys.stderr)


def load_config(path: str) -> dict[str, Any]:
    """Read a config file, strip its comments and parse it as JSON.

    This never raises. If the file can't be read, isn't valid UTF-8,
    isn't valid JSON or doesn't hold an object at top level, the
    problem is logged and an empty dict is returned.

    Args:
        path: Path to the configuration file.
    Returns:
        The parsed config, or an empty dict if loading failed.
    """
    try:
        with open(path, "r", encoding="utf-8") as config_file:
            text = config_file.read()
        data = json.loads(strip_comments(text))
    except FileNotFoundError:
        log_error(f"file not found: {path}")
        return {}
    except OSError as error:
        log_error(f"cannot read {path}: {error.strerror}")
        return {}
    except UnicodeDecodeError:
        log_error(f"cannot decode {path} is not a valid UTF-8 file")
        return {}
    except json.JSONDecodeError as error:
        log_error(f"invalid JSON in {path}: {error.msg} (line {error.lineno})")
        return {}
    if not isinstance(data, dict):
        log_error(f"{path} must contain a JSON object at top level")
        return {}
    return data


def get_int(
    config: dict[str, Any],
    key: str,
    default: int,
    minimum: int | None = None,
) -> int:
    """Read an integer from the config, falling back to a default.

    A missing key silently gives the default. Booleans are rejected on
    purpose: in Python, True is an int, so "lives": true would otherwise
    be read as 1.

    Args:
        config: The parsed config.
        key: The key to read.
        default: The value used if the key is missing, not an integer,
            or below minimum.
        minimum: The smallest accepted value, or None for no lower bound.
    Returns:
        The integer stored under key, or the default.
    """
    if key not in config:
        return default
    value = config[key]

    if isinstance(value, bool) or not isinstance(value, int):
        log_error(
            f"config key '{key}' must be an int, using default"
        )
        return default
    if minimum is not None and value < minimum:
        log_error(
            f"config key '{key}' is too small ({value} < {minimum}), "
            f"using default"
        )
        return default
    return value


def get_str(
    config: dict[str, Any],
    key: str,
    default: str,
) -> str:
    """Read a string from the config, falling back to a default.

    Args:
        config: The parsed config.
        key: The key to read.
        default: The value used if the key is missing, not a string,
            or empty.
    Returns:
        The string stored under key, or the default.
    """
    if key not in config:
        return default
    value = config[key]
    if not isinstance(value, str):
        log_error(
            f"config key '{key}' must be a string, using default"
        )
        return default
    if value.strip() == "":
        log_error(
            f"config key '{key}' must not be empty, using default"
        )
        return default
    return value
