'''
A note on the minimax algorithm:
- we are going to calculate the strength of our position based on the score on the board at any given moment.
- If we want to look multiple moves ahead, we will simulate multiple moves and pick the optimal one.
- However, by doing that blindly, we will be using the moves which would result in one player picking optimally,
while the other player picks in the worst possible way.
- To solve this problem, we will be selecting optimal moves (e.g. maximizing white score) while our
opponent also optimizes their moves (e.g. minimizing black score) because high score is great for white
and low score is great for black.

'''
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
    opponentMinMaxScore = float('inf')
    turnMultiplier = 1 if state.whiteToMove else -1

    bestMove = None
    random.shuffle(validMoves)

    for playerMove in validMoves:
        state.make_move(playerMove)
        opponentMoves = state.get_valid_moves()
        opponentMaxScore = float('-inf')

        for opponentMove in opponentMoves:
            state.make_move(opponentMove)

            if state.checkmate:
                score = -turnMultiplier * CHECKMATE
            elif state.stalemate:
                score = STALEMATE
            else:
                # if the board score is negative, that is good for black.
                # so we will multiply it by -1 to make it positive in order
                # to compare it to the current opponentMinMaxScore they could get
                score = -turnMultiplier * get_board_score(state.board)

            if score > opponentMaxScore:
                opponentMaxScore = score

            state.undo_move()

        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestMove = playerMove

        state.undo_move()

    return bestMove
