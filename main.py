import copy
import numpy as np


class SudokuHelpUtils:
    """Helpful utilities used to organise sudoku"""

    def __init__(self):
        """Create the helper lists"""
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

    def __cross_product(self, A, B):
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

        for i in [[0, 1, 2], [3, 4, 5], [6, 7, 8]]:
            for j in [[0, 1, 2], [3, 4, 5], [6, 7, 8]]:
                self.box_list.append(self.__cross_product(i, j))

    def get_units(self) -> list:
        """Gets each coordinate's related elements from rows, columns and its box, including the coordinate itself."""

        all_relations = (self.row_list + self.column_list + self.box_list)

        all_unit_relations = [[u for u in all_relations if s in u] for s in self.squares_list]
        self.unit_list = np.array_split(all_unit_relations, 9)
        # print(self.unit_list[1][0])
        return self.unit_list

    def __generate_peers(self):
        """Get each coordinates related elements from rows, columns and its box, excluding the coordinate itself."""
        # for s in self.squares_list:
        for s in self.squares_list:
            numpy_edition = np.array(self.get_units()[s[0]][s[1]])
            numpy_edition = (numpy_edition.reshape(-1, numpy_edition.shape[-1]))
            numpy_edition = np.unique(numpy_edition, axis=0)
            numpy_edition = [x for x in numpy_edition if not np.array_equal(x, s)]
            # print(numpy_edition)
            self.peer_list.append(numpy_edition)
        # print(self.peer_list)
        self.peer_list = np.array_split(self.peer_list, 9)
        return self.peer_list

    def get_peers(self):
        return self.peer_list

    def to_backtrack_or_not(self, values):
        for items in values:
            if items:
                return items
        # If the assert function returns false due to breaking a constraint
        # then some function returns false
        return False


helpful_stuff = SudokuHelpUtils()


def display_sudkou(values):
    # print(values)
    if values == False:
        return np.array([[-1] * 9] * 9)

    values_2 = [[] for _ in range(9)]
    # print("bob")
    # print(values_2)
    for i in range(9):

        for j in range(9):
            # print(i,j)
            values_2[i].append(values[i][j][0])
    # print(values_2)
    return values_2


def parse_sudoku(sudoku):
    values = [[list(range(1, 10)) for _ in range(9)] for _ in range(9)]
    for row in range(9):
        for column in range(9):
            square_value = sudoku[row][column]
            # print(row, column, square_value)
            if square_value in [1, 2, 3, 4, 5, 6, 7, 8, 9] and not assign(values, (row, column), square_value):
                return False  # We cant assign d to square square_value
    return values


def assign(values, coordinates, square_value):
    other_values = values[coordinates[0]][coordinates[1]].copy()
    try:
        other_values.remove(square_value)
    except ValueError:
        return False
    # print(other_values)
    # print(values[coordinates[0]][coordinates[1]])

    if all(eliminate(values, coordinates, possible_values) for possible_values in other_values):
        return values
    else:
        return False
    # If a square has only 1 possible value then eliminate that value from its peers

    # If a unit has only one possible place for a value then place it there


def eliminate(values, coordinates, square_value):
    # print(values)
    if square_value not in values[coordinates[0]][coordinates[1]]:
        return values
    # print(values[coordinates[0]][coordinates[1]])
    values[coordinates[0]][coordinates[1]].remove(square_value)
    # print(values[coordinates[0]][coordinates[1]])

    # If a square eventually reaches one possible square value then remove it from its peers
    if len(values[coordinates[0]][coordinates[1]]) == 0:
        return False
    elif len(values[coordinates[0]][coordinates[1]]) == 1:
        other_values = values[coordinates[0]][coordinates[1]][0]
        if not all(eliminate(values, peer_coordinates, other_values) for peer_coordinates in
                   helpful_stuff.get_peers()[coordinates[0]][coordinates[1]]):
            return False

    # If a unit is reduced to only one place then put it there.
    for u in helpful_stuff.get_units()[coordinates[0]][coordinates[1]]:
        dplaces = [coordinates for coordinates in u if square_value in values[coordinates[0]][coordinates[1]]]
        if len(dplaces) == 0:
            return False
        elif len(dplaces) == 1:
            if not assign(values, dplaces[0], square_value):
                return False
    return values


def search(values):
    if values is False:
        print("Values is false")
        return False
    if all(len(values[coordinate[0]][coordinate[1]]) == 1 for coordinate in helpful_stuff.squares_list):
        print("Solved")
        return values
    length_coordinate = min(len(values[coordinate[0]][coordinate[1]]) for coordinate in helpful_stuff.squares_list if
                            len(values[coordinate[0]][coordinate[1]]) > 1)
    next_coordinate = min(
        coordinate for coordinate in helpful_stuff.squares_list if len(values[coordinate[0]][coordinate[1]]) > 1)
    return helpful_stuff.to_backtrack_or_not(
        search(assign(copy.deepcopy(values), next_coordinate, next_value)) for next_value in
        values[next_coordinate[0]][next_coordinate[1]])


def sudoku_solver(sudoku):
    def solve(grid):
        return search(parse_sudoku(grid))

    return display_sudkou(solve(sudoku))


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
