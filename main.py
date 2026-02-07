import pygame
import PIL
from pathlib import Path

# Config
BASE_WIDTH = 320
BASE_HEIGHT = 180
WINDOW_SCALE = 2
FPS = 120

BASE_DIR = Path(__file__).resolve().parent
ASSETS = BASE_DIR / "assets"

def load_image(*parts: str) -> pygame.Surface:
    """Load an image from assets/... with per-pixel transparency."""
    path = ASSETS.joinpath(*parts)
    return pygame.image.load(str(path)).convert_alpha()

def blit_scale_nearest(dst: pygame.Surface, src: pygame.Surface):
    """Scale the base (low-res) surface to the window using crisp nearest-neighbor scaling."""
    scaled = pygame.transform.scale(src, dst.get_size())
    dst.blit(scaled, (0, 0))

def main():
    pygame.init()
    window = pygame.display.set_mode((BASE_WIDTH * WINDOW_SCALE, BASE_HEIGHT * WINDOW_SCALE))
    pygame.display.set_caption("Aura Surge")
    clock = pygame.time.Clock()

    # Low-res render target
    base = pygame.Surface((BASE_WIDTH, BASE_HEIGHT), pygame.SRCALPHA)

    # -------------------------
    # Load separated assets
    # -------------------------
    bg = load_image("bg", "space_320x180.png")
    highway = load_image("highway", "highway_128x180.png")

    # UI (only if you have them already; comment out if not)
    combo_label = load_image("ui", "combo.png")
    score_box = load_image("ui", "score_box_64x16.png")

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # -------------------------
        # Draw scene (320x180)
        # -------------------------
        base.fill((10, 10, 18))  # fallback
        base.blit(bg, (0, 0))

        # center the highway (128x180) on the 320-wide screen
        highway_x = (BASE_WIDTH - highway.get_width()) // 2
        HIGHWAY_Y = 20  # tweak between 16–32 until it feels right
        base.blit(highway, (highway_x, HIGHWAY_Y))

        # UI example placement (optional)
        base.blit(combo_label, (8, 8))
        base.blit(score_box, (BASE_WIDTH - score_box.get_width() - 8, 8))

        # -------------------------
        # Present
        # -------------------------
        window.fill((0, 0, 0))
        blit_scale_nearest(window, base)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
