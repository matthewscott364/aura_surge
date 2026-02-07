import pygame
from pathlib import Path

pygame.init()

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
OUT_DIR = ASSETS_DIR / "exported"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SHEET_PATH = ASSETS_DIR / "sheet.png"

WINDOW_SCALE = 0.5

def main():
    # Load image without conversion first
    sheet = pygame.image.load(r"C:\Users\matth\OneDrive\Desktop\DA\Personal Projects\Applications\aura_surge\assets\sheet.png")
    sw, sh = sheet.get_size()

    # Set video mode first, then convert image
    window = pygame.display.set_mode((sw * WINDOW_SCALE, sh * WINDOW_SCALE))
    sheet = sheet.convert_alpha()
    pygame.display.set_caption("Aura Surge Sprite Slicer")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("None", 20)

    selecting = False
    start = (0, 0)
    end = (0, 0)

    # Quick-Save slots (press these to save selections)
    
    slots = {
        pygame.K_1: "bg_space_320_180.png",
        pygame.K_2: "highway_128x180.png",
        pygame.K_3: "note_green_16.png",
        pygame.K_4: "hit_flash_24.png",
        pygame.K_5: "ui_score_box_64x16.png",
    }

    def to_sheet_coords(mx, my):
        return mx // WINDOW_SCALE, my // WINDOW_SCALE
    
    def rect_from_points(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        left = min(x1, x2)
        top = min(y1, y2)
        w = abs(x1 - x2)
        h = abs(y1 - y2)
        return pygame.Rect(left, top, w, h)
    
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                # Save selection to a preset file name
                if event.key in slots:
                    r = rect_from_points(start, end)
                    if r.w > 0 and r.h > 0:
                        crop = sheet.subsurface(r).copy()
                        out_path = OUT_DIR / slots[event.key]
                        pygame.image.save(crop, out_path)
                        print(f"SAVED: {out_path.name} RECT: (x={r.x}, y={r.y}, w={r.w}, h={r.h})")

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                selecting = True
                start = to_sheet_coords(*event.pos)
                end = start

            if event.type == pygame.MOUSEMOTION and selecting:
                end = to_sheet_coords(*event.pos)

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                selecting = False
                end = to_sheet_coords(*event.pos)

        window.fill((0, 0, 0))
        # Draw the sprite sheet scaled up
        scaled_sheet = pygame.transform.scale(sheet, (sw * WINDOW_SCALE, sh * WINDOW_SCALE))
        window.blit(scaled_sheet, (0, 0))

        # Draw selection rect overlay
        r = rect_from_points(start, end)
        rr = pygame.Rect(r.x * WINDOW_SCALE, r.y * WINDOW_SCALE, r.w * WINDOW_SCALE, r.h * WINDOW_SCALE)
        pygame.draw.rect(window, (255, 255, 255), rr, 2)

        #help text
        txt = ["Drag-select. Press:",
               "1=BG, 2=Highway, 3=Note, 4=Hit Flash, 5=Score Box"
               "ESC quits. Saved images go in the assets/exported/"
               ]
        y = 6
        for line in txt:
            surf = font.render(line, True, (255, 255, 255))
            window.blit(surf, (6, y))
            y += 18

        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
        