from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import chessEngine

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some super secret key!'
socketio = SocketIO(app, logger=True)
chess = chessEngine.ChessEngine()

@app.route('/')
def index():
    return render_template('jogar.html')

@app.route('/jogar')
def jogar():
    return render_template('chess.html')

@socketio.on('connect')
def handle_connect():
    emit('game_state', chess.get_game_state())

@socketio.on('speech')
def handle_speech(msg):
    move = msg["speech"].lower().replace(" ", "")
    process_move(move, int(msg.get('depth', 0)))

@socketio.on('move')
def handle_movement(data):
    move = data['source'] + data['target']
    process_move(move, int(data.get('depth', 0)))

def process_move(move, depth):
    result = chess.make_move(move)
    if not result:
        emit('game_state', chess.get_game_state())
        return

    emit('thinking', True)
    best_move = chess.get_best_move(depth)
    emit('thinking', False)
    
    result = chess.make_move(best_move)
    emit('game_state', result)

@socketio.on('invert')
def handle_invert(msg):
    chess.invert(msg['orientation'])
    emit('game_state', chess.get_game_state())

@socketio.on('reset')
def handle_reset():
    chess.reset()
    emit('game_state', chess.get_game_state())

if __name__ == '__main__':
    socketio.run(app)
