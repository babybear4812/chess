# Handling user input and displaying the board (state of the game, i.e. State class)
import pygame as pg
import engine

pg.init()  # initializing pygame
WIDTH = HEIGHT = 400
SQUARE_SIZE = WIDTH // 8
MAX_FPS = 15  # for animations only
IMAGES = {}


def import_images():
    """Only used once to import piece images at the start of the game"""
    pieces = ["wR", "wKn", "wB", "wQ", "wK",
              "wP", "bR", "bKn", "bB", "bQ", "bK", "bP"]
    for piece in pieces:
        IMAGES[piece] = pg.transform.scale(pg.image.load(
            "images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))


def main():
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    screen.fill(pg.Color("White"))

    clock = pg.time.Clock()
    state = engine.State()

    import_images()

    playing = True
    while playing:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                playing = False
        clock.tick(MAX_FPS)
        pg.display.flip()


# this will allow main.py to run only when we're running this module, not when it's imported from another one
if __name__ == "__main__":
    main()
