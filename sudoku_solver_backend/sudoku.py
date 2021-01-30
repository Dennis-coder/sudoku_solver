import math
import time
import copy

class Sudoku:
    # Initializes the object and sets its properties
    def __init__(self, input_data):
        self.__done = False
        self.__error = None
        self.__refactor_input(input_data)
        self.__set_all_possible_numbers()

    # Refactors the input
    def __refactor_input(self, input_data):
        if isinstance(input_data, str):
            rows = input_data.split("\n")
            for i in range(9):
                rows[i] = rows[i].split(",")
                for j in range(9):
                    if rows[i][j] == " ":
                        rows[i][j] = []
                    else:
                        rows[i][j] = int(rows[i][j])
        elif isinstance(input_data, list):
            rows = input_data
            for i in range(9):
                for j in range(9):
                    if isinstance(rows[i][j], list):
                        rows[i][j] = []
        else:
            raise
        self.__rows = rows

    # Set the columns property of the object based on the rows property
    def __columns(self):
        columns = []
        for i in range(9):
            col = []
            for j in range(9):
                col.append(self.__rows[j][i])
            columns.append(col)
        return columns

    # Set the squares property of the object based on the rows property
    def __squares(self):
        squares = []
        for squares_row in range(3):
            for s_col in range(3):
                square = []
                for row in range(3):
                    for col in range(3):
                        square.append(self.__rows[squares_row * 3 + row][s_col * 3 + col])
                squares.append(square)
        return squares

    # Returns the row, column, and square that intersects the given coordinates
    def __get_row_column_square(self, row_i, col_i):
        row = self.__rows[row_i]
        col = self.__columns()[col_i]
        square = self.__squares()[(math.floor(row_i/3) * 3) + math.floor(col_i / 3)]
        return row, col, square

    # Returns the row and column given the squares index and the numbers index inside the square
    def __get_row_column_from_square(self, square, index):
        row = math.floor(square / 3) * 3 + math.floor(index / 3)
        col = (square % 3) * 3 + (index % 3)
        return row, col

    # Returns a list of all the possible numbers that can be in a specific spot given the coordinates
    def __get_possible_numbers(self, row_i, col_i):
        possible_numbers = [1,2,3,4,5,6,7,8,9]

        row, col, square = self.__get_row_column_square(row_i, col_i)

        possible_numbers = [num for num in possible_numbers if num not in row]
        possible_numbers = [num for num in possible_numbers if num not in col]
        possible_numbers = [num for num in possible_numbers if num not in square]

        if len(possible_numbers) > 0:
            return possible_numbers
        else:
            raise Exception("No possible numbers")
    
    # Set the list of possible numbers to every spot
    def __set_all_possible_numbers(self):
        try:
            for row in range(9):
                for col in range(9):
                    if not isinstance(self.__rows[row][col], int):
                        possible_numbers = self.__get_possible_numbers(row, col)
                        self.__rows[row][col] = possible_numbers
        except Exception as error:
            self.__error = error
            self.__done = True

    # Sets a value given coordinates and the value
    def __set_value(self, row_i, col_i, value):
        row, col, square = self.__get_row_column_square(row_i, col_i)
        
        for index, value2 in enumerate(row):
            if isinstance(value2, list) and value in value2:
                self.__rows[row_i][index].remove(value)
        
        for index, value2 in enumerate(col):
            if isinstance(value2, list) and value in value2:
                self.__rows[index][col_i].remove(value)
        
        for index, value2 in enumerate(square):
            if isinstance(value2, list) and value in value2:
                self.__rows[(math.floor(row_i / 3) * 3 + math.floor(index / 3))][(math.floor(col_i / 3) * 3 + (index % 3))].remove(value)

        self.__rows[row_i][col_i] = value

    # Checks if the sudoku has changed after executing a function
    def __changed(self, function):
        list_before = copy.deepcopy(self.__rows)
        function()
        return not (list_before == self.__rows)

    # Checks if a spot only has one possible number and sets it if it's true
    def __check_if_only_one_possible_number(self):
        for row in range(9):
            for col in range(9):
                value = self.__rows[row][col]
                if isinstance(value, list):
                    if len(value) == 1:
                        self.__set_value(row, col, value[0])
    
    # Checks if a number can only go in one spot in the specific row and sets it if it's true
    def __check_if_only_one_possible_spot_in_row(self):
        for row in range(9):
            for col in range(9):
                if isinstance(self.__rows[row][col], list):
                    for value in self.__rows[row][col]:
                        add = True
                        for value2_i, value2 in enumerate(self.__rows[row]):
                            if col != value2_i and isinstance(value2, list) and value in value2:
                                add = False
                        if add == True:
                            self.__set_value(row, col, value)

    # Checks if a number can only go in one spot in the specific column and sets it if it's true
    def __check_if_only_one_possible_spot_in_column(self):
        for col in range(9):
            for row in range(9):
                if isinstance(self.__columns()[col][row], list):
                    for value in self.__columns()[col][row]:
                        add = True
                        for value2_i, value2 in enumerate(self.__columns()[col]):
                            if row != value2_i and isinstance(value2, list) and value in value2:
                                add = False
                        if add == True:
                            self.__set_value(row, col, value)

    # Checks if a number can only go in one spot in the specific square and sets it if it's true
    def __check_if_only_one_possible_spot_in_square(self):
        for square in range(9):
            for index in range(9):
                if isinstance(self.__squares()[square][index], list):
                    for value in self.__squares()[square][index]:
                        add = True
                        for value2_i, value2 in enumerate(self.__squares()[square]):
                            if index != value2_i and isinstance(value2, list) and value in value2:
                                add = False
                        if add == True:
                            row, col = self.__get_row_column_from_square(square, index)
                            self.__set_value(row, col, value)

    # Checks if two numbers can only go in the same two spots in a row
    def __two_nums_two_spots_check_rows(self):
        for row in range(9):
            for index in range(9):
                if isinstance(self.__rows[row][index], list):
                    for value_i in range(9):
                        value = self.__rows[row][value_i]
                        if index != value_i and isinstance(value, list):
                            shared_possible_numbers = [num for num in self.__rows[row][index] if num in value]
                            for value2_i, value2 in enumerate(self.__rows[row]):
                                if index != value2_i and value_i != value2_i and isinstance(value2, list):
                                    shared_possible_numbers = [num for num in shared_possible_numbers if num not in value2]
                            if len(shared_possible_numbers) == 2:
                                for i in range(9):
                                    if isinstance(self.__rows[row][i], list):
                                        if i == index or i == value_i:
                                            self.__rows[row][i] = copy.deepcopy(shared_possible_numbers)
                                        else:
                                            self.__rows[row][i] = [num for num in self.__rows[row][i] if num not in shared_possible_numbers]

    # Checks if two numbers can only go in the same two spots in a column
    def __two_nums_two_spots_check_columns(self):
        for col in range(9):
            for index in range(9):
                if isinstance(self.__columns()[col][index], list):
                    for value_i in range(9):
                        value = self.__columns()[col][value_i]
                        if index != value_i and isinstance(value, list):
                            shared_possible_numbers = [num for num in self.__columns()[col][index] if num in value]
                            for value2_i, value2 in enumerate(self.__columns()[col]):
                                if index != value2_i and value_i != value2_i and isinstance(value2, list):
                                    shared_possible_numbers = [num for num in shared_possible_numbers if num not in value2]
                            if len(shared_possible_numbers) == 2:
                                for i in range(9):
                                    if isinstance(self.__columns()[col][i], list):
                                        if i == index or i == value_i:
                                            self.__rows[i][col] = copy.deepcopy(shared_possible_numbers)
                                        else:
                                            self.__rows[i][col] = [num for num in self.__rows[i][col] if num not in shared_possible_numbers]

    # Checks if two numbers can only go in the same two spots in a square
    def __two_nums_two_spots_check_squares(self):
        for square in range(9):
            for index in range(9):
                if isinstance(self.__squares()[square][index], list):
                    for value_i in range(9):
                        value = self.__squares()[square][value_i]
                        if index != value_i and isinstance(value, list):
                            shared_possible_numbers = [num for num in self.__squares()[square][index] if num in value]
                            for value2_i, value2 in enumerate(self.__squares()[square]):
                                if index != value2_i and value_i != value2_i and isinstance(value2, list):
                                    shared_possible_numbers = [num for num in shared_possible_numbers if num not in value2]
                            if len(shared_possible_numbers) == 2:
                                for i in range(9):
                                    row, col = self.__get_row_column_from_square(square, i)
                                    if isinstance(self.__squares()[square][i], list):
                                        if i == index or i == value_i:
                                            self.__rows[row][col] = copy.deepcopy(shared_possible_numbers)
                                        else:
                                            self.__rows[row][col] = [num for num in self.__rows[row][col] if num not in shared_possible_numbers]

    def __only_one_possible_row_or_column_in_square_check(self):
        for s_row in range(3):
            for s_col in range(3):
                for number in range(1,10):
                    possible_indexes = [index for index, value in enumerate(self.__squares()[s_row * 3 + s_col]) if isinstance(value, list) and number in value]

                    if len(possible_indexes) == 3:
                        if math.floor(possible_indexes[0] / 3) == math.floor(possible_indexes[1] / 3) == math.floor(possible_indexes[2] / 3): # Row
                            row_i = s_row * 3 + math.floor(possible_indexes[0] / 3)
                            indexes = [index for index, value in enumerate(self.__rows[row_i]) if isinstance(value, list) and number in value and (index < s_col * 3 or index >= (s_col + 1) * 3)]
                            for index in indexes:
                                self.__rows[row_i][index].remove(number)

                        if possible_indexes[0] % 3 == possible_indexes[1] % 3 == possible_indexes[2] % 3: # Column
                            col_i = s_col * 3 + possible_indexes[0] % 3
                            indexes = [index for index, value in enumerate(self.__columns()[col_i]) if isinstance(value, list) and number in value and (index < s_row * 3 or index >= (s_row + 1) * 3)]
                            for index in indexes:
                                self.__rows[index][col_i].remove(number)

                    elif len(possible_indexes) == 2:
                        if math.floor(possible_indexes[0] / 3) == math.floor(possible_indexes[1] / 3): # Row
                            row_i = s_row * 3 + math.floor(possible_indexes[0] / 3)
                            indexes = [index for index, value in enumerate(self.__rows[row_i]) if isinstance(value, list) and number in value and (index < s_col * 3 or index >= (s_col + 1) * 3)]
                            for index in indexes:
                                self.__rows[row_i][index].remove(number)

                        if possible_indexes[0] % 3 == possible_indexes[1] % 3: # Column
                            col_i = s_col * 3 + possible_indexes[0] % 3
                            indexes = [index for index, value in enumerate(self.__columns()[col_i]) if isinstance(value, list) and number in value and (index < s_row * 3 or index >= (s_row + 1) * 3)]
                            for index in indexes:
                                self.__rows[index][col_i].remove(number)

    def __same_number_in_two_squares_in_same_two_rows_check(self):
        for s_row in range(3):
            for number in range(1,10):
                all_indexes = []
                unique_relative_indexes = []
                for s_col in range(3):
                    all_indexes.append([index for index, value in enumerate(self.__squares()[s_row * 3 + s_col]) if isinstance(value, list) and number in value])
                    relative_indexes = [math.floor(index / 3) for index, value in enumerate(self.__squares()[s_row * 3 + s_col]) if isinstance(value, list) and number in value]
                    unique_relative_indexes.append(list(set(relative_indexes)))
                indexes_to_change = copy.deepcopy(unique_relative_indexes)
                for s_index in range(3):
                    for s_index2 in range(3):
                        if s_index != s_index2:
                            indexes_to_change[s_index] = [num for num in indexes_to_change[s_index] if num not in unique_relative_indexes[s_index2]]
                for s_col, square in enumerate(indexes_to_change):
                    for relative_row_i in square:
                        for index in all_indexes[s_col]:
                            if math.floor(index / 3) != relative_row_i:
                                self.__rows[s_row * 3 + math.floor(index / 3)][s_col * 3 + index % 3].remove(number)

    def __same_number_in_two_squares_in_same_two_columns_check(self):
        for s_col in range(3):
            for number in range(1,10):
                all_indexes = []
                unique_relative_indexes = []
                for s_row in range(3):
                    all_indexes.append([index for index, value in enumerate(self.__squares()[s_row * 3 + s_col]) if isinstance(value, list) and number in value])
                    relative_indexes = [index % 3 for index, value in enumerate(self.__squares()[s_row * 3 + s_col]) if isinstance(value, list) and number in value]
                    unique_relative_indexes.append(list(set(relative_indexes)))
                indexes_to_change = copy.deepcopy(unique_relative_indexes)
                for s_index in range(3):
                    for s_index2 in range(3):
                        if s_index != s_index2:
                            indexes_to_change[s_index] = [num for num in indexes_to_change[s_index] if num not in unique_relative_indexes[s_index2]]
                for s_row, square in enumerate(indexes_to_change):
                    for relative_col_i in square:
                        for index in all_indexes[s_row]:
                            if index % 3 != relative_col_i:
                                self.__rows[s_row * 3 + math.floor(index / 3)][s_col * 3 + index % 3].remove(number)

    def __recursive_testing(self):
        nums = None
        for i in range(9):
            for j in range(9):
                if isinstance(self.__rows[i][j], list):
                    nums = self.__rows[i][j]
                    break
            if isinstance(nums, list):
                break
        for num in nums:
            self.__rows[i][j] = num
            rows = copy.deepcopy(self.__rows)
            sudoku = Sudoku(rows)
            sudoku.solve()
            if sudoku.correct() == "Correct!":
                self.__rows = sudoku.rows
                break

    def stringify(self):
        out = ""
        for i in range(9):
            for j in range(9):
                if isinstance(self.__rows[i][j], int):
                    out += str(self.__rows[i][j])
                else:
                    out += " "
                out += ","
            out = out[:-1]
            out += "\n"
        out = out[:-1]
        return out

    def iterate(self):
        if self.correct() == "Correct!":
            self.__done = True
            return
        if self.__changed(self.__check_if_only_one_possible_number): return
        if self.__changed(self.__check_if_only_one_possible_spot_in_row): return
        if self.__changed(self.__check_if_only_one_possible_spot_in_column): return
        if self.__changed(self.__check_if_only_one_possible_spot_in_square): return
        if self.__changed(self.__two_nums_two_spots_check_rows): return
        if self.__changed(self.__two_nums_two_spots_check_columns): return
        if self.__changed(self.__two_nums_two_spots_check_squares): return
        if self.__changed(self.__only_one_possible_row_or_column_in_square_check): return
        if self.__changed(self.__same_number_in_two_squares_in_same_two_rows_check): return
        if self.__changed(self.__same_number_in_two_squares_in_same_two_columns_check): return
        if self.__changed(self.__recursive_testing): return
        self.__done = True

    def solve(self):
        while not self.done:
            self.iterate()

    def correct(self):
        numbers = [1,2,3,4,5,6,7,8,9]
        wrong = []
        try:
            for i, row in enumerate(self.__rows):
                if numbers != sorted(row):
                    wrong.append("Row: %d" % i)
            for i, cols in enumerate(self.__columns()):
                if numbers != sorted(cols):
                    wrong.append("Column: %d" %i)
            for i, square in enumerate(self.__squares()):
                if numbers != sorted(square):
                    wrong.append("Square: %d" %i)
        except:
            for row in self.__rows:
                for value in row:
                    if value == []:
                        return "No possible values"
            return "Incomplete..."

        if len(wrong) == 0:
            return "Correct!"
        else:
            return "Wrong at: " + ", ".join(wrong)

    def print(self):
        print("")
        for i in range(9):
            printing = " ".join([str(num) if isinstance(num, int) else " " for num in self.__rows[i]])
            printing = printing[:5] + " | " + printing[6:11] + " | " + printing[12:]
            print(printing)
            if i == 2 or i == 5:
                print("------|-------|------")

    @property
    def done(self):
        return self.__done

    @property
    def error(self):
        return self.__error
    
    @property
    def rows(self):
        return self.__rows
    
    @property
    def columns(self):
        return self.__columns()
    
    @property
    def squares(self):
        return self.__squares()

    @property
    def unknown(self):
        return self.__unknown

    @property
    def iterations(self):
        return self.__iterations