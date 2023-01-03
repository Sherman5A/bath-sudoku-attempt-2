import numpy as np

# columns are 1-9
# rows A-I
# collection of 9 squares (be it a column row or box) are a unit
# squares that share a unit are peers
# Each square must have a different value than its peers

# i WILL USE A 9X9 ARRAY
# single digit for already given
# this will be called values
# going to use list for possible values

test_sudoku = [[4, 0, 0, 0, 0, 0, 8, 0, 5],
               [0, 3, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 7, 0, 0, 0, 0, 0],
               [0, 2, 0, 0, 0, 0, 0, 6, 0],
               [0, 0, 0, 0, 8, 0, 4, 0, 0],
               [0, 0, 0, 0, 1, 0, 0, 0, 0],
               [0, 0, 0, 6, 0, 3, 0, 7, 0],
               [5, 0, 0, 2, 0, 0, 0, 0, 0],
               [1, 0, 4, 0, 0, 0, 0, 0, 0]
               ]


def parse_sudoku(sudoku):
    values = [[list(range(1, 10)) for _ in range(9)] for _ in range(9)]
    for row in range(9):
        for column in range(9):
            square_value = sudoku[row][column]
            print(row, column, square_value)

