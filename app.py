from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

# Constants for players
X = 1   # Human
O = -1  # AI

def minimax(board, depth, is_maximizing):
    if check_winner(board) == O:
        return 10 - depth
    elif check_winner(board) == X:
        return depth - 10
    elif is_board_full(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == 0:
                board[i] = O
                score = minimax(board, depth + 1, False)
                board[i] = 0
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == 0:
                board[i] = X
                score = minimax(board, depth + 1, True)
                board[i] = 0
                best_score = min(score, best_score)
        return best_score

def find_best_move(board):
    best_score = -math.inf
    move = -1
    for i in range(9):
        if board[i] == 0:
            board[i] = O
            score = minimax(board, 0, False)
            board[i] = 0
            if score > best_score:
                best_score = score
                move = i
    print(f"AI is making move at position: {move}")  # Debugging line
    return move

def check_winner(board):
    # Check rows, columns, and diagonals for a winner
    for i in range(3):
        if abs(sum(board[i * 3:(i + 1) * 3])) == 3:
            return O if board[i * 3] == O else X
    
    for i in range(3):
        if abs(sum(board[i::3])) == 3:
            return O if board[i] == O else X
    
    if abs(sum([board[0], board[4], board[8]])) == 3:
        return O if board[0] == O else X
    if abs(sum([board[2], board[4], board[6]])) == 3:
        return O if board[2] == O else X
    
    return None

def is_board_full(board):
    return all(x != 0 for x in board)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    data = request.json
    human_move = data['move']
    board = data['board']
    
    board[human_move] = X  # Human move
    
    # Check for winner or full board after human move
    if check_winner(board) or is_board_full(board):
        return jsonify({"board": board, "winner": check_winner(board)})

    # AI makes its move
    ai_move = find_best_move(board)
    if ai_move != -1:  # Ensure AI has a valid move
        board[ai_move] = O
    
    winner = check_winner(board)
    
    return jsonify({"board": board, "winner": winner})

if __name__ == '__main__':
    app.run(debug=True)