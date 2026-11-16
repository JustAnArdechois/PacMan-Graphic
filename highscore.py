import json
import sys
from typing import Any

MAX_SCORES = 10
MAX_NAME_LENGTH = 10


def log_error(name: str) -> None:
    """Log an error message to stderr."""
    print(f"[highscore] {name}", file=sys.stderr)


def is_valid_name(name: str) -> bool:
    """Check that player name can go in the highscore file

    Args:
        name: The player name to check.
    Returns:
        True if the name is valid, False otherwise.
    """
    if len(name) < 1 or len(name) > MAX_NAME_LENGTH:
        return False
    if name.strip() == "":
        return False
    for char in name:
        is_letter_or_digit = char.isascii() and char.isalnum()
        if not is_letter_or_digit and char != " ":
            return False
    return True


def is_valid_score(score: Any) -> bool:
    """Check that score is an int, zero or more

    Booleans are rejected bc True == 1
    Args:
        score: The score to check.
    Returns:
        True if the score is valid, False otherwise.
    """
    if isinstance(score, bool) or not isinstance(score, int):
        return False
    return score >= 0


def get_score(entry: dict[str, Any]) -> int:
    """Give the score of an entry. Used to sort highscores

    Args:
        entry: One highscore like {"name": "Player", "score": 100}
    Returns:
        its score
    """
    score: int = entry["score"]
    return score


def keep_best(scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep the best scores, sorted from best to worst.

    Args:
        scores: The list of scores to filter and sort.
    Returns:
        The best scores, sorted from best to worst.
    """
    scores.sort(key=get_score, reverse=True)
    return scores[:MAX_SCORES]


def load_highscores(path: str) -> list[dict[str, Any]]:
    """Load the highscores from a JSON file.

    Never raises if the file is missing or malformed, just logs an error
    and returns an empty list.

    The file may have been edited by hand so each entry is checked
    too: a wrong entry is logged and skipped.
    Args:
        path: the path to the highscore file
    Returns:
        At most MAX_SCORES valid entries, sorted from best to worst
    """
    try:
        with open(path, "r", encoding="utf-8") as scores_file:
            data = json.load(scores_file)
    except FileNotFoundError:
        # Normal on the very first game: no file yet, no message
        return []
    except OSError as error:
        log_error(f"cannot read {path}: {error.strerror}")
    except UnicodeDecodeError:
        log_error(f"{path} is not a valid UTF-8 file")
        return []
    except json.JSONDecodeError as error:
        log_error(f"invalid JSON in {path}: {error.msg} "
                  f"(line {error.lineno})")
        return []

    if not isinstance(data, list):
        log_error(f"{path} must contain a JSON list")
        return []

    scores: list[dict[str, Any]] = []
    for index in range(len(data)):
        entry = data[index]
        if not isinstance(entry, dict):
            log_error(f"entry {index + 1} is not an object, skipped")
            continue
        name = entry.get("name")
        score = entry.get("score")
        if not isinstance(name, str) or not is_valid_name(name):
            log_error(f"entry {index + 1} has an invalid name, skipped")
            continue
        if not is_valid_score(score):
            log_error(f"entry {index + 1} has an invalid score, skipped")
            continue
        scores.append({"name": name, "score": score})
    return keep_best(scores)


def add_score(
        scores: list[dict[str, Any]],
        name: str,
        score: int,
        ) -> list[dict[str, Any]]:
    """Add a new score and keep the best ones.

    Args:
        scores: the current highscores
        name: the player's name. Check it first with is_valid_name
        score: the score of the game, zero or more
    Returns:
        A new list, at most MAX_SCORES entries, best first. The list given
        as argument is not changed.
    Raises:
        ValueError: if the name or the score is invalid.
        The game should never let this happen.
    """
    if not is_valid_name(name):
        raise ValueError(f"invalid player name: {name!r}")
    if not is_valid_score(score):
        raise ValueError(f"invalid score: {score!r}")
    new_scores = list(scores)
    new_scores.append({"name": name, "score": score})
    return keep_best(new_scores)


def save_highscores(path: str, scores: list[dict[str, Any]]) -> bool:
    """Write the highscore file.

    This never raises: if the disk refuses to write, the problem
    is logged and the game goes on.
    Args:
        path: Path to the highscores file
        scores: the highscores to save
    Returns:
        True if the file was written, False otherwise
    """
    try:
        with open(path, "w", encoding="utf-8") as scores_file:
            json.dump(scores, scores_file, indent=4)
    except OSError as error:
        log_error(f"cannot write {path}: {error.strerror}")
        return False
    return True
