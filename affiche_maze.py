from mazegenerator import MazeGenerator  # type: ignore[import-untyped]
import pygame
import colors


def show_wall(
    screen: pygame.Surface,
    pos: int,
    cell_size: int
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


def PacGum(pos_x: int, pos_y: int, scale: int) -> None:
    pacgum = pygame.image.load("assets/PacGum.png").convert_alpha()

    # Redimensionner à 20 × 20 pixels
    pacgum = pygame.transform.scale(pacgum, (scale // 1.5, scale // 1.5))

    # Afficher l'image aux coordonnées (100, 80)
    screen.blit(pacgum, (pos_x, pos_y))


def PacGum_Super(pos_x: int, pos_y: int, scale: int) -> None:
    pacgum_super = pygame.image.load("assets/Super_PacGum.png").convert_alpha()

    # Redimensionner à 20 × 20 pixels
    pacgum_super = pygame.transform.scale(
        pacgum_super,
        (scale // 1.2, scale // 1.2)
    )

    # Afficher l'image aux coordonnées (100, 80)
    screen.blit(pacgum_super, (pos_x, pos_y))


def test_PacMan_animation(
    animation: list[int],
    animation_speed: int,
    pos: tuple[int, int, str],
    scale: float,
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
    pos_x: int,
    pos_y: int,
    direction: str,
) -> None:
    images_Blue_Ghost = [
        pygame.transform.scale(
            pygame.image.load("assets/Blue_Ghost_U.png").convert_alpha(),
            (pos_y, pos_y),
        ),
        pygame.transform.scale(
            pygame.image.load("assets/Blue_Ghost_D.png").convert_alpha(),
            (pos_y, pos_y),
        ),
        pygame.transform.scale(
            pygame.image.load("assets/Blue_Ghost_L.png").convert_alpha(),
            (pos_y, pos_y),
        ),
        pygame.transform.scale(
            pygame.image.load("assets/Blue_Ghost_R.png").convert_alpha(),
            (pos_y, pos_y),
        ),
    ]
    if direction == "U":
        screen.blit(images_Blue_Ghost[0], (pos_x, pos_y))
    elif direction == "D":
        screen.blit(images_Blue_Ghost[1], (pos_x, pos_y))
    elif direction == "L":
        screen.blit(images_Blue_Ghost[2], (pos_x, pos_y))
    elif direction == "R":
        screen.blit(images_Blue_Ghost[3], (pos_x, pos_y))


def test_Red_Ghost_animation(
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
    movements = {
        "U": (0, -1),
        "D": (0, 1),
        "L": (-1, 0),
        "R": (1, 0)
    }

    if direction not in movements:
        return False

    dx, dy = movements[direction]

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


def game_runnig(
    maze: list[list[int]],
    screen: pygame.Surface,
    screen_size: tuple[int, int],
    scale: int,
    pacman_speed: int,
    ghost_speed: int
) -> None:
    # Définir la taille des cellules du labyrinthe
    width = len(maze[0]) * scale
    '''height = len(maze) * scale'''

    # Calculer la position du labyrinthe pour le centrer à l'écran
    maze_pos = (screen_size[0] - width) // 2
    '''maze_pos_y = ((screen_size[1] - height) // 2) - 200'''

    # Ordre des images
    animation = [0, 1, 2, 1]

    # Durée d'une image en millisecondes
    animation_speed = 80

    Pac_Man_Place = (505, 505, "R")  # Position initiale de Pac-Man

    pacman_radius = scale * 0.8 / 2

    direction = "R"
    next_direction = "R"

    directions = {
        pygame.K_w: "U",
        pygame.K_s: "D",
        pygame.K_a: "L",
        pygame.K_d: "R"
    }

    movements = {
        "U": (0, -1),
        "D": (0, 1),
        "L": (-1, 0),
        "R": (1, 0)
    }

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key in directions:
                    next_direction = directions[event.key]

                elif event.key == pygame.K_p:
                    running = False

        screen.fill(colors.BLACK)

        # Centre de Pac-Man
        center_x = Pac_Man_Place[0] + pacman_radius
        center_y = Pac_Man_Place[1] + pacman_radius

        # Vérifier si le virage demandé est possible
        if can_move(
            maze,
            center_x,
            center_y,
            next_direction,
            pacman_speed,
            scale,
            maze_pos,
            pacman_radius,
            margin=2
        ):
            direction = next_direction

        # Déplacement automatique
        if can_move(
            maze,
            center_x,
            center_y,
            direction,
            pacman_speed,
            scale,
            maze_pos,
            pacman_radius,
            margin=2
        ):
            dx, dy = movements[direction]

            Pac_Man_Place = (
                Pac_Man_Place[0] + dx * pacman_speed,
                Pac_Man_Place[1] + dy * pacman_speed,
                direction
            )
        if keys[pygame.K_ESCAPE]:
                running = False

        show_wall(screen, maze_pos, scale)

        test_PacMan_animation(
            animation, animation_speed,
            pos=Pac_Man_Place,
            scale=scale * 0.8
        )

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    maze_generator = MazeGenerator(
        size=(20, 20),
        seed=42,
        perfect=False
    )
    maze = maze_generator.maze
    for row in maze:
        print(row)

    pygame.init()
    screen_size = (1080, 1200)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Pac Man")

    game_runnig(
        maze,
        screen,
        screen_size,
        scale=40,
        pacman_speed=2,
        ghost_speed=3
    )
