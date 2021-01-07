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

    def getPawnMoves(self, i, j, moves):
        """Generate all possible pawn moves. """
        if self.whiteToMove:  # white pawns
            if not self.board[i-1][j]:  # one square up
                moves.append(Move([i, j], [i-1, j], self.board))
                if i == 6 and not self.board[i-2][j]:  # two squares up
                    moves.append(Move([i, j], [i-2, j], self.board))

            # check capture up-left, then up-right
            if j > 0 and self.board[i-1][j-1] and self.board[i-1][j-1][0] == "b":
                moves.append(Move([i, j], [i-1, j-1], self.board))
            if j < 7 and self.board[i-1][j+1] and self.board[i-1][j+1][0] == "b":
                moves.append(Move([i, j], [i-1, j+1], self.board))

        else:  # black pawns
            if not self.board[i+1][j]:  # one square down
                moves.append(Move([i, j], [i+1, j], self.board))
                if i == 1 and not self.board[i+2][j]:  # two squares down
                    moves.append(Move([i, j], [i+2, j], self.board))

            # check capture down-left, then down-right
            if j > 0 and self.board[i+1][j-1] and self.board[i+1][j-1][0] == "w":
                moves.append(Move([i, j], [i+1, j-1], self.board))
            if j < 7 and self.board[i+1][j+1] and self.board[i+1][j+1][0] == "w":
                moves.append(Move([i, j], [i+1, j+1], self.board))

    def getRookMoves(self, i, j, moves):
        """Generate all possible rook moves. """
        # check up
        for r in range(i-1, -1, -1):
            if not self.board[r][j]:
                moves.append(Move([i, j], [r, j], self.board))
            else:
                if (self.board[r][j][0] == "w" and not self.whiteToMove) or \
                        (self.board[r][j][0] == "b" and self.whiteToMove):
                    moves.append(Move([i, j], [r, j], self.board))
                break

        # check right
        for c in range(j+1, 8, 1):
            if not self.board[i][c]:
                moves.append(Move([i, j], [i, c], self.board))
            else:
                if (self.board[i][c][0] == "w" and not self.whiteToMove) or \
                        (self.board[i][c][0] == "b" and self.whiteToMove):
                    moves.append(Move([i, j], [i, c], self.board))
                break

        # check down
        for r in range(i+1, 8, 1):
            if not self.board[r][j]:
                moves.append(Move([i, j], [r, j], self.board))
            else:
                if (self.board[r][j][0] == "w" and not self.whiteToMove) or \
                        (self.board[r][j][0] == "b" and self.whiteToMove):
                    moves.append(Move([i, j], [r, j], self.board))
                break

        # check left
        for c in range(j-1, -1, -1):
            if not self.board[i][c]:
                moves.append(Move([i, j], [i, c], self.board))
            else:
                if (self.board[i][c][0] == "w" and not self.whiteToMove) or \
                        (self.board[i][c][0] == "b" and self.whiteToMove):
                    moves.append(Move([i, j], [i, c], self.board))
                break

    def getKnightMoves(self, i, j, moves):
        """Generate all possible knight moves. """
        pass

    def getBishopMoves(self, i, j, moves):
        """Generate all possible bishop moves. """
        pass

    def getQueenMoves(self, i, j, moves):
        """Generate all possible queen moves. """
        pass

    def getKingMoves(self, i, j, moves):
        """Generate all possible king moves. """
        pass

    def getValidMoves(self):
        """ Generates valid moves only. """
        return self.getAllPossibleMoves()  # temporary

    def getAllPossibleMoves(self):
        """Generates all possible moves. """
        moves = []

        for i in range(8):
            for j in range(8):
                if self.board[i][j]:
                    if (self.board[i][j][0] == "w" and self.whiteToMove) or \
                            (self.board[i][j][0] == "b" and not self.whiteToMove):
                        piece = self.board[i][j][1]
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

        return moves


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

    def __eq__(self, other):
        """
        Overriding equal so we can compare two move objects.
        We need to compare our starting and ending position (x and y coordinates)
        to the starting and ending postion of the possible valid move we're comparing it to.
        Since they are both lists, we can not simply check equality regularly
        """
        if isinstance(other, Move):
            return self.startRow == other.startRow and \
                self.endRow == other.endRow and \
                self.startCol == other.startCol and \
                self.endCol == other.endCol
        return False  # not sure why this is here

    def getChessNotation(self):
        """Converting array indices to proper chess notation. """
        start = self.colToFile[self.startCol] + self.rowToRank[self.startRow]
        end = self.colToFile[self.endCol] + self.rowToRank[self.endRow]
        return start + "-" + end
