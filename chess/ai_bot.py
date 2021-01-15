import random


class Bot():
    """Controls the decision making of the bot player. """

    def __init__(self):
        self.pieceValues = {
            "wP": 10,
            "bP": -10,
            "wN": 30,
            "bN": -30,
            "wB": 30,
            "bB": -30,
            "wR": 50,
            "bR": -50,
            "wQ": 90,
            "bQ": -90,
            "wK": 900,
            "bK": -900
        }

    def bot_move(self, state):
        """
        Simulates all the valid moves for the bot, and calls the appropriate
        helper functions to decide which move to play.
        """
        board = state.board

        validMoves = state.get_valid_moves()
        minPoints = float('inf')
        bestMoves = []

        # walk through every possible valid move
        for move in validMoves:
            state.make_move(move)  # simulate making the move
            # get number of points after that move is made
            movePoints = self.get_board_value(board)

            if movePoints < minPoints:  # found a new best move
                minPoints = movePoints
                bestMoves = [move]
            elif movePoints == minPoints:  # found an equally best move
                bestMoves.append(move)

            state.undo_move()  # undo the simulated move

        # if there are multiple best moves, pick a random move to make
        randomNumber = random.randint(0, len(bestMoves) - 1)
        bestMove = bestMoves[randomNumber]
        state.make_move(bestMove)

    def get_board_value(self, board):
        """
        Calculates the value of the pieces on the board in order to decide which 
        move is best to make.
        """
        totalPoints = 0
        for i in range(8):
            for j in range(8):
                if board[i][j]:
                    totalPoints += self.pieceValues[board[i][j]]
        return totalPoints
