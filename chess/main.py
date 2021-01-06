# Handling user input and displaying the board (state of the game, i.e. State class)
import pygame as pg
import engine

pg.init()  # initializing pygame
WIDTH = HEIGHT = 400
SQ_SIZE = WIDTH // 8
MAX_FPS = 15  # for animations only
IMAGES = {}


def import_images():
    """Only used once to import piece images at the start of the game"""
    pieces = ["wR", "wKn", "wB", "wQ", "wK",
              "wP", "bR", "bKn", "bB", "bQ", "bK", "bP"]
    for piece in pieces:
        IMAGES[piece] = pg.transform.scale(pg.image.load(
            "images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


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
        drawState(screen, state)
        clock.tick(MAX_FPS)
        pg.display.flip()


def drawState(screen, state):
    board = state.board

    def drawBoard():
        for i in range(8):
            for j in range(8):
                color = pg.Color(235, 235, 208) if (
                    i + j) % 2 == 0 else pg.Color(119, 148, 85)
                pg.draw.rect(screen, color, pg.Rect(
                    j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))

    def drawPieces():
        pass

    drawBoard()
    drawPieces()


# this will allow main.py to run only when we're running this module, not when it's imported from another one
if __name__ == "__main__":
    main()
