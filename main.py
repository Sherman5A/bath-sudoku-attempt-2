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


class SudokuHelpUtils:
    """Helpful utilities used to organise sudoku"""

    def __init__(self):
        """Create the helper lists"""
        self.row_list = []
        self.__get_row_relations()
        self.column_list = []
        self.__get_column_relations()
        self.box_list = []
        self.__get_box_relations()

    def __cross_product(self, A, B):
        """Creates the cross product of two given lists."""

        return [(a, b) for a in A for b in B]

    def __get_row_relations(self):
        """Creates a list containing the coordinates of all the sudoku's rows"""
        # get rows
        for i in range(9):
            self.row_list.append([(row, i) for row in range(9)])

    def __get_column_relations(self):
        """Creates a list containing the coordinates of all the sudoku's columns"""
        for i in range(9):
            self.column_list.append([(i, column) for column in range(9)])

    def __get_box_relations(self):
        """Creates a list containing the coordinates of all the boxes in a 9x9 sudoku"""
        for i in [[0, 1, 2], [3, 4, 5], [6, 7, 8]]:
            for j in [[0, 1, 2], [3, 4, 5], [6, 7, 8]]:
                self.box_list.append(self.__cross_product(i, j))

    def get_units(self):
        """Gets each coordinate's related elements from rows, columns and its box, including the coordinate itself."""

    def get_peers(self):
        """Get each coordinates related elements from rows, columns and its box, excluding the coordinate itself."""
