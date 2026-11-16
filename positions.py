# A cell with walls on all four sides, one of the cells of the 42 logo.

CLOSED_CELL = 15


def manhattan(a: tuple[int, int], b: tuple[int, int]) -> int:
    """Count the steps between two cells on the grid, walls ignored.

    This is the Manhattan distance: the number of columns plus the
    number of rows between the two cells.

    Args:
        a: The first cell, as (col, row).
        b: The second cell, as (col, row).
    Returns:
        The distance between a and b.
    """
    # Like a taxi in Manhattan's grid of streets: it can only go
    # horizontally or vertically, so the distance is the gap on one
    # axis plus the gap on the other. abs() because a gap is never
    # negative: from 5 to 2 is 3 steps, like from 2 to 5.
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def nearest_open_cell(
    maze: list[list[int]],
    target: tuple[int, int],
) -> tuple[int, int]:
    """Find the open cell (not a 15) closest to the target.

    Args:
        maze: The maze grid, one wall bitmask per cell.
        target: The cell to get close to, as (col, row). It can be a
            closed cell.
    Returns:
        The nearest open cell, as (col, row).
    """
    height = len(maze)
    width = len(maze[0])
    found = False
    best_col = 0
    best_row = 0
    best_distance = 0

    for row in range(height):
        for col in range(width):
            cell = maze[row][col]  # row first the grid is read line by line
            if cell != CLOSED_CELL:
                distance = manhattan((col, row), target)
                # Keep the smallest distance seen so far. Strict <, so on
                # a tie the first cell found (top-left first) is kept.
                if not found or distance < best_distance:
                    found = True
                    best_col = col
                    best_row = row
                    best_distance = distance
    if not found:
        raise ValueError("No open cell found in the maze.")
    return (best_col, best_row)


def start_positions(
    maze: list[list[int]],
) -> tuple[tuple[int, int], list[tuple[int, int]]]:
    """Give the starting cells of PacMan and of the four ghosts.

    PacMan starts as close as possible to the center. Each ghost
    starts as close as possible to one corner.

    Args:
        maze: The maze grid, as given by MazeGenerator.maze.
    Returns:
        PacMan's cell, then the list of the four ghosts' cells, all as
        (col, row). Ghost order: top-left, top-right, bottom-left,
        bottom-right.
    """
    height = len(maze)
    width = len(maze[0])
    # // is integer division: 15 // 2 = 7, so the center is always a
    # real cell, even when the size is odd.
    center = (width // 2, height // 2)
    pacman = nearest_open_cell(maze, center)
    # Cells are numbered from 0, so the last column is width - 1
    # and the last row is height - 1.
    top_left = (0, 0)
    top_right = (width - 1, 0)
    bottom_left = (0, height - 1)
    bottom_right = (width - 1, height - 1)

    ghosts = []
    ghosts.append(nearest_open_cell(maze, top_left))
    ghosts.append(nearest_open_cell(maze, top_right))
    ghosts.append(nearest_open_cell(maze, bottom_left))
    ghosts.append(nearest_open_cell(maze, bottom_right))

    return pacman, ghosts
