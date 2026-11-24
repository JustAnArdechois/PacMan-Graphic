"""Load, cache, animate and draw the original Pac-Man artwork."""
from pathlib import Path
import pygame  # type: ignore[import-not-found]


class SpriteManager:
    """Own sprite assets and cache their resized/rotated versions."""

    PACMAN_SEQUENCE = (0, 1, 2, 1)
    DIRECTIONS = ('U', 'D', 'L', 'R')
    GHOST_NAMES = ('red', 'pink', 'blue', 'orange')

    def __init__(self, root: Path | None = None) -> None:
        """Load source images once; root defaults to the project assets."""
        self.root = root or Path(__file__).resolve().parent.parent / 'assets'
        self.sources: dict[str, pygame.Surface] = {}
        self.cache: dict[tuple[str, int, str], pygame.Surface] = {}
        for frame in range(1, 4):
            self._load(f'pacman_{frame}', f'pacman/PacMan_{frame}.png')
        for name in self.GHOST_NAMES:
            for direction in self.DIRECTIONS:
                title = name.capitalize()
                self._load(f'{name}_{direction}',
                           f'ghosts/{name}/{title}_Ghost_{direction}.png')
        self._load('frightened_blue', 'ghosts/frightened/blue.png')
        self._load('frightened_white', 'ghosts/frightened/white.png')
        self._load('gum', 'pacgum/PacGum.png')
        self._load('super_gum', 'pacgum/Super_PacGum.png')

    def _load(self, key: str, relative: str) -> None:
        """Read one PNG with transparency and report missing assets."""
        path = self.root / relative
        try:
            self.sources[key] = pygame.image.load(str(path)).convert_alpha()
        except (pygame.error, OSError) as exc:
            raise RuntimeError(f'Cannot load sprite {path}: {exc}') from exc

    def _scaled(self, key: str, size: int,
                direction: str = 'R') -> pygame.Surface:
        """Return a cached image of a particular size and orientation."""
        size = max(1, int(size))
        cache_key = (key, size, direction)
        if cache_key not in self.cache:
            image = pygame.transform.scale(self.sources[key], (size, size))
            if key.startswith('pacman_'):
                if direction == 'U':
                    image = pygame.transform.rotate(image, 90)
                elif direction == 'D':
                    image = pygame.transform.rotate(image, -90)
                elif direction == 'L':
                    image = pygame.transform.flip(image, True, False)
            self.cache[cache_key] = image
        return self.cache[cache_key]

    def draw_pacman(self, screen: pygame.Surface, center: tuple[float, float],
                    size: int, direction: str, elapsed_ms: int) -> None:
        """Animate the three mouth frames and orient Pac-Man."""
        frame = self.PACMAN_SEQUENCE[(elapsed_ms // 110) %
                                     len(self.PACMAN_SEQUENCE)] + 1
        image = self._scaled(f'pacman_{frame}', size, direction)
        self._blit_center(screen, image, center)

    def draw_ghost(self, screen: pygame.Surface, center: tuple[float, float],
                   size: int, name: str, direction: str,
                   frightened_seconds: float, elapsed_ms: int) -> None:
        """Draw a directional ghost or its blue/white frightened state."""
        if frightened_seconds > 0:
            flash = (frightened_seconds <= 2.0 and
                     (elapsed_ms // 200) % 2 == 0)
            key = 'frightened_white' if flash else 'frightened_blue'
        else:
            key = f'{name}_{direction}'
        image = self._scaled(key, size)
        self._blit_center(screen, image, center)

    def draw_gum(self, screen: pygame.Surface, center: tuple[float, float],
                 cell_size: float, super_gum: bool = False) -> None:
        """Draw an ordinary or large pellet centered inside its cell."""
        key = 'super_gum' if super_gum else 'gum'
        ratio = 0.60 if super_gum else 0.30
        image = self._scaled(key, max(2, round(cell_size * ratio)))
        self._blit_center(screen, image, center)

    @staticmethod
    def _blit_center(screen: pygame.Surface, image: pygame.Surface,
                     center: tuple[float, float]) -> None:
        """Position an image by its center, rather than its top-left."""
        rect = image.get_rect(center=(round(center[0]), round(center[1])))
        screen.blit(image, rect)
