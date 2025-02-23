from flask import Flask, render_template
import random

app = Flask(__name__)

# List of fun quotes
quotes = [
    "I'm not lazy, I'm in energy saving mode.",
    "Life is short. Smile while you still have teeth.",
    "I don't need Google, my wife knows everything!",
    "Why don't scientists trust atoms? Because they make up everything!",
    "I used to think I was indecisive. But now I'm not so sure.",
    "Don't worry if plan A fails, there are 25 more letters in the alphabet.",
]

@app.route('/')
def home():
    return render_template('index.html', quote=random.choice(quotes))

if __name__ == '__main__':
    app.run(debug=True)
