import numpy as np
def isValid(board):
    row, col, box = set(), set(), set()
    for i in range(9):
        for j in range(9):
            if board[i][j]!= 0:
                rowKey = (i, board[i][j])
                colKey = (j, board[i][j])
                boxKey = (i//3, j//3, board[i][j])
                if (rowKey in row) or (colKey in col) or (boxKey in box):
                    return False
                row.add(rowKey)
                col.add(colKey)
                box.add(boxKey)
    return True

def noZero(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return False
    return True
