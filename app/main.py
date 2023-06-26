from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send

import chessEngine

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('chess.html')

chess = chessEngine.ChessEngine()

@socketio.on('connect')
def handle_connect():
    emit('game_state', chess.get_game_state())

@socketio.on('speech')
def handle_speech(msg):
    move = msg["speech"].lower().replace(" ", "")
    result = chess.make_move(move)
    if(result == False):
        emit('game_state', chess.get_game_state())
        return
    emit('thinking', True)
    best_move = chess.get_best_move(int(msg['depth']))
    emit('thinking', False)
    result = chess.make_move(best_move)
    
    emit('game_state', result)

@socketio.on('move')
def handle_movement(data):
    move = data['source'] + data['target']
    result = chess.make_move(move)
    if(result == False):
        emit('game_state', chess.get_game_state())
        return
    emit('thinking', True)
    best_move = chess.get_best_move(int(data['depth']))
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