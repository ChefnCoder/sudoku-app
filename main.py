from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)


# Function to fetch a random Sudoku puzzle from the sudoku.com API
def fetch_random_sudoku():
    url = "https://sudoku-game-and-api.netlify.app/api/sudoku"
    response = requests.get(url)
    if response.status_code == 200:
        # Extract the 'easy' puzzle from the response
        puzzle = response.json()['easy']
        return puzzle
    else:
        # Fallback to a static puzzle if API fails
        return generate_sudoku()


# Static fallback Sudoku puzzle
def generate_sudoku():
    puzzle = [[5, 3, 0, 0, 7, 0, 0, 0, 0], [6, 0, 0, 1, 9, 5, 0, 0, 0],
              [0, 9, 8, 0, 0, 0, 0, 6, 0], [8, 0, 0, 0, 6, 0, 0, 0, 3],
              [4, 0, 0, 8, 0, 3, 0, 0, 1], [7, 0, 0, 0, 2, 0, 0, 0, 6],
              [0, 6, 0, 0, 0, 0, 2, 8, 0], [0, 0, 0, 4, 1, 9, 0, 0, 5],
              [0, 0, 0, 0, 8, 0, 0, 7, 9]]
    return puzzle


# Function to check if placing a number is valid
def is_possible(board, sr, sc, val):
    for row in range(9):
        if board[row][sc] == val:
            return False
    for col in range(9):
        if board[sr][col] == val:
            return False
    r, c = sr - sr % 3, sc - sc % 3
    for cr in range(r, r + 3):
        for cc in range(c, c + 3):
            if board[cr][cc] == val:
                return False
    return True


# Recursive function to solve the Sudoku puzzle
def solve_sudoku_helper(board, sr, sc):
    if sr == 9:
        return True
    if sc == 9:
        return solve_sudoku_helper(board, sr + 1, 0)
    if board[sr][sc] != 0:
        return solve_sudoku_helper(board, sr, sc + 1)

    for i in range(1, 10):
        if is_possible(board, sr, sc, i):
            board[sr][sc] = i
            if solve_sudoku_helper(board, sr, sc + 1):
                return True
            board[sr][sc] = 0
    return False


# Function to initiate solving the Sudoku puzzle
def solve(board):
    solve_sudoku_helper(board, 0, 0)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sudoku', methods=['GET'])
def get_sudoku():
    board = fetch_random_sudoku()  # Use the API to fetch a random Sudoku
    return jsonify({"board": board})


@app.route('/solve', methods=['POST'])
def solve_sudoku():
    board = request.json['board']
    solve(board)
    return jsonify({"board": board})


if __name__ == '__main__':
    app.run(debug=True)
