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
            if square_value in [1, 2, 3, 4, 5, 6, 7, 8, 9] and not assign(values, (row, column), square_value):
                return False  # We cant assign d to square square_value
    return values


def assign(values, coordinates, square_value):
    other_values = values[coordinates[0]][coordinates[1]].copy()
    other_values.remove(square_value)
    print(other_values)
    print(values[coordinates[0]][coordinates[1]])


def cross_product(A, B):
    return [(a, b) for a in A for b in B]