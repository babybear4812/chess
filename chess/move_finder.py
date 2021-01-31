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

# number of points per piece type
PIECE_POINTS = {
    "P": 1,
    "N": 3,
    "B": 3,
    "R": 5,
    "Q": 9,
    "K": 0
}

# setting checkmate to a very high value indicating extreme importance
CHECKMATE = 1000
# setting stalemate to a netural 0 point score, rendering it desirable
# if losing, and not desirable if winning
STALEMATE = 0


def get_board_score(board):
    """
    Gets the total material score on the board.
    A positive score indicates a favorable number of pieces for white.
    A negative score indicates a favorable number of pieces for black.
    """
    totalScore = 0
    for i in range(8):
        for j in range(8):
            # if there is a piece on the board ...
            if board[i][j]:
                points = PIECE_POINTS[board[i][j][1]]
                # ... update the total score with it
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
    # shuffles possible moves so bot doesn't repeat the same move
    # when presented with multiple best moves of equal point outcome
    random.shuffle(validMoves)

    for playerMove in validMoves:
        state.make_move(playerMove)
        opponentMoves = state.get_valid_moves()
        if state.checkmate:
            opponentMaxScore = float('-inf')
        elif state.stalemate:
            opponentMaxScore = 0
        else:
            opponentMaxScore = float('-inf')

            for opponentMove in opponentMoves:
                state.make_move(opponentMove)
                state.get_valid_moves()

                if state.checkmate:
                    score = CHECKMATE
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
