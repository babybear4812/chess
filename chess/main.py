# Handling user input and displaying the board (state of the game, i.e. State class)
import pygame as pg
import engine

pg.init()  # initializing pygame
WIDTH = HEIGHT = 400  # pygame screen size display
SQ_SIZE = WIDTH // 8  # each square size of the 8x8 board
MAX_FPS = 15  # for animations only
PIECES = {}  # global dictionary giving access to all piece images

"""Only used once to import piece images at the start of the game"""


def import_pieces():
    pieces = ["wR", "wKn", "wB", "wQ", "wK",
              "wP", "bR", "bKn", "bB", "bQ", "bK", "bP"]
    for piece in pieces:
        PIECES[piece] = pg.transform.scale(pg.image.load(
            "images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


"""Main function that controls screen display, imports pieces, and runs the clock"""


def main():
    screen = pg.display.set_mode((WIDTH, HEIGHT))  # initialize screen

    clock = pg.time.Clock()  # create Clock object to track time
    state = engine.State()  # instance of State class from engine.py

    import_pieces()  # import pieces into global PIECES dictionary

    # listen for pygame QUIT event; when game is quit, stop drawing state.
    playing = True
    while playing:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                playing = False
        drawState(screen, state)
        clock.tick(MAX_FPS)
        pg.display.flip()  # updates the full display Surface


"""Fills board with squares and pieces every time it is called"""


def drawState(screen, state):
    board = state.board

    # walk through entire board
    for i in range(8):
        for j in range(8):
            # alternate between white and black squares
            color = pg.Color(235, 235, 208) if (
                i + j) % 2 == 0 else pg.Color(119, 148, 85)

            # fill square colour accordingly
            pg.draw.rect(screen, color, pg.Rect(
                j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))

            # if there should be a piece on the board, grab it and display it
            piece = board[i][j]
            if piece:
                screen.blit(PIECES[piece], pg.Rect(
                    j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))


# this will allow main.py to run only when we're running this module, not when it's imported from another one
if __name__ == "__main__":
    main()
