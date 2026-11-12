from mazegenerator import MazeGenerator
import pygame


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
                    (0, 0, 255),
                    (px, py),
                    (px + cell_size, py),
                    2
                )

            if cell & 2:  # Est
                pygame.draw.line(
                    screen,
                    (0, 0, 255),
                    (px + cell_size, py),
                    (px + cell_size, py + cell_size),
                    2
                )

            if cell & 4:  # Sud
                pygame.draw.line(
                    screen,
                    (0, 0, 255),
                    (px, py + cell_size),
                    (px + cell_size, py + cell_size),
                    2
                )

            if cell & 8:  # Ouest
                pygame.draw.line(
                    screen,
                    (0, 0, 255),
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
    pacgum_super = pygame.transform.scale(pacgum_super, (scale // 1.2, scale // 1.2))

    # Afficher l'image aux coordonnées (100, 80)
    screen.blit(pacgum_super, (pos_x, pos_y))


def test_PacMan_animation(
    animation: list[int],
    animation_speed: int,
    pos_x: int,
    pos_y: int,
) -> None:
    images_PacMan = [
        pygame.transform.scale(
            pygame.image.load("assets/PacMan_1.png").convert_alpha(), (pos_y, pos_y)
        ),
        pygame.transform.scale(
            pygame.image.load("assets/PacMan_2.png").convert_alpha(), (pos_y, pos_y)
        ),
        pygame.transform.scale(
            pygame.image.load("assets/PacMan_3.png").convert_alpha(), (pos_y, pos_y)
        ),
    ]
    frame = (
        pygame.time.get_ticks() // animation_speed
    ) % len(animation)

    image_index = animation[frame]

    screen.blit(images_PacMan[image_index], (pos_x, pos_y))


def test_Blue_Ghost_animation(
    pos_x: int,
    pos_y: int,
    direction: str
) -> None:
    images_Blue_Ghost = [
        pygame.transform.scale(
            pygame.image.load("assets/Blue_Ghost_U.png").convert_alpha(), (pos_y, pos_y)
        ),
        pygame.transform.scale(
            pygame.image.load("assets/Blue_Ghost_D.png").convert_alpha(), (pos_y, pos_y)
        ),
        pygame.transform.scale(
            pygame.image.load("assets/Blue_Ghost_L.png").convert_alpha(), (pos_y, pos_y)
        ),
        pygame.transform.scale(
            pygame.image.load("assets/Blue_Ghost_R.png").convert_alpha(), (pos_y, pos_y)
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
    direction: str
) -> None:
    images_Red_Ghost = [
        pygame.transform.scale(
            pygame.image.load("assets/Red_Ghost_U.png").convert_alpha(), (pos_y, pos_y)
        ),
        pygame.transform.scale(
            pygame.image.load("assets/Red_Ghost_D.png").convert_alpha(), (pos_y, pos_y)
        ),
        pygame.transform.scale(
            pygame.image.load("assets/Red_Ghost_L.png").convert_alpha(), (pos_y, pos_y)
        ),
        pygame.transform.scale(
            pygame.image.load("assets/Red_Ghost_R.png").convert_alpha(), (pos_y, pos_y)
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
    direction: str
) -> None:
    images_Orange_Ghost = [
        pygame.transform.scale(
            pygame.image.load("assets/Orange_Ghost_U.png").convert_alpha(), (pos_y, pos_y)
        ),
        pygame.transform.scale(
            pygame.image.load("assets/Orange_Ghost_D.png").convert_alpha(), (pos_y, pos_y)
        ),
        pygame.transform.scale(
            pygame.image.load("assets/Orange_Ghost_L.png").convert_alpha(), (pos_y, pos_y)
        ),
        pygame.transform.scale(
            pygame.image.load("assets/Orange_Ghost_R.png").convert_alpha(), (pos_y, pos_y)
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
            pygame.image.load("assets/Pink_Ghost_U.png").convert_alpha(), (pos_y, pos_y)
        ),
        pygame.transform.scale(
            pygame.image.load("assets/Pink_Ghost_D.png").convert_alpha(), (pos_y, pos_y)
        ),
        pygame.transform.scale(
            pygame.image.load("assets/Pink_Ghost_L.png").convert_alpha(), (pos_y, pos_y)
        ),
        pygame.transform.scale(
            pygame.image.load("assets/Pink_Ghost_R.png").convert_alpha(), (pos_y, pos_y)
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


def affiche_maze(
    maze: list[list[int]],
    screen: pygame.Surface,
    screen_size: tuple[int, int],
    scale: int
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
    animation_speed = 150

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((100, 100, 100))

        show_wall(screen, maze_pos, scale)

        test_PacMan_animation(animation, animation_speed, scale * 2, scale)

        test_Red_Ghost_animation(scale * 5, scale, "L")
        test_Blue_Ghost_animation(scale * 6, scale, "D")
        test_Orange_Ghost_animation(scale * 7, scale, "U")
        test_Pink_Ghost_animation(scale * 8, scale, "D")

        for i in range(5):
            PacGum((scale * i + scale * 5) + i * 20, 0, scale)

        PacGum_Super(scale * 1, scale, scale)

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

    affiche_maze(maze, screen, screen_size, scale=50)
