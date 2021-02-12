import math
import time
from sudoku import Sudoku

start = time.perf_counter()
sudokuStr = open("sudoku.txt").read()
sudoku = Sudoku(sudokuStr)
sudoku.solve()

end = time.perf_counter()
print("time:", (end - start))

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