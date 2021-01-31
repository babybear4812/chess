import random

piecePoints = {
    "P": 1,
    "N": 3,
    "B": 3,
    "R": 5,
    "Q": 9,
    "K": 0
}

CHECKMATE = 1000
STALEMATE = 0


def get_board_score(board):
    """Gets the total material score on the board. """
    totalScore = 0
    for i in range(8):
        for j in range(8):
            # if there is a piece on the board ...
            if board[i][j]:
                points = piecePoints[board[i][j][1]]
                # ...add it to the total score if it's white, otherwise subtract it
                totalScore = totalScore + \
                    points if board[i][j][0] == "w" else totalScore - points

    return totalScore


def get_random_move(validMoves):
    """Makes a random move. """
    return validMoves[random.randint(0, len(validMoves) - 1)]


def get_best_move(state, validMoves):
    """Makes the best move. """
    maxScore = float('-inf')
    turnMultiplier = 1 if state.whiteToMove else -1

    bestMove = None

    for playerMove in validMoves:
        state.make_move(playerMove)

        if state.checkmate:
            score = CHECKMATE
        elif state.stalemate:
            score = STALEMATE
        else:
            # if the board score is negative, that is good for black.
            # so we will multiply it by -1 to make it positive in order
            # to compare it to the current maxScore they could get
            score = turnMultiplier * get_board_score(state.board)

        if score > maxScore:
            maxScore = score
            bestMove = playerMove

        state.undo_move()

    return bestMove
