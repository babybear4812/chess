# Handling user input and displaying the board (state of the game, i.e. State class)
import pygame as pg
import engine

pg.init()  # initializing pygame
WIDTH = HEIGHT = 400  # pygame screen size display
SQ_SIZE = WIDTH // 8  # each square size of the 8x8 board
MAX_FPS = 15  # for animations only
PIECES = {}  # global dictionary giving access to all piece images


def import_pieces():
    """Only used once to import piece images at the start of the game. """
    pieces = ["wR", "wN", "wB", "wQ", "wK",
              "wP", "bR", "bN", "bB", "bQ", "bK", "bP"]
    for piece in pieces:
        PIECES[piece] = pg.transform.scale(pg.image.load(
            "images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def main():
    """Main function that controls screen display, imports pieces, and runs the clock. """
    screen = pg.display.set_mode((WIDTH, HEIGHT))  # initialize screen

    clock = pg.time.Clock()  # create Clock object to track time
    state = engine.State()  # instance of State class from engine.py

    import_pieces()  # import pieces into global PIECES dictionary

    playing = True
    sqClicked = [None, None]  # will store [r, c] of square clicked
    prevClicks = []  # will store click history in the form [startSq, endSq]

    # game event queue
    while playing:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                playing = False  # when game is quit, stop drawing state.
            elif event.type == pg.MOUSEBUTTONDOWN:
                # we can change this event to be a drag instead of a click
                location = pg.mouse.get_pos()  # [x, y]
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE

                # check if user is double clicking on a square so we can clear original click
                if sqClicked[0] == row and sqClicked[1] == col:
                    sqClicked = []  # deselect original click
                    prevClicks = []  # clear all other clicks
                else:
                    # stores first click, or overwrites prev click
                    sqClicked = [row, col]
                    # stores both first and second click
                    prevClicks.append(sqClicked)

                # check if they have decided to make a move
                if len(prevClicks) == 2:
                    move = engine.Move(
                        prevClicks[0], prevClicks[1], state.board)
                    print(move.getChessNotation())
                    state.makeMove(move)
                    sqClicked = [None, None]  # reset clicks
                    prevClicks = []  # reset clicks
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_z:
                    state.undoMove()

        draw_state(screen, state)
        clock.tick(MAX_FPS)
        pg.display.flip()  # updates the full display Surface


def draw_state(screen, state):
    """Fills board with squares and pieces every time it is called. """
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


if __name__ == "__main__":
    """
    This will allow main.py to run only when we're running this module,
    not when it's imported from another one.
    """
    main()
