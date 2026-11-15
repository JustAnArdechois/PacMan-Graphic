import random
from collections import deque

# One bit per wall, as in the maze package: a bit set to 1 is a wall.
WALLS: dict[str, int] = {"U": 1, "R": 2, "D": 4, "L": 8}

# How each direction changes (col, row).
MOVES: dict[str, tuple[int, int]] = {
    "U": (0, -1),
    "R": (1, 0),
    "D": (0, 1),
    "L": (-1, 0),
}
REVERSE: dict[str, str] = {"U": "D", "R": "L", "D": "U", "L": "R"}


def available_directions(
    maze: list[list[int]],
    col: int,
    row: int,
) -> list[str]:
    """List the directions with no wall from a cell.

    Args:
        maze: The maze grid, one wall bitmask per cell.
        col: Column of the cell.
        row: Row of the cell.
    Returns:
        The open directions, among "U", "R", "D" and "L".
    """
    cell = maze[row][col]
    directions: list[str] = []
    for direction, wall in WALLS.items():
        if not cell & wall:
            directions.append(direction)
    return directions


def random_direction(
    maze: list[list[int]],
    col: int,
    row: int,
    current: str,
) -> str:
    """Pick a random open direction, without turning back.

    The ghost only turns back when the cell is a dead end.

    Args:
        maze: The maze grid, one wall bitmask per cell.
        col: Column of the ghost.
        row: Row of the ghost.
        current: The direction the ghost is moving in.
    Returns:
        The new direction.
    """
    directions = available_directions(maze, col, row)
    if not directions:
        raise ValueError(f"ghost stuck in closed cell ({col}, {row})")
    forward: list[str] = []
    for d in directions:
        if d != REVERSE[current]:
            forward.append(d)
    if not forward:
        return REVERSE[current]
    return random.choice(forward)


def chase_direction(
    maze: list[list[int]],
    ghost: tuple[int, int],
    target: tuple[int, int],
    current: str,
) -> str:
    """Pick the first step of the shortest path to the target.

    Uses a BFS, so the ghost may turn back if the target is behind.
    Moves randomly if the target cannot be reached.

    Args:
        maze: The maze grid, one wall bitmask per cell.
        ghost: The (col, row) of the ghost.
        target: The (col, row) of the target.
        current: The direction the ghost is moving in.
    Returns:
        The new direction.
    """
    if ghost == target:
        return random_direction(maze, ghost[0], ghost[1], current)
    parents: dict[tuple[int, int], tuple[int, int]] = {}
    queue: deque[tuple[int, int]] = deque([ghost])
    while queue:
        col, row = queue.popleft()
        if (col, row) == target:
            break
        for direction in available_directions(maze, col, row):
            dx, dy = MOVES[direction]
            neighbor = (col + dx, row + dy)
            if neighbor != ghost and neighbor not in parents:
                parents[neighbor] = (col, row)
                queue.append(neighbor)
    if target not in parents:
        return random_direction(maze, ghost[0], ghost[1], current)
    # Backtrack to find the first step from ghost to target.
    step = target
    while parents[step] != ghost:
        step = parents[step]
    # Find the direction from ghost to step.
    move = (step[0] - ghost[0], step[1] - ghost[1])
    for direction, delta in MOVES.items():
        if delta == move:
            return direction
    raise AssertionError("first step is not next to the ghost")


def distances_from(
    maze: list[list[int]],
    start: tuple[int, int],
) -> dict[tuple[int, int], int]:
    """Count the steps from a cell to every reachable cell.

    Same BFS as chase_direction, but it explores the whole maze.

    Args:
        maze: The maze grid, one wall bitmask per cell.
        start: The starting cell, as (col, row).
    Returns:
        The distance to start of each reachable cell. Unreachable
        cells are not in it.
    """
    distances = {start: 0}
    queue: deque[tuple[int, int]] = deque([start])
    while queue:
        col, row = queue.popleft()
        for direction in available_directions(maze, col, row):
            dx, dy = MOVES[direction]
            neighbor = (col + dx, row + dy)
            if neighbor not in distances:
                distances[neighbor] = distances[(col, row)] + 1
                queue.append(neighbor)
    return distances


def flee_direction(
    maze: list[list[int]],
    ghost: tuple[int, int],
    threat: tuple[int, int],
    current: str,
) -> str:
    """Pick the direction that takes the ghost furthest from the threat.

    Each next cell is scored by its distance to the threat, and the
    furthest wins (ties are drawn at random). The ghost only turns
    back in a dead end, or when it is strictly better than every
    other way, otherwise it would go back and forth. Moves randomly
    if the threat cannot reach the ghost.

    Args:
        maze: The maze grid, one wall bitmask per cell.
        ghost: The (col, row) of the ghost.
        threat: The (col, row) to run away from.
        current: The direction the ghost is moving in.
    Returns:
        The new direction.
    """
    distances = distances_from(maze, threat)
    if ghost not in distances:
        return random_direction(maze, ghost[0], ghost[1], current)

    directions = available_directions(maze, ghost[0], ghost[1])
    if not directions:
        raise ValueError(f"ghost stuck in closed cell {ghost}")

    # Step 1: for each direction, how far from the threat would the
    # ghost be after one step?
    scores: dict[str, int] = {}
    for direction in directions:
        dx, dy = MOVES[direction]
        next_cell = (ghost[0] + dx, ghost[1] + dy)
        scores[direction] = distances[next_cell]

    # Step 2: by default, the ghost doesn't turn back.
    candidates: list[str] = []
    for direction in directions:
        if direction != REVERSE[current]:
            candidates.append(direction)

    # Step 3: in a dead end, turning back is the only way out.
    back = REVERSE[current]
    if not candidates:
        return back

    # Step 4: find the biggest score among the candidates.
    best_score = -1
    for direction in candidates:
        best_score = max(best_score, scores[direction])

    # Step 5: turn back only if it is strictly better than every other
    # way, for example when PacMan comes from the front. On a tie, it
    # would only make the ghost go back and forth.
    if back in scores and scores[back] > best_score:
        return back

    # Step 6: keep every candidate with that score, and pick one.
    best_directions: list[str] = []
    for direction in candidates:
        if scores[direction] == best_score:
            best_directions.append(direction)
    return random.choice(best_directions)
