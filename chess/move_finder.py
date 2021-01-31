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
# recursive call depth
MAX_DEPTH = 3


def get_board_score(state):
    """
    Gets the total material score on the board.
    A positive score indicates a favorable number of pieces for white.
    A negative score indicates a favorable number of pieces for black.
    """
    board = state.board
    totalScore = 0

    # if there's a checkmate or stalemate, don't bother looking through the rest of the board
    if state.checkmate:
        if state.whiteToMove:
            # black wins
            return -CHECKMATE
        else:
            # white wins
            return CHECKMATE
    elif state.stalemate:
        return STALEMATE

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


def get_best_move_min_max(state, validMoves):
    """Helper method that will make the first recursive call. """
    global nextMove
    nextMove = None
    # shuffles possible moves so bot doesn't repeat the same move
    # when presented with multiple best moves of equal point outcome
    random.shuffle(validMoves)
    get_move_min_max(state, validMoves, 0)
    print(nextMove)
    return nextMove


def get_move_min_max(state, validMoves, depth):
    global nextMove
    if depth == MAX_DEPTH:
        return get_board_score(state)

    if state.whiteToMove:
        maxScore = float('-inf')
        for move in validMoves:
            state.make_move(move)
            newValidMoves = state.get_valid_moves()
            score = get_move_min_max(
                state, newValidMoves, depth + 1)
            if score > maxScore:
                maxScore = score
                if depth == 0:
                    nextMove = move

            state.undo_move()
        return maxScore

    else:
        minScore = float('inf')
        for move in validMoves:
            state.make_move(move)
            newValidMoves = state.get_valid_moves()
            score = get_move_min_max(
                state, newValidMoves, depth + 1)
            if score < minScore:
                minScore = score
                if depth == 0:
                    nextMove = move

            state.undo_move()
        return minScore
