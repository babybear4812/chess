# the engine will store the State class which will contain the board, turn, and move log
import numpy as np


class State():
    def __init__(self):
        self.board = np.array([
            np.array(["bR", "bKn", "bB", "bQ", "bK", "bB", "bKn", "bR"]),
            np.array(["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"]),
            np.array(["", "", "", "", "", "", "", "", ]),
            np.array(["", "", "", "", "", "", "", "", ]),
            np.array(["", "", "", "", "", "", "", "", ]),
            np.array(["", "", "", "", "", "", "", "", ]),
            np.array(["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"]),
            np.array(["wR", "wKn", "wB", "wQ", "wK", "wB", "wKn", "wR"]),
        ])  # using numpy array for improved efficency when running AI bot
        self.whiteMove = True
        self.log = []  # move log
