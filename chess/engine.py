# We will store game information here and determine valid moves + keep a move log
class State():
    def __init__(self):
        # can be more efficient if using numpy arrays for AI piece
        self.board = [
            ["bR", "bKn", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["", "", "", "", "", "", "", "", ],
            ["", "", "", "", "", "", "", "", ],
            ["", "", "", "", "", "", "", "", ],
            ["", "", "", "", "", "", "", "", ],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"]
            ["wR", "wKn", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ],
        self.whiteMove = True
        self.log = []
