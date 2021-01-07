# the engine will store the State class which will contain the board, turn, and move log
import numpy as np


class State():
    def __init__(self):
        self.board = np.array([
            np.array(["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"]),
            np.array(["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"]),
            np.array(["", "", "", "", "", "", "", "", ]),
            np.array(["", "", "", "", "", "", "", "", ]),
            np.array(["", "", "", "", "", "", "", "", ]),
            np.array(["", "", "", "", "", "", "", "", ]),
            np.array(["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"]),
            np.array(["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]),
        ])  # using numpy array for improved efficency when running AI bot
        self.whiteToMove = True
        self.log = []  # move log

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = ""
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.log.append(move)
        self.whiteToMove = not self.whiteToMove  # swap turns


class Move():
    # rankToRow = {"1": 7, "2": 6, "3": 5,
    #              "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    # rowToRank = {val: key for key, val in rankToRow.items()}
    # fileToCol = {"a": 0, "b": 1, "c": 2,
    #              "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    # colToFile = {val: key for key, val in fileToCol.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.rankToRow = {"1": 7, "2": 6, "3": 5,
                          "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
        self.rowToRank = {val: key for key, val in self.rankToRow.items()}
        self.fileToCol = {"a": 0, "b": 1, "c": 2,
                          "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
        self.colToFile = {val: key for key, val in self.fileToCol.items()}

    def getChessNotation(self):
        start = self.colToFile[self.startCol] + self.rowToRank[self.startRow]
        end = self.colToFile[self.endCol] + self.rowToRank[self.endRow]
        return start + "-" + end
