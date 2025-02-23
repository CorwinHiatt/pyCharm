from flask import Flask, render_template, request, jsonify, session
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for session management

# Original quotes list
quotes = [
    "I'm not lazy, I'm in energy saving mode.",
    "Life is short. Smile while you still have teeth.",
    "I don't need Google, my wife knows everything!",
    "Why don't scientists trust atoms? Because they make up everything!",
    "I used to think I was indecisive. But now I'm not so sure.",
    "Don't worry if plan A fails, there are 25 more letters in the alphabet.",
]


# Tic Tac Toe game state
class TicTacToe:
    def __init__(self):
        self.board = ['' for _ in range(9)]
        self.current_player = 'X'

    def make_move(self, position):
        if self.board[position] == '':
            self.board[position] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def check_winner(self):
        # Winning combinations
        wins = [(0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
                (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
                (0, 4, 8), (2, 4, 6)]  # Diagonals

        for w in wins:
            if self.board[w[0]] == self.board[w[1]] == self.board[w[2]] != '':
                return self.board[w[0]]
        if '' not in self.board:
            return 'Tie'
        return None


# Chat messages storage
chat_messages = []


# Routes
@app.route('/')
def home():
    return render_template('index.html',
                           quote=random.choice(quotes),
                           current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


@app.route('/tictactoe')
def tictactoe():
    # Initialize new game
    game = TicTacToe()
    session['board'] = game.board
    session['current_player'] = game.current_player
    return render_template('tictactoe.html', board=game.board)


@app.route('/make_move/<int:position>', methods=['POST'])
def make_move(position):
    game = TicTacToe()
    game.board = session.get('board', ['' for _ in range(9)])
    game.current_player = session.get('current_player', 'X')

    if game.make_move(position):
        session['board'] = game.board
        session['current_player'] = game.current_player
        winner = game.check_winner()
        return jsonify({
            'board': game.board,
            'current_player': game.current_player,
            'winner': winner
        })
    return jsonify({'error': 'Invalid move'}), 400


@app.route('/chat')
def chat():
    return render_template('chat.html', messages=chat_messages)


@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form.get('message')
    if message:
        timestamp = datetime.now().strftime("%H:%M:%S")
        chat_messages.append({'text': message, 'time': timestamp})
        if len(chat_messages) > 10:  # Keep only last 10 messages
            chat_messages.pop(0)
    return jsonify({'messages': chat_messages})


@app.route('/counter')
def counter():
    count = session.get('count', 0)
    session['count'] = count + 1
    return render_template('counter.html', count=session['count'])


if __name__ == '__main__':
    app.run(debug=True)
