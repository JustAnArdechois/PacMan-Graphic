from mazegenerator import MazeGenerator  # type: ignore[import-untyped]
import pygame
import colors
from game import game_runnig


def main_menu(screen: pygame.Surface) -> bool:
    """Renvoie True pour jouer, False pour quitter."""
    clock = pygame.time.Clock()
    width, height = screen.get_size()
    title_font = pygame.font.Font(None, 110)
    button_font = pygame.font.Font(None, 54)
    hint_font = pygame.font.Font(None, 28)

    button_width, button_height = 300, 75
    play_button = pygame.Rect(0, 0, button_width, button_height)
    quit_button = pygame.Rect(0, 0, button_width, button_height)
    play_button.center = (width // 2, height // 2)
    quit_button.center = (width // 2, height // 2 + 105)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button.collidepoint(event.pos):
                    return True
                if quit_button.collidepoint(event.pos):
                    return False

        screen.fill(colors.BLACK)
        title = title_font.render("PAC-MAN", True, (255, 220, 0))
        screen.blit(title, title.get_rect(center=(width // 2, height // 3)))

        for rect, label in ((play_button, "JOUER"), (quit_button, "QUITTER")):
            hovered = rect.collidepoint(mouse_pos)
            background = (45, 90, 220) if hovered else (20, 45, 135)
            pygame.draw.rect(screen, background, rect, border_radius=14)
            pygame.draw.rect(screen, (80, 150, 255), rect, 3, border_radius=14)
            text = button_font.render(label, True, (255, 255, 255))
            screen.blit(text, text.get_rect(center=rect.center))

        hint = hint_font.render("Clique sur un bouton", True, (160, 160, 160))
        screen.blit(
            hint, hint.get_rect(center=(width // 2, height // 2 + 200))
        )
        pygame.display.flip()
        clock.tick(60)


def main() -> None:
    pygame.init()
    screen_size = (1080, 1200)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Pac Man")

    maze = MazeGenerator(
        size=(20, 20),
        seed=42,
        perfect=False
    ).maze

    while True:
        if not main_menu(screen):
            break
        should_return_to_menu = game_runnig(
            maze,
            screen,
            screen_size,
            scale=40,
            pacman_speed=2,
            ghost_speed=3,
            format_clavier="dualzqsd"
        )
        if not should_return_to_menu:
            break

    pygame.quit()


if __name__ == "__main__":
    main()
