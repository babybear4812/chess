# Handling user input and displaying the board (state of the game, i.e. State class)
import pygame as pg
import engine
import move_finder

pg.init()  # initializing pygame
WIDTH = HEIGHT = 800  # pygame screen size display
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


def draw_board(screen):
    """Draws the board with an alternating checkered pattern. """
    # walk through entire board
    for i in range(8):
        for j in range(8):
            # alternate between white and black squares
            color = pg.Color(235, 235, 208) if (
                i + j) % 2 == 0 else pg.Color(119, 148, 85)

            # fill square colour accordingly
            pg.draw.rect(screen, color, pg.Rect(
                j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def highlight_square(screen, state, validMoves, sqClicked):
    """Highlights the current square being clicked, if it has a valid piece on it. """
    # only highlight a square one on the screen is clicked...
    if sqClicked:
        i, j = sqClicked
        # ... and it's not empty...
        if state.board[i][j]:
            allyColor = "w" if state.whiteToMove else "b"
            # ... and it's that color's turn to move
            if state.board[i][j][0] == allyColor:
                # surface allows us to draw shapes onto the screen
                surface = pg.Surface((SQ_SIZE, SQ_SIZE))
                # transparency value, from 0 to 255
                surface.set_alpha(100)
                surface.fill(pg.Color('yellow'))

                # this will display the highlight on the screen
                screen.blit(surface, (j*SQ_SIZE, i*SQ_SIZE))


def draw_pieces(screen, board):
    """Draws the individual pieces on the board based on where they are in the state. """
    # if there should be a piece on the board, grab it and display it
    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece:
                screen.blit(PIECES[piece], pg.Rect(
                    j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_game_state(screen, state, validMoves, sqClicked):
    draw_board(screen)
    highlight_square(screen, state, validMoves, sqClicked)
    draw_pieces(screen, state.board)


def draw_text(screen, text):
    """Draws end of game message, including which player one or whether there was a stalemate. """
    # font type, size, bold, italics
    font = pg.font.SysFont("Arial", 32, True, False)
    textObject = font.render(text, 0, pg.Color("Black"))
    textLocation = pg.Rect(0, 0, WIDTH, HEIGHT).move(
        WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)


def main():
    """Main function that controls screen display, imports pieces, runs the clock, and contains the event listener. """
    screen = pg.display.set_mode((WIDTH, HEIGHT))  # initialize screen

    clock = pg.time.Clock()  # create Clock object to track time
    state = engine.State()  # instance of State class from engine.py
    validMoves = state.get_valid_moves()  # list containing all possible valid moves
    moveMade = False  # flag if move is made

    import_pieces()  # import pieces into global PIECES dictionary

    playing = True
    gameOver = False
    sqClicked = ()  # will store [r, c] of square clicked
    prevClicks = []  # will store click history in the form [startSq, endSq]

    whiteIsHuman = True  # True if human is playing white, else False if bot
    blackIsHuman = True  # True if human is playing black, else False if bot

    # game event queue
    while playing:
        isHumanTurn = (state.whiteToMove and whiteIsHuman) or (
            not state.whiteToMove and blackIsHuman)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                playing = False  # when game is quit, stop drawing state.
            # mouse listener
            elif event.type == pg.MOUSEBUTTONDOWN:
                if not gameOver and isHumanTurn:
                    # we can change this event to be a drag instead of a click
                    location = pg.mouse.get_pos()  # [x, y]
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE

                    # check if user is double clicking on a square so we can clear original click
                    if sqClicked == (row, col):
                        sqClicked = ()  # deselect original click
                        prevClicks = []  # clear all other clicks
                    else:
                        # stores first click, or overwrites prev click
                        sqClicked = (row, col)
                        # stores both first and second click
                        prevClicks.append(sqClicked)

                    # check if they have decided to make a move
                    if len(prevClicks) == 2:
                        move = engine.Move(
                            prevClicks[0], prevClicks[1], state.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                state.make_move(validMoves[i])
                                moveMade = True

                                # reset square clicked and previous clicks
                                sqClicked = ()
                                prevClicks = []
                        if not moveMade:
                            # otherwise, if it wasn't a valid move, we won't change the square clicked
                            # but we will clear the previous clicks and only keep the current click made
                            prevClicks = [sqClicked]
            # key listener
            elif event.type == pg.KEYDOWN:
                # key listener for undo move
                if event.key == pg.K_z:
                    state.undo_move()
                    # we will consider this a move made so that it will trigger validMove recalculation
                    moveMade = True
                    gameOver = False
                # key listener for restart game
                if event.key == pg.K_r:
                    state = engine.State()
                    validMoves = state.get_valid_moves()
                    sqClicked = ()
                    prevClicks = []
                    moveMade = False
                    gameOver = False

        # bot will make move only if it is not a human turn, and the game is not over
        if not gameOver and not isHumanTurn:
            botMove = move_finder.get_best_move(state, validMoves)
            if botMove:
                state.make_move(botMove)
            else:
                # if there is no best move, make a random move
                state.make_move(move_finder.get_random_move(validMoves))

            moveMade = True

        # if a move was made, generate new set of valid moves and reset flag
        if moveMade:
            validMoves = state.get_valid_moves()
            moveMade = False

        draw_game_state(screen, state, validMoves, sqClicked)

        # if the game is in checkmate or stalemate, we need to display the appropriate message
        if state.checkmate:
            gameOver = True
            if state.whiteToMove:
                draw_text(screen, "Black wins by checkmate!")
            else:
                draw_text(screen, "White wins by checkmate!")
        elif state.stalemate:
            gameOver = True
            draw_text(screen, "Stalemate!")

        clock.tick(MAX_FPS)
        pg.display.flip()  # updates the full display Surface


if __name__ == "__main__":
    """
    This will allow main.py to run only when we're running this module,
    not when it's imported from another one.
    """
    main()
