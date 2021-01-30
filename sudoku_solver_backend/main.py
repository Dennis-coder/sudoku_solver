import math
import datetime
from sudoku import Sudoku

sudokuStr = open("sudoku.txt").read()
sudoku = Sudoku(sudokuStr)
sudoku.solve()

sudoku.print()
print(sudoku.correct())

# print("Rows:")
# for row in sudoku.rows:
#     print(row)

# print("Columns:")
# for column in sudoku.columns:
#     print(column)

# print("Squares:")
# for square in sudoku.squares:
#     print(square)

# if isinstance(sudoku.error, Exception):
#     print(sudoku.error)
#     print("Make sure the soduku is correct")