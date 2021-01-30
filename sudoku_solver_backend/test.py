import math
import time
from sudoku import Sudoku

def run_test(file, iterations):
    sudoku_strs = open("tests/" + file + ".txt").read().split("\n\n")
    sudokus = []

    start = time.perf_counter()
    for _ in range(iterations):
        for sudoku_str in sudoku_strs:
            sudokus.append(Sudoku(sudoku_str))
    end = time.perf_counter()

    print("Initialization")
    print("Time:     ", (end - start), "seconds")
    print("Avg. time:", ((end - start) / (iterations * len(sudokus)) * 1000000), "nanoseconds")

    start = time.perf_counter()
    for sudoku in sudokus:
        sudoku.solve()
    end = time.perf_counter()

    print("Solving")
    print("Time:     ", (end - start), "seconds")
    print("Avg. time:", ((end - start) / (iterations * len(sudokus)) * 1000000), "nanoseconds")

    start = time.perf_counter()
    for sudoku in sudokus:
        if sudoku.correct() != "Correct!":
            sudoku.print()
            raise Exception("Incorrect sudoku")
    end = time.perf_counter()

    print("Correction")
    print("Time:     ", (end - start), "seconds")
    print("Avg. time:", ((end - start) / (iterations * len(sudokus)) * 1000000), "nanoseconds")

iterations = 20

print("5 easy sudokus running " + str(iterations) + " times")
run_test("easy_sudokus", iterations)
print("")

print("5 medium sudokus running " + str(iterations) + " times")
run_test("medium_sudokus", iterations)
print("")

print("5 hard sudokus running " + str(iterations) + " times")
run_test("hard_sudokus", iterations)
print("")

print("5 expert sudokus running " + str(iterations) + " times")
run_test("expert_sudokus", iterations)
print("")