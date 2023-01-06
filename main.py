import copy

import numpy as np


class SudokuHelpUtils:
    """Helpful utilities used to organise sudoku"""

    def __init__(self):
        """Create the helper lists and populate them"""
        self.squares_list = []
        self.__get_sudoku_elements()
        self.row_list = []
        self.__get_row_relations()
        self.column_list = []
        self.__get_column_relations()
        self.box_list = []
        self.__get_box_relations()
        self.unit_list = []
        self.peer_list = []
        self.__generate_peers()

    def __cross_product(self, A, B) -> list:
        """Creates the cross product of two given lists."""

        return [(a, b) for a in A for b in B]

    def __get_sudoku_elements(self):
        """Gets a list containing the coordinates of every sudoku element."""
        rows = list(range(9))
        columns = list(range(9))
        self.squares_list = self.__cross_product(rows, columns)

    def __get_row_relations(self):
        """Creates a list containing the coordinates of all the sudoku's rows"""

        for i in range(9):
            self.row_list.append([(row, i) for row in range(9)])

    def __get_column_relations(self):
        """Creates a list containing the coordinates of all the sudoku's columns"""

        for i in range(9):
            self.column_list.append([(i, column) for column in range(9)])

    def __get_box_relations(self):
        """Creates a list containing the coordinates of all the boxes in a 9x9 sudoku"""

        # Iterate through all the 3xe boxes of the sudoku.
        for i in [[0, 1, 2], [3, 4, 5], [6, 7, 8]]:
            for j in [[0, 1, 2], [3, 4, 5], [6, 7, 8]]:
                self.box_list.append(self.__cross_product(i, j))

    def get_units(self) -> list:
        """Gets each coordinate's related elements from rows, columns and its box, including the coordinate itself."""

        # Concatenate all the list relations.
        all_relations = (self.row_list + self.column_list + self.box_list)

        # Go through every coordinate and get lists related to that coordinates
        # in rows, columns, and the squares.
        all_unit_relations = [[u for u in all_relations if s in u] for s in self.squares_list]
        # Split the list into nested lists of 9 elements each.
        self.unit_list = np.array_split(all_unit_relations, 9)
        return self.unit_list

    def __generate_peers(self):
        """Get each coordinates related elements from rows, columns and its box, excluding the coordinate itself in a
           "flat-ish" list"""

        # for s in self.squares_list:
        for s in self.squares_list:
            peers = np.array(self.get_units()[s[0]][s[1]])
            # Flatten last layer of the nested list.
            peers = (peers.reshape(-1, peers.shape[-1]))
            # Remove repeated coordinates
            peers = np.unique(peers, axis=0)
            peers = [x for x in peers if not np.array_equal(x, s)]
            self.peer_list.append(peers)
        # print(self.peer_list)
        self.peer_list = np.array_split(self.peer_list, 9)

    def get_peers(self):
        """Gets the peers"""
        return self.peer_list

    def to_backtrack_or_not(self, values):
        """If the search successfully returns values, continue,
           otherwise return false"""
        for items in values:
            if items != False:
                return items
        # If the assert function returns false due to breaking a constraint
        # then some function returns false
        return False


def init_sudoku(sudoku):
    """Initialises the sudoku values grid and reads the given sudoku into the grid."""

    # Create grid 9x9 grid of lists containing the integers 1-9.
    values = [[list(range(1, 10)) for _ in range(9)] for _ in range(9)]
    for row in range(9):
        for column in range(9):
            square_value = sudoku[row][column]
            # print(row, column, square_value)
            if square_value in [1, 2, 3, 4, 5, 6, 7, 8, 9] and not assign_value(values, (row, column), square_value):
                return False  # We cant assign d to square square_value
    return values


def assign_value(values: list, coordinates: tuple, square_value: int):
    """Assign a value to an element."""

    other_values = values[coordinates[0]][coordinates[1]].copy()

    # If value does not exist already in the list, produce error
    # This prevents double related numbers in the sudoku grid.
    try:
        other_values.remove(square_value)
    except ValueError:
        return False
    # print(other_values)
    # print(values[coordinates[0]][coordinates[1]])

    # Remove the value from the element and its related elements.
    if all(remove_related_values(values, coordinates, possible_values) for possible_values in other_values):
        return values
    else:
        return False


def remove_related_values(values: list, coordinates: tuple, square_value: int):
    """Remove related values from the element's coordinates.s"""

    # print(values)
    if square_value not in values[coordinates[0]][coordinates[1]]:
        return values
    # print(values[coordinates[0]][coordinates[1]])
    values[coordinates[0]][coordinates[1]].remove(square_value)
    # print(values[coordinates[0]][coordinates[1]])

    # If an element eventually reaches one possible square value then remove it from its related elements.
    if len(values[coordinates[0]][coordinates[1]]) == 0:
        return False
    elif len(values[coordinates[0]][coordinates[1]]) == 1:
        other_values = values[coordinates[0]][coordinates[1]][0]
        if not all(remove_related_values(values, peer_coordinates, other_values) for peer_coordinates in
                   sudoku_help_utils.get_peers()[coordinates[0]][coordinates[1]]):
            return False

    # If a unit is reduced to only one place then put it there.
    for unit in sudoku_help_utils.get_units()[coordinates[0]][coordinates[1]]:
        unit_values = [coordinates for coordinates in unit if square_value in values[coordinates[0]][coordinates[1]]]
        if len(unit_values) == 0:
            return False
        elif len(unit_values) == 1:
            if not assign_value(values, unit_values[0], square_value):
                return False
    return values


def backtrack_search(values: list):
    """Perform a backtracking search."""

    if values is False:
        return False

    # Terminating condition for checking if the sudoku is solved.
    if all(len(values[coordinate[0]][coordinate[1]]) == 1 for coordinate in sudoku_help_utils.squares_list):
        return values

    # Pick the element with the smallest amount of values
    next_coordinate = min(
        coordinate for coordinate in sudoku_help_utils.squares_list if len(values[coordinate[0]][coordinate[1]]) > 1)

    # Try to assign the possible values to the element, using a copy of the values.
    return sudoku_help_utils.to_backtrack_or_not(
        backtrack_search(assign_value(copy.deepcopy(values), next_coordinate, next_value)) for next_value in
        values[next_coordinate[0]][next_coordinate[1]])


def sudoku_solver(sudoku: list):
    """Driver code for sudoku"""

    global sudoku_help_utils
    sudoku_help_utils = SudokuHelpUtils()

    # Nested functions clear my very messy global namespace :))
    # Don't complain.
    def return_sudoku(values: list):
        """Return sudoku when solved, or if search failed, return the failure sudoku."""

        # If search fails return 9x9 numpy array of -1s.
        if values == False:
            return np.array([[-1] * 9] * 9)

        formatted_values = [[] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                formatted_values[i].append(values[i][j][0])
        # print(formatted_values)
        return formatted_values

    def solve(sudoku_grid: list):
        return backtrack_search(init_sudoku(sudoku_grid))

    return return_sudoku(solve(sudoku))


# **************** Coursework Driver Code ****************

SKIP_TESTS = False


def tests():
    import time
    difficulties = ["very_easy", "easy", "medium", "hard"]

    for difficulty in difficulties:

        print(f"Testing {difficulty} sudokus")

        sudokus = np.load(f"data/{difficulty}_puzzle.npy")
        solutions = np.load(f"data/{difficulty}_solution.npy")

        count = 0
        for i in range(len(sudokus)):
            sudoku = sudokus[i].copy()
            print(f"This is {difficulty} sudoku number", i)
            print(sudoku)

            start_time = time.process_time()
            your_solution = sudoku_solver(sudoku)
            end_time = time.process_time()

            print(f"This is your solution for {difficulty} sudoku number", i)
            print(your_solution)

            print("Is your solution correct?")
            if np.array_equal(your_solution, solutions[i]):
                print("Yes! Correct solution.")
                count += 1
            else:
                print("No, the correct solution is:")
                print(solutions[i])

            print("This sudoku took", end_time - start_time, "seconds to solve.\n")

        print(f"{count}/{len(sudokus)} {difficulty} sudokus correct")
        if count < len(sudokus):
            break


if not SKIP_TESTS:
    tests()
