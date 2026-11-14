import pygame
import colors

MOVEMENTS = {
        "U": (0, -1),
        "D": (0, 1),
        "L": (-1, 0),
        "R": (1, 0)
}

WALL_BITS = {
    "U": 1,
    "R": 2,
    "D": 4,
    "L": 8
}


def show_wall(
    screen: pygame.Surface,
    pos: int,
    cell_size: int,
    maze: list[list[int]]
) -> None:
    for row_index, row in enumerate(maze):
        for col_index, cell in enumerate(row):
            px = pos + col_index * cell_size
            py = pos + row_index * cell_size

            if cell & 1:  # Nord
                pygame.draw.line(
                    screen,
                    colors.BLUE,
                    (px, py),
                    (px + cell_size, py),
                    2
                )

            if cell & 2:  # Est
                pygame.draw.line(
                    screen,
                    colors.BLUE,
                    (px + cell_size, py),
                    (px + cell_size, py + cell_size),
                    2
                )

            if cell & 4:  # Sud
                pygame.draw.line(
                    screen,
                    colors.BLUE,
                    (px, py + cell_size),
                    (px + cell_size, py + cell_size),
                    2
                )

            if cell & 8:  # Ouest
                pygame.draw.line(
                    screen,
                    colors.BLUE,
                    (px, py),
                    (px, py + cell_size),
                    2
                )


def PacGum(
    screen: pygame.Surface,
    pos_x: int,
    pos_y: int,
    scale: int
) -> None:
    pacgum = pygame.image.load("assets/PacGum.png").convert_alpha()

    # Redimensionner à 20 × 20 pixels
    pacgum = pygame.transform.scale(pacgum, (scale // 1.5, scale // 1.5))

    # Afficher l'image aux coordonnées (100, 80)
    screen.blit(pacgum, (pos_x, pos_y))


def PacGum_Super(
    screen: pygame.Surface,
    pos_x: int,
    pos_y: int,
    scale: int
) -> None:
    pacgum_super = pygame.image.load("assets/Super_PacGum.png").convert_alpha()

    # Redimensionner à 20 × 20 pixels
    pacgum_super = pygame.transform.scale(
        pacgum_super,
        (scale // 1.2, scale // 1.2)
    )

    # Afficher l'image aux coordonnées (100, 80)
    screen.blit(pacgum_super, (pos_x, pos_y))


def PacMan_Movements(
    screen: pygame.Surface,
    animation: list[int],
    animation_speed: int,
    pos: tuple[int, int, str],
    scale: float
) -> None:
    images_PacMan = [
        pygame.transform.scale(
            pygame.image.load("assets/PacMan_1.png").convert_alpha(),
            (scale, scale),
        ),
        pygame.transform.scale(
            pygame.image.load("assets/PacMan_2.png").convert_alpha(),
            (scale, scale),
        ),
        pygame.transform.scale(
            pygame.image.load("assets/PacMan_3.png").convert_alpha(),
            (scale, scale),
        ),
    ]
    frame = (
        pygame.time.get_ticks() // animation_speed
    ) % len(animation)

    image_index = animation[frame]

    if pos[2] == "U":
        images_PacMan[image_index] = pygame.transform.rotate(
            images_PacMan[image_index], 90
        )
    elif pos[2] == "D":
        images_PacMan[image_index] = pygame.transform.rotate(
            images_PacMan[image_index], -90
        )
    elif pos[2] == "L":
        images_PacMan[image_index] = pygame.transform.flip(
            images_PacMan[image_index], True, False
        )
    screen.blit(images_PacMan[image_index], (pos[0], pos[1]))


def test_Blue_Ghost_animation(
    screen: pygame.Surface,
    pos: tuple[int, int, str],
    animation: list[int],
    animation_speed: int,
    scale: float
) -> None:
    images_Blue_Ghost = [
        pygame.transform.scale(
            pygame.image.load("assets/Blue_Ghost_U.png").convert_alpha(),
            (scale, scale),
        ),
        pygame.transform.scale(
            pygame.image.load("assets/Blue_Ghost_D.png").convert_alpha(),
            (scale, scale),
        ),
        pygame.transform.scale(
            pygame.image.load("assets/Blue_Ghost_L.png").convert_alpha(),
            (scale, scale),
        ),
        pygame.transform.scale(
            pygame.image.load("assets/Blue_Ghost_R.png").convert_alpha(),
            (scale, scale),
        ),
    ]
    '''frame = (
            pygame.time.get_ticks() // animation_speed
        ) % len(animation)'''

    image_index = {
        "U": 0,
        "D": 1,
        "L": 2,
        "R": 3
    }[pos[2]]

    if pos[2] == "U":
        images_Blue_Ghost[image_index] = pygame.transform.rotate(
            images_Blue_Ghost[image_index], 90
        )
    elif pos[2] == "D":
        images_Blue_Ghost[image_index] = pygame.transform.rotate(
            images_Blue_Ghost[image_index], -90
        )
    elif pos[2] == "L":
        images_Blue_Ghost[image_index] = pygame.transform.flip(
            images_Blue_Ghost[image_index], True, False
        )
    screen.blit(images_Blue_Ghost[image_index], (pos[0], pos[1]))


def test_Red_Ghost_animation(
    screen: pygame.Surface,
    pos_x: int,
    pos_y: int,
    direction: str,
) -> None:
    images_Red_Ghost = [
        pygame.transform.scale(
            pygame.image.load(
                "assets/Red_Ghost_U.png"
            ).convert_alpha(),
            (pos_y, pos_y),
        ),
        pygame.transform.scale(
            pygame.image.load(
                "assets/Red_Ghost_D.png"
            ).convert_alpha(),
            (pos_y, pos_y),
        ),
        pygame.transform.scale(
            pygame.image.load(
                "assets/Red_Ghost_L.png"
            ).convert_alpha(),
            (pos_y, pos_y),
        ),
        pygame.transform.scale(
            pygame.image.load(
                "assets/Red_Ghost_R.png"
            ).convert_alpha(),
            (pos_y, pos_y),
        ),
    ]
    if direction == "U":
        screen.blit(images_Red_Ghost[0], (pos_x, pos_y))
    elif direction == "D":
        screen.blit(images_Red_Ghost[1], (pos_x, pos_y))
    elif direction == "L":
        screen.blit(images_Red_Ghost[2], (pos_x, pos_y))
    elif direction == "R":
        screen.blit(images_Red_Ghost[3], (pos_x, pos_y))


def test_Orange_Ghost_animation(
    screen: pygame.Surface,
    pos_x: int,
    pos_y: int,
    direction: str,
) -> None:
    images_Orange_Ghost = [
        pygame.transform.scale(
            pygame.image.load(
                "assets/Orange_Ghost_U.png"
            ).convert_alpha(),
            (pos_y, pos_y),
        ),
        pygame.transform.scale(
            pygame.image.load(
                "assets/Orange_Ghost_D.png"
            ).convert_alpha(),
            (pos_y, pos_y),
        ),
        pygame.transform.scale(
            pygame.image.load(
                "assets/Orange_Ghost_L.png"
            ).convert_alpha(),
            (pos_y, pos_y),
        ),
        pygame.transform.scale(
            pygame.image.load(
                "assets/Orange_Ghost_R.png"
            ).convert_alpha(),
            (pos_y, pos_y),
        ),
    ]
    if direction == "U":
        screen.blit(images_Orange_Ghost[0], (pos_x, pos_y))
    elif direction == "D":
        screen.blit(images_Orange_Ghost[1], (pos_x, pos_y))
    elif direction == "L":
        screen.blit(images_Orange_Ghost[2], (pos_x, pos_y))
    elif direction == "R":
        screen.blit(images_Orange_Ghost[3], (pos_x, pos_y))


def test_Pink_Ghost_animation(
    screen: pygame.Surface,
    pos_x: int,
    pos_y: int,
    direction: str
) -> None:
    images_Pink_Ghost = [
        pygame.transform.scale(
            pygame.image.load("assets/Pink_Ghost_U.png").convert_alpha(),
            (pos_y, pos_y)
        ),
        pygame.transform.scale(
            pygame.image.load("assets/Pink_Ghost_D.png").convert_alpha(),
            (pos_y, pos_y)
        ),
        pygame.transform.scale(
            pygame.image.load("assets/Pink_Ghost_L.png").convert_alpha(),
            (pos_y, pos_y)
        ),
        pygame.transform.scale(
            pygame.image.load("assets/Pink_Ghost_R.png").convert_alpha(),
            (pos_y, pos_y)
        ),
    ]
    if direction == "U":
        screen.blit(images_Pink_Ghost[0], (pos_x, pos_y))
    elif direction == "D":
        screen.blit(images_Pink_Ghost[1], (pos_x, pos_y))
    elif direction == "L":
        screen.blit(images_Pink_Ghost[2], (pos_x, pos_y))
    elif direction == "R":
        screen.blit(images_Pink_Ghost[3], (pos_x, pos_y))


def can_move(
    maze: list[list[int]],
    x: float,
    y: float,
    direction: str,
    speed: float,
    cell_size: int,
    maze_pos: int,
    radius: float,
    margin: float = 2
) -> bool:

    if direction not in MOVEMENTS:
        return False

    dx, dy = MOVEMENTS[direction]

    # Position du centre après déplacement
    next_x = x + dx * speed
    next_y = y + dy * speed

    # Rayon de collision avec marge
    r = radius + margin

    # Limites du labyrinthe
    left = maze_pos
    top = maze_pos
    right = left + len(maze[0]) * cell_size
    bottom = top + len(maze) * cell_size

    if (
        next_x - r < left
        or next_x + r > right
        or next_y - r < top
        or next_y + r > bottom
    ):
        return False

    # Vérifier les segments de murs proches
    for row, cells in enumerate(maze):
        for col, cell in enumerate(cells):
            px = left + col * cell_size
            py = top + row * cell_size

            walls = []

            if cell & 1:  # Nord
                walls.append((px, py, px + cell_size, py))
            if cell & 2:  # Est
                walls.append((
                    px + cell_size, py,
                    px + cell_size, py + cell_size
                ))
            if cell & 4:  # Sud
                walls.append((
                    px, py + cell_size,
                    px + cell_size, py + cell_size
                ))
            if cell & 8:  # Ouest
                walls.append((px, py, px, py + cell_size))

            for x1, y1, x2, y2 in walls:
                # Point du mur le plus proche du centre
                closest_x = max(min(x1, x2), min(next_x, max(x1, x2)))
                closest_y = max(min(y1, y2), min(next_y, max(y1, y2)))

                distance_sq = (
                    (next_x - closest_x) ** 2
                    + (next_y - closest_y) ** 2
                )

                if distance_sq < r ** 2:
                    return False

    return True


def open_passage(
    col: int,
    row: int,
    facing: str,
    maze: list[list[int]]
) -> bool:
    dx, dy = MOVEMENTS[facing]
    new_col, new_row = col + dx, row + dy
    if not (0 <= row < len(maze) and 0 <= col < len(maze[row])):
        return False
    if not (0 <= new_row < len(maze) and
            0 <= new_col < len(maze[new_row])):
        return False
    return not (maze[row][col] & WALL_BITS[facing])


def move_character(
    character: dict,
    maze: list[list[int]],
    maze_pos: int,
    scale: int,
    speed: int
) -> None:
    if (character["center_x"] == character["target_x"]
            and character["center_y"] == character["target_y"]):

        col = character["col"]
        row = character["row"]

        if open_passage(col, row, character["next_direction"], maze):
            character["direction"] = character["next_direction"]

        if open_passage(col, row, character["direction"], maze):
            dx, dy = MOVEMENTS[character["direction"]]

            character["col"] += dx
            character["row"] += dy

            character["target_x"] = (
                maze_pos + (character["col"] + 0.5) * scale
            )
            character["target_y"] = (
                maze_pos + (character["row"] + 0.5) * scale
            )

    for axis in ("x", "y"):
        center = character[f"center_{axis}"]
        target = character[f"target_{axis}"]

        if center < target:
            center = min(center + speed, target)
        elif center > target:
            center = max(center - speed, target)

        character[f"center_{axis}"] = center


def game_runnig(
    maze: list[list[int]],
    screen: pygame.Surface,
    screen_size: tuple[int, int],
    scale: int,
    pacman_speed: int,
    ghost_speed: int,
    format_clavier: str
) -> bool:
    width = len(maze[0]) * scale
    maze_pos = (screen_size[0] - width) // 2
    animation = [0, 1, 2, 1]
    animation_speed = 80

    pacman_radius = scale * 0.8 / 2
    if format_clavier == "zqsd":
        directions = {
            pygame.K_z: "U", pygame.K_s: "D",
            pygame.K_q: "L", pygame.K_d: "R"
        }
    elif format_clavier == "wasd":
        directions = {
            pygame.K_w: "U", pygame.K_s: "D",
            pygame.K_a: "L", pygame.K_d: "R"
        }
    elif format_clavier == "arrows":
        directions = {
            pygame.K_UP: "U", pygame.K_DOWN: "D",
            pygame.K_LEFT: "L", pygame.K_RIGHT: "R"
        }
    elif format_clavier == "dualzqsd":
        directions1 = {
            pygame.K_z: "U", pygame.K_s: "D",
            pygame.K_q: "L", pygame.K_d: "R",
        }
        directions2 = {
            pygame.K_UP: "U", pygame.K_DOWN: "D",
            pygame.K_LEFT: "L", pygame.K_RIGHT: "R",
        }
    elif format_clavier == "dualwasd":
        directions1 = {
            pygame.K_w: "U", pygame.K_s: "D",
            pygame.K_a: "L", pygame.K_d: "R",
        }
        directions2 = {
            pygame.K_UP: "U", pygame.K_DOWN: "D",
            pygame.K_LEFT: "L", pygame.K_RIGHT: "R",
        }

    def create_character(col, row, direction, maze_pos, scale):
        center_x = maze_pos + (col + 0.5) * scale
        center_y = maze_pos + (row + 0.5) * scale

        return {
            "col": col,
            "row": row,
            "direction": direction,
            "next_direction": direction,
            "center_x": center_x,
            "center_y": center_y,
            "target_x": center_x,
            "target_y": center_y
        }

    pacman = create_character(9, 9, "R", maze_pos, scale)
    ghost = create_character(0, 0, "L", maze_pos, scale)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_p, pygame.K_ESCAPE):
                    running = False

                elif (
                    format_clavier == "dualwasd"
                    or format_clavier == "dualzqsd"
                ):
                    if event.key in directions1:
                        pacman["next_direction"] = directions1[event.key]

                    elif event.key in directions2:
                        ghost["next_direction"] = directions2[event.key]

                elif event.key in directions:
                    pacman["next_direction"] = directions[event.key]

        if not running:
            break

        move_character(
            pacman, maze, maze_pos, scale, pacman_speed
        )
        screen.fill(colors.BLACK)
        show_wall(screen, maze_pos, scale, maze)

        PacMan_Movements(
            screen,
            animation,
            animation_speed,
            pos=(
                round(pacman["center_x"] - pacman_radius),
                round(pacman["center_y"] - pacman_radius),
                pacman["direction"]
            ),
            scale=scale * 0.8
        )

        if format_clavier == "dualwasd" or format_clavier == "dualzqsd":
            test_Blue_Ghost_animation(
                screen,
                pos=(
                    round(ghost["center_x"] - pacman_radius),
                    round(ghost["center_y"] - pacman_radius),
                    ghost["direction"]
                ),
                animation=animation,
                animation_speed=animation_speed,
                scale=scale * 0.8
            )
        pygame.display.flip()
        clock.tick(60)
    return True  # Retour au menu (P ou Échap)
