# the engine will store the State class which will contain the board, turn, and move log
import numpy as np


class State():
    def __init__(self):
        self.board = np.array([
            np.array(["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"]),
            np.array(["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"]),
            np.array(["", "", "", "", "", "", "", ""]),
            np.array(["", "", "", "", "", "", "", ""]),
            np.array(["", "", "", "", "", "", "", ""]),
            np.array(["", "", "", "", "", "", "", ""]),
            np.array(["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"]),
            np.array(["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]),
        ])  # using numpy array for improved efficency when running AI bot

        self.whiteToMove = True
        self.log = []  # move log

        self.whiteKingPosition = (7, 4)
        self.blackKingPosition = (0, 4)

        self.checkmate = False
        self.stalemate = False

        self.inCheck = False  # flag if current player is in check
        self.pins = []  # list of all current pins
        self.checks = []  # list of all current checks

    def makeMove(self, move):
        """Takes a move and executes it (not working with castling, en passant, promotion). """

        # move piece from starting position to ending position
        self.board[move.startRow][move.startCol] = ""
        self.board[move.endRow][move.endCol] = move.pieceMoved

        # store ply in log and swap turns
        self.log.append(move)
        self.whiteToMove = not self.whiteToMove

        # update king's location if needed
        if move.pieceMoved == "wK":
            self.whiteKingPosition = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingPosition = (move.endRow, move.endCol)

    def undoMove(self):
        """Takes the last move and undoes it. """
        if self.log:
            # remove last move from log, if one exists
            lastMove = self.log.pop()

            # clear ending position and put piece back on starting position
            self.board[lastMove.endRow][lastMove.endCol] = lastMove.pieceCaptured
            self.board[lastMove.startRow][lastMove.startCol] = lastMove.pieceMoved

            # undo turn change
            self.whiteToMove = not self.whiteToMove

            # update king's location if needed
            if lastMove.pieceMoved == "wK":
                self.whiteKingPosition = (lastMove.startRow, lastMove.startCol)
            elif lastMove.pieceMoved == "bK":
                self.blackKingPosition = (lastMove.startRow, lastMove.startCol)

    def getPawnMoves(self, i, j, moves):
        """Generate all possible pawn moves. """

        # We need to identify if the pawn is pinned.
        # as well, if it is, we need to make sure that we can only
        # move that piece in the direction of the pin
        isPinned = False
        pinDirection = ()  # direction the piece is being pinned from

        for idx, pin in enumerate(self.pins):
            if pin[0] == i and pin[1] == j:
                isPinned = True
                pinDirection = (pin[2], pin[3])
                self.pins.remove(self.pins[idx])  # NOT SURE WHY WE DO THIS YET
                break

        if self.whiteToMove:  # white pawns
            if not self.board[i-1][j]:  # one square up
                if not isPinned or pinDirection == (-1, 0):
                    # we can only make this move if the pawn isn't pinned,
                    # or if it's moving up in the direction of the pin (from a rook or queen)
                    moves.append(Move([i, j], [i-1, j], self.board))
                    if i == 6 and not self.board[i-2][j]:  # two squares up
                        moves.append(Move([i, j], [i-2, j], self.board))

            # check capture up-left, then up-right
            if j > 0 and self.board[i-1][j-1] and self.board[i-1][j-1][0] == "b":
                if not isPinned or pinDirection == (-1, -1):
                    # if the piece isn't pinned or it's pinned from the upper-left (from a bishop or queen)
                    moves.append(Move([i, j], [i-1, j-1], self.board))
            if j < 7 and self.board[i-1][j+1] and self.board[i-1][j+1][0] == "b":
                if not isPinned or pinDirection == (-1, 1):
                    moves.append(Move([i, j], [i-1, j+1], self.board))

        else:  # black pawns
            if not self.board[i+1][j]:  # one square down
                if not isPinned or pinDirection == (1, 0):
                    # notice direction of pin is reversed from white pawn logic above
                    moves.append(Move([i, j], [i+1, j], self.board))
                    if i == 1 and not self.board[i+2][j]:  # two squares down
                        moves.append(Move([i, j], [i+2, j], self.board))

            # check capture down-left, then down-right
            if j > 0 and self.board[i+1][j-1] and self.board[i+1][j-1][0] == "w":
                if not isPinned or pinDirection == (1, -1):
                    moves.append(Move([i, j], [i+1, j-1], self.board))
            if j < 7 and self.board[i+1][j+1] and self.board[i+1][j+1][0] == "w":
                if not isPinned or pinDirection == (1, 1):
                    moves.append(Move([i, j], [i+1, j+1], self.board))

    def getRookMoves(self, i, j, moves):
        """Generate all possible rook moves. """

        # We need to identify if the rook is pinned.
        # as well, if it is, we need to make sure that we can only
        # move that piece in the direction of the pin (or away from it)
        isPinned = False
        pinDirection = ()  # direction the piece is being pinned from

        for idx, pin in enumerate(self.pins):
            if pin[0] == i and pin[1] == j:
                isPinned = True
                pinDirection = (pin[2], pin[3])
                if self.board[i][j][1] != "Q":  # NOT SURE WHY THIS CONDITION YET
                    # NOT SURE WHY WE DO THIS YET
                    self.pins.remove(self.pins[idx])
                break

        # When checking for all the pin directions for the rook, we also need to
        # allow the rook to move toward (and away from) the pin, as both movements
        # will continue to protect the king

        # check up
        for r in range(i-1, -1, -1):
            if not isPinned or pinDirection == (-1, 0) or pinDirection == (1, 0):
                if not self.board[r][j]:  # if square is empty
                    moves.append(Move([i, j], [r, j], self.board))
                else:
                    if (self.board[r][j][0] == "w" and not self.whiteToMove) or \
                            (self.board[r][j][0] == "b" and self.whiteToMove):
                        moves.append(Move([i, j], [r, j], self.board))
                    break  # break out of the for loop since we can't keep checking further

        # check right
        for c in range(j+1, 8, 1):
            if not isPinned or pinDirection == (0, 1) or pinDirection == (1, 0):
                if not self.board[i][c]:  # if square is empty
                    moves.append(Move([i, j], [i, c], self.board))
                else:
                    if (self.board[i][c][0] == "w" and not self.whiteToMove) or \
                            (self.board[i][c][0] == "b" and self.whiteToMove):
                        moves.append(Move([i, j], [i, c], self.board))
                    break  # break out of the for loop since we can't keep checking further

        # check down
        for r in range(i+1, 8, 1):
            if not isPinned or pinDirection == (1, 0) or pinDirection == (-1, 0):
                if not self.board[r][j]:  # if square is empty
                    moves.append(Move([i, j], [r, j], self.board))
                else:
                    if (self.board[r][j][0] == "w" and not self.whiteToMove) or \
                            (self.board[r][j][0] == "b" and self.whiteToMove):
                        moves.append(Move([i, j], [r, j], self.board))
                    break  # break out of the for loop since we can't keep checking further

        # check left
        for c in range(j-1, -1, -1):
            if not isPinned or pinDirection == (0, -1) or pinDirection == (0, 1):
                if not self.board[i][c]:  # if square is empty
                    moves.append(Move([i, j], [i, c], self.board))
                else:
                    if (self.board[i][c][0] == "w" and not self.whiteToMove) or \
                            (self.board[i][c][0] == "b" and self.whiteToMove):
                        moves.append(Move([i, j], [i, c], self.board))
                    break  # break out of the for loop since we can't keep checking further

    def getKnightMoves(self, i, j, moves):
        """Generate all possible knight moves. """

        # We need to identify if the knight is pinned.
        # if it is, there is no way for us to capture the piece
        # that's pinning it, so we need to stop it from moving

        isPinned = False

        for idx, pin in enumerate(self.pins):
            if pin[0] == i and pin[1] == j:
                isPinned = True
                self.pins.remove(self.pins[idx])  # NOT SURE WHY WE DO THIS YET
                break

        # there are no possible moves for a knight if it is pinned by another piece
        if isPinned:
            return

        # all possible jumps in horiz/vert distance from current square
        jumps = [(-2, 1), (-1, 2), (1, 2), (2, 1),
                 (2, -1), (1, -2), (-1, -2), (-2, -1)]
        for x, y in jumps:
            r, c = i + x, j + y
            if -1 < r < 8 and -1 < c < 8:  # if the cell exists
                # if square is empty or occupied by opponent
                if (not self.board[r][c]) or \
                    ((self.board[r][c][0] == "w" and not self.whiteToMove) or
                        (self.board[r][c][0] == "b" and self.whiteToMove)):
                    moves.append(Move([i, j], [r, c], self.board))

    def getBishopMoves(self, i, j, moves):
        """Generate all possible bishop moves. """

        # We need to identify if the bishop is pinned.
        # as well, if it is, we need to make sure that we can only
        # move that piece in the direction of the pin (or away from it)
        isPinned = False
        pinDirection = ()  # direction the piece is being pinned from

        for idx, pin in enumerate(self.pins):
            if pin[0] == i and pin[1] == j:
                isPinned = True
                pinDirection = (pin[2], pin[3])
                self.pins.remove(self.pins[idx])  # NOT SURE WHY WE DO THIS YET
                break

        # When checking for all the pin directions for the bishop, we also need to
        # allow the bishop to move toward (and away from) the pin, as both movements
        # will continue to protect the king

        # check up-left
        r, c = i - 1, j - 1
        while r > -1 and c > -1:
            if not isPinned or pinDirection == (-1, -1) or pinDirection == (1, 1):
                if not self.board[r][c]:  # if square is empty
                    moves.append(Move([i, j], [r, c], self.board))
                else:
                    if (self.board[r][c][0] == "w" and not self.whiteToMove) or \
                            (self.board[r][c][0] == "b" and self.whiteToMove):
                        moves.append(Move([i, j], [r, c], self.board))
                    break  # break out of the for loop since we can't keep checking further

                r -= 1
                c -= 1
            else:
                # if pinned and the pin direction isn't in line with potential move,
                # we need to break out and avoid an infinite loop
                break

        # check up-right
        r, c = i - 1, j + 1
        while r > -1 and c < 8:
            if not isPinned or pinDirection == (-1, 1) or pinDirection == (1, -1):
                if not self.board[r][c]:
                    moves.append(Move([i, j], [r, c], self.board))
                else:
                    if (self.board[r][c][0] == "w" and not self.whiteToMove) or \
                            (self.board[r][c][0] == "b" and self.whiteToMove):
                        moves.append(Move([i, j], [r, c], self.board))
                    break  # break out of the for loop since we can't keep checking further

                r -= 1
                c += 1
            else:
                # if pinned and the pin direction isn't in line with potential move,
                # we need to break out and avoid an infinite loop
                break

        # check down-right
        r, c = i + 1, j + 1
        while r < 8 and c < 8:
            if not isPinned or pinDirection == (1, 1) or pinDirection == (-1, -1):
                if not self.board[r][c]:
                    moves.append(Move([i, j], [r, c], self.board))
                else:
                    if (self.board[r][c][0] == "w" and not self.whiteToMove) or \
                            (self.board[r][c][0] == "b" and self.whiteToMove):
                        moves.append(Move([i, j], [r, c], self.board))
                    break  # break out of the for loop since we can't keep checking further

                r += 1
                c += 1
            else:
                # if pinned and the pin direction isn't in line with potential move,
                # we need to break out and avoid an infinite loop
                break

        # check down-left
        r, c = i + 1, j - 1
        while r < 8 and c > -1:
            if not isPinned or pinDirection == (1, -1) or pinDirection == (-1, 1):
                if not self.board[r][c]:
                    moves.append(Move([i, j], [r, c], self.board))
                else:
                    if (self.board[r][c][0] == "w" and not self.whiteToMove) or \
                            (self.board[r][c][0] == "b" and self.whiteToMove):
                        moves.append(Move([i, j], [r, c], self.board))
                    break  # break out of the for loop since we can't keep checking further

                r += 1
                c -= 1
            else:
                # if pinned and the pin direction isn't in line with potential move,
                # we need to break out and avoid an infinite loop
                break

    def getQueenMoves(self, i, j, moves):
        """Generate all possible queen moves. """
        self.getBishopMoves(i, j, moves)
        self.getRookMoves(i, j, moves)

    def getKingMoves(self, i, j, moves):
        # after we make a king move, we need to make sure that it's not in check
        # we're going to do this by simulating the king move, and then calling the `findPinsAndChecks` function
        kingMoves = [(-1, -1), (-1, 0), (-1, 1), (0, 1),
                     (1, 1), (1, 0), (1, -1), (0, -1)]
        for x, y in kingMoves:
            r, c = i + x, j + y
            if -1 < r < 8 and -1 < c < 8:  # if the adjacent cell exists
                endPiece = self.board[r][c]
                # if the cell is empty or occupied by opponent
                if (not endPiece) or \
                    ((endPiece[0] == "w" and not self.whiteToMove) or
                        (endPiece[0] == "b" and self.whiteToMove)):

                    if self.whiteToMove:
                        self.whiteKingPosition = (r, c)
                    else:
                        self.blackKingPosition = (r, c)

                    inCheck, pins, checks = self.findPinsAndChecks()
                    print("inCheck: ", inCheck, "len(pins): ",
                          len(pins), "len(checks): ", len(checks))
                    if not inCheck:
                        moves.append(Move([i, j], [r, c], self.board))

                    if self.whiteToMove:
                        self.whiteKingPosition = (i, j)
                    else:
                        self.blackKingPosition = (i, j)

    def isInCheck(self):
        """ Determine if player is in check. """
        if self.whiteToMove:  # examine white king
            return self.isUnderAttack(self.whiteKingPosition[0], self.whiteKingPosition[1])
        else:  # examine black king
            return self.isUnderAttack(self.blackKingPosition[0], self.blackKingPosition[1])

    def isUnderAttack(self, i, j):
        """ Determine if a specific square is under attack. """

        # switch turns to validate opponent's possible moves
        self.whiteToMove = not self.whiteToMove
        opponentMoves = self.getAllPossibleMoves()
        for move in opponentMoves:
            if move.endRow == i and move.endCol == j:
                self.whiteToMove = not self.whiteToMove  # switch turns back
                return True

        # switch turns back if not under attack
        self.whiteToMove = not self.whiteToMove

    def findPinsAndChecks(self):
        """ Identifies all pins and checks on the king. """
        inCheck = False
        pins = []
        checks = []

        startRow = self.whiteKingPosition[0] if self.whiteToMove else self.blackKingPosition[0]
        startCol = self.whiteKingPosition[1] if self.whiteToMove else self.blackKingPosition[1]
        allyColor = "w" if self.whiteToMove else "b"
        enemyColor = "b" if self.whiteToMove else "w"

        # sorted by orthogonal directions, followed by diagonals
        kingDirections = [(-1, 0), (0, 1), (1, 0), (0, -1),
                          (-1, -1), (-1, 1), (1, 1), (1, -1)]

        # this loop will check for all potential pins and checks
        # from all pieces EXCEPT knights (done after for loop)
        for i, direction in enumerate(kingDirections):
            potentialPin = ()  # placeholder variable for a potential pin
            for distance in range(1, 8):
                # check all pieces in the given direction
                endRow = startRow + direction[0] * distance
                endCol = startCol + direction[1] * distance

                # if the square is on the board...
                if -1 < endRow < 8 and -1 < endCol < 8:
                    endPiece = self.board[endRow][endCol]

                    # ...and there's a piece there...
                    if endPiece:
                        # ... and it's an ally piece ...
                        if endPiece[0] == allyColor:
                            # ... and it is NOT the king
                            # (We need to add the king condition because the getKingMoves() function calls this after placing
                            # a "phantom" king to test for any potential checks if the move was made.
                            # We need to make sure that when this call is made that we aren't "protecting" our phantom king)
                            if endPiece[1] != "K":
                                if not potentialPin:
                                    # if there hasn't been a pin yet, save it!
                                    potentialPin = (
                                        endRow, endCol, direction[0], direction[1])
                                else:
                                    # otherwise, there's really no pin if we already ahve a "potential pin";
                                    # we have multiple layers of protection and can break out of this direction and move onto the next one
                                    break
                        else:
                            # But if it's an enemy piece...
                            # there are 6 potential enemy pieces that could be putting it into check:
                            # 1) could be a rook (orthogonal)
                            # 2) could be a bishop (diagonal)
                            # 3) could be a queen (anywhere)
                            # 4) could be a (white) pawn attacking upward
                            # 5) could be a (black) pawn attacking downwward
                            # 6) could be a knight (8 positions)

                            pieceType = endPiece[1]

                            # we will loop through all the directions and match them
                            # up with the appropriate piece to identify potential pin
                            # Note: The direction of the pawn movements are TOWARD the king, not away from him
                            if (0 <= i <= 3 and pieceType == "R") or \
                                (4 <= i <= 7 and pieceType == "B") or \
                                (pieceType == "Q") or \
                                (distance == 1 and pieceType == "P" and allyColor == "b" and (i == 6 or i == 7)) or \
                                (distance == 1 and pieceType == "P" and enemyColor == "w" and (i == 4 or i == 5)) or \
                                    (distance == 1 and pieceType == "K"):
                                if not potentialPin:
                                    # since there was no possible pin blocking this,
                                    # it must be a direct check
                                    inCheck = True
                                    checks.append(
                                        (endRow, endCol, direction[0], direction[1]))
                                else:
                                    # if there was a possible pin, we will  append it to actual pins
                                    # because it is clearly blocking a check
                                    pins.append(potentialPin)

                                break
                            else:
                                # there is no check from the opponent
                                break
                else:
                    # we are off the board
                    break

        # find any knight checks
        # note: there can NOT be any knight pins
        knightJumps = [(-2, 1), (-1, 2), (1, 2), (2, 1),
                       (2, -1), (1, -2), (-1, -2), (-2, -1)]
        for x, y in knightJumps:
            endRow = startRow + x
            endCol = startCol + y

            if -1 < endRow < 8 and -1 < endCol < 8:  # make sure we're on the board
                endPiece = self.board[endRow][endCol]
                # make sure piece is an enemy knight
                if endPiece and endPiece[0] == enemyColor and endPiece[1] == "N":
                    inCheck = True
                    checks.append((endRow, endCol, x, y))

        return inCheck, pins, checks

    def getValidMoves(self):
        """ Generates valid moves only. """

        validMoves = []
        self.inCheck, self.pins, self.checks = self.findPinsAndChecks()

        kingRow = self.whiteKingPosition[0] if self.whiteToMove else self.blackKingPosition[0]
        kingCol = self.whiteKingPosition[1] if self.whiteToMove else self.blackKingPosition[1]

        if self.inCheck:
            # if there is a check, we need to be very clear about what moves are valid
            if len(self.checks) == 1:
                # in this case, there is a single check
                # when there is a single check, the king may move, or we can block the check, or capture the piece
                moves = self.getAllPossibleMoves()
                checkRow, checkCol, checkDirectionX, checkDirectionY = self.checks[0]
                pieceChecking = self.board[checkRow][checkCol]

                # squares that pieces (apart from the king) can move to
                movesThatBlockCheck = []

                # king must be moved or knight must be captured
                if pieceChecking[1] == "N":
                    movesThatBlockCheck.append((checkRow, checkCol))
                else:
                    for i in range(1, 8):
                        square = (kingRow + checkDirectionX * i,
                                  kingCol + checkDirectionY * i)
                        movesThatBlockCheck.append(square)
                        if square[0] == checkRow and square[1] == checkCol:
                            break

                for move in moves:
                    if move.pieceMoved[1] == "K":
                        # if the king moved, he is not blocking the check but escaping it. this is valid
                        validMoves.append(move)
                    else:
                        # if it's not the king that was moved,
                        # then the piece that did move must be one of the moves that blocks the check
                        if (move.endRow, move.endCol) in movesThatBlockCheck:
                            validMoves.append(move)

            else:
                # in this case, there is a double check
                # when there is a double check, the king must move no matter what
                self.getKingMoves(kingRow, kingCol, moves)
        else:
            # if there is no check, anything goes
            # (pins are dealt with in the get<piece>Moves functions)
            validMoves = self.getAllPossibleMoves()

        print("numMoves: " + str(len(validMoves)),
              "kingPosition: " + str(self.whiteKingPosition))
        return validMoves

        # # 1) generate all possible moves
        # allMoves = self.getAllPossibleMoves()
        # validMoves = []

        # for move in allMoves:
        #     # 2) for each move, make the move
        #     self.makeMove(move)

        #     # 3) generate every opponent move
        #     # 4) for each opponent move, see if it attacks our king

        #     # At the start of this function, we check all possible moves for 1 color (e.g. white)
        #     # Then, we actually proceed to make the move, which would switch turns to black
        #     # So, we now need to manually switch back to make sure it's white's move so that when
        #     # we're determining if they're in check, we're looking at the white king
        #     self.whiteToMove = not self.whiteToMove

        #     # 5) if king is not attacked, add it to valid moves
        #     if not self.isInCheck():
        #         validMoves.append(move)

        #     # the undoMove function toggles player turn, so we need to manually toggle it back
        #     self.undoMove()
        #     self.whiteToMove = not self.whiteToMove

        # # check for checkmate or stalemate
        # if not validMoves:
        #     if self.isInCheck():
        #         print('checkmate')
        #         self.checkmate = True
        #     else:
        #         print('stalemate')
        #         self.stalemate = True
        # # else statement sets flags to False so we can undo moves if in check/stale mates
        # else:
        #     self.checkmate = False
        #     self.stalemate = False

        # return validMoves

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
