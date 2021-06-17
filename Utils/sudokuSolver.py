"""
Example input board
this is the type of board we need to give as an input to solve sudoku problem
board = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]
"""

# takes the board as input and solves the problem
def solve(bo):
    find = find_empty(bo)  # finds the empty location and return a tuple of (row, col)
    if not find:  # if board is completely filled which means we have reached valid sol
        return True
    else:  # if board has empty location
        row, col = find
    for i in range(1, 10):  # try all the values from 0 to 9 in the empty and consider the value which is valid at that loc
        if valid(bo, i, (row, col)):  # check if value i is valid at particular location
            bo[row][col] = i  # if valid then put that value in that loc.
            if solve(bo):  # then recursively call the solve function by passing the board to fill next empty loc.
                return True  # if the board is completely filled then return true
            bo[row][col] = 0  # if current building sol is not valid then un-fill the value by filling 0 into it and make it empty again
    return False  # after trying all the 0 to 9 values if they don't fit then return false so we can backtrack

#  to check whether the given value is valid at particular location
def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:  # checking if the num is present in same row, if yes then return false
            return False
    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:  # checking if the num is present in same col, if yes then return false
            return False
    # Check box
    # finding the location of boxes
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    for i in range(box_y*3, box_y*3 + 3):  # changing the row index
        for j in range(box_x * 3, box_x*3 + 3):  # changing the col index by keeping row index const
            if bo[i][j] == num and (i, j) != pos:  # if num is present in box return false
                return False
    return True  # if num is valid at particular pos return true

# to print sudoku board in proper manner
def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:  # after every 3 row's
            print("- - - - - - - - - - - - - ")
        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:  # after every 3 col's
                print(" | ", end="")
            if j == 8:  # after printing 9th element of row break the line and start from next line
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")  # print the value of board

#  function to find first empty position in board
def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j )  # row, col
    return None  # if board does not have any empty position which means we have reached final sol
