from sudoku import Sudoku
import time
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/<sudoku_str>')
def solve(sudoku_str):
    start = time.perf_counter()
    sudoku_str = sudoku_str.replace("x", "\n")
    if sudoku_str[-1:] == ",":
        sudoku_str += " "
    sudoku = Sudoku(sudoku_str)
    sudoku.solve()
    end = time.perf_counter()
    return jsonify({"state": sudoku.correct(), "sudoku": sudoku.rows, "time": (end - start)})