class ChessNotation():
    __init__(self):
        self.rankToRow = {"1": 7, "2": 6, "3": 5,
                          "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
        self.rowToRank = {val: key for key, val in self.rankToRow.items()}
        self.fileToCol = {"a": 0, "b": 1, "c": 2,
                          "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
        self.colToFile = {val: key for key, val in self.fileToCol.items()}

    def get_chess_notation(self):
        # Converting array indices to proper chess notation.
        start = self.colToFile[self.startCol] + self.rowToRank[self.startRow]
        end = self.colToFile[self.endCol] + self.rowToRank[self.endRow]
        return start + "-" + end
