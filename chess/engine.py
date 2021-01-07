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
        """Takes a move and executes it (not working with castling, en passant, promotion). """

        # move piece from starting position to ending position
        self.board[move.startRow][move.startCol] = ""
        self.board[move.endRow][move.endCol] = move.pieceMoved

        # store ply in log and swap turns
        self.log.append(move)
        self.whiteToMove = not self.whiteToMove

    def undoMove(self):
        """Takes the last move and undoes it. """
        if self.log:
            lastMove = self.log.pop()  # remove last move from log

            # clear ending position and put piece back on starting position
            self.board[lastMove.endRow][lastMove.endCol] = lastMove.pieceCaptured
            self.board[lastMove.startRow][lastMove.startCol] = lastMove.pieceMoved

            self.whiteToMove = not self.whiteToMove  # undo turn change

    def getPawnMoves(i, j, moves):
        pass

    def getRookMoves(i, j, moves):
        pass

    def getKnightMoves(i, j, moves):
        pass

    def getBishopMoves(i, j, moves):
        pass

    def getQueenMoves(i, j, moves):
        pass

    def getKingMoves(i, j, moves):
        pass

    def getValidMoves(self):
        """ Generates valid moves only. """
        return self.getAllPossibleMoves()  # temporary

    def getAllPossibleMoves(self):
        """Generates all possible moves. """
        possibleMoves = []

        for i in range(8):
            for j in range(8):
                if self.board[i][j]:
                    if (self.board[i][j][0] == "w" and self.whiteToMove) or \
                            (self.board[i][j][0] == "b" and not self.whiteToMove):
                        piece = self.board[i][j][1]:
                        if piece == "P":
                            self.getPawnMoves(i, j, moves)
                        elif piece == "R":
                            self.getRookMoves(i, j, moves)
                        elif piece == "N":
                            self.getKnightMoves(i, j, moves)
                        elif piece == "B":
                            self.getBishopMoves(i, j, moves)
                        elif piece == "Q":
                            self.getQueenMoves(i, j, moves)
                        elif piece == "K":
                            self.getKingMoves(i, j, moves)


class Move():
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
        """Converting array indices to proper chess notation. """
        start = self.colToFile[self.startCol] + self.rowToRank[self.startRow]
        end = self.colToFile[self.endCol] + self.rowToRank[self.endRow]
        return start + "-" + end
