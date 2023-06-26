import chess
class ChessEngine:

    def __init__(self):
        self.piece_values = {'P': 100, 'N': 280, 'B': 320, 'R': 479, 'Q': 929, 'K': 60000}
        self.pst = {
            'P': [
                [0,  0,  0,  0,  0,  0,  0,  0],
                [-6,  2,  3,  4,  4,  3,  2, -6],
                [-6,  2,  8, 12, 12,  8,  2, -6],
                [-6,  4, 12, 16, 16, 12,  4, -6],
                [-6,  6, 18, 24, 24, 18,  6, -6],
                [-6,  8, 24, 32, 32, 24,  8, -6],
                [-6, 12, 36, 48, 48, 36, 12, -6],
                [0,  0,  0,  0,  0,  0,  0,  0]
            ],
            'N': [  
                [-50, -40, -30, -30, -30, -30, -40, -50],
                [-40, -20,   0,   0,   0,   0, -20, -40],
                [-30,   0,  10,  15,  15,  10,   0, -30],
                [-30,   5,  15,  20,  20,  15,   5, -30],
                [-30,   0,  15,  20,  20,  15,   0, -30],
                [-30,   5,  10,  15,  15,  10,   5, -30],
                [-40, -20,   0,   5,   5,   0, -20, -40],
                [-50, -40, -30, -30, -30, -30, -40, -50]
            ],
            'B': [
                [-20, -10, -10, -10, -10, -10, -10, -20],
                [-10,   0,   0,   0,   0,   0,   0, -10],
                [-10,   0,   5,  10,  10,   5,   0, -10],
                [-10,   5,   5,  10,  10,   5,   5, -10],
                [-10,   0,  10,  10,  10,  10,   0, -10],
                [-10,  10,  10,  10,  10,  10,  10, -10],
                [-10,   5,   0,   0,   0,   0,   5, -10],
                [-20, -10, -10, -10, -10, -10, -10, -20]
            ],
            'R': [
                [0,  0,  0,  5,  5,  0,  0,  0],
                [-5,  0,  0,  0,  0,  0,  0, -5],
                [-5,  0,  0,  0,  0,  0,  0, -5],
                [-5,  0,  0,  0,  0,  0,  0, -5],
                [-5,  0,  0,  0,  0,  0,  0, -5],
                [-5,  0,  0,  0,  0,  0,  0, -5],
                [5, 10, 10, 10, 10, 10, 10,  5],
                [0,  0,  0,  0,  0,  0,  0,  0]
            ],
            'Q': [
                [-20, -10, -10, -5, -5, -10, -10, -20],
                [-10,   0,   0,  0,  0,   0,   0, -10],
                [-10,   0,   5,  5,  5,   5,   0, -10],
                [-5,   0,   5,  5,  5,   5,   0,  -5],
                [0,   0,   5,  5,  5,   5,   0,  -5],
                [-10,   5,   5,  5,  5,   5,   0, -10],
                [-10,   0,   5,  0,  0,   0,   0, -10],
                [-20, -10, -10, -5, -5, -10, -10, -20]
            ],
            'K': [
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-20, -30, -30, -40, -40, -30, -30, -20],
                [-10, -20, -20, -20, -20, -20, -20, -10],
                [20,  20,   0,   0,   0,   0,  20,  20],
                [20,  30,  10,   0,   0,  10,  30,  20]
            ]
        }
        self.pst_b = {piece: [row[::-1] for row in self.pst[piece]] for piece in self.pst}
        self.board = chess.Board()
        self.game_over = False
        self.turn = 'w'
        self.winner = None
        self.orientation = 'white'

    def invert(self, orientation):
        if(orientation == 'black'):
            self.orientation = 'black'
            self.make_move(self.get_best_move(1))
        if(orientation == 'white'):
            self.orientation = 'white'
    
    def reset(self):
        if(self.orientation == 'black'):
            self.make_move(self.get_best_move(1))
        self.board.reset()
        self.game_over = False
        self.turn = 'w'
        self.winner = None

    def minimax(self, depth, alpha, beta, isMaximizingPlayer, board=None):
        if(board is None):
            board = self.board.copy()

        if(depth == 0):
            return self.evaluate(board)

        if(isMaximizingPlayer):
            maxEval = -99999
            moves = self.get_ordered_moves(board)
            for move in moves:
                board.push(chess.Move.from_uci(move))
                value = self.minimax(depth - 1, alpha, beta, False, board)
                board.pop()
                maxEval = max(maxEval,value)
                alpha = max(alpha,value)
                if beta <= alpha:
                    return maxEval
            return maxEval
        
        else:
            minEval = 99999
            moves = self.get_ordered_moves(board)
            for move in moves:
                board.push(chess.Move.from_uci(move))
                value = self.minimax(depth - 1, alpha, beta, True, board)
                board.pop()
                minEval = min(minEval,value)
                beta = min(beta,value)
                if beta <= alpha:
                    return minEval
            return minEval

    def evaluate(self, board):
        white_material = self.count_material(chess.WHITE,board)
        black_material = self.count_material(chess.BLACK,board)
        pst_evaluation = self.calculate_pst_evaluation(chess.WHITE, board) - self.calculate_pst_evaluation(chess.BLACK, board)
        evaluation = white_material - black_material + pst_evaluation
        perspective = 1 if self.turn == 'w' else -1
        return perspective * evaluation
    
    def count_material(self, color, board):
        material = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                if piece.color == color:
                    material += self.piece_values[piece.symbol().upper()]
                else:
                    material -= self.piece_values[piece.symbol().upper()]
        return material
    
    def calculate_pst_evaluation(self, color, board):
        pst_evaluation = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                if piece.color == color:
                    rank = chess.square_rank(square)
                    file = chess.square_file(square)
                    pst_evaluation += self.pst[piece.symbol().upper()][rank][file]
                else:
                    rank = chess.square_rank(square)
                    file = chess.square_file(square)
                    pst_evaluation -= self.pst_b[piece.symbol().upper()][rank][file]
        return pst_evaluation
    
    def make_move(self, move):
        try:
            if self.game_over:
                return False
            
            if (move == None):
                return False

            if (move + 'q') in self.get_valid_moves(self.board):
                move = move + 'q'

            if move not in self.get_valid_moves(self.board):
                print('[!] Invalid move - ' + move)
                return False
            
            self.board.push(chess.Move.from_uci(move))

            if self.board.is_game_over():
                self.game_over = True
                if self.board.is_checkmate():
                    self.winner = 'w' if self.turn == 'b' else 'b'
                else:
                    self.winner = 'draw'
            self.turn = 'w' if self.turn == 'b' else 'b'
            return self.get_game_state()

        except Exception as e:
            self.board.pop()
            print('[!] Error making move - ' + move)
            print('[!] BEGIN ERROR MESSAGE')
            print(e)
            print('[!] END ERROR MESSAGE')

    #Getters
    
    def get_best_move(self,depth):
        try:
            board = chess.Board(self.get_game_state())
            board.turn = True if self.turn == 'w' else False
            bestMove = None
            bestValue = -99999
            alpha = -99999
            beta = 99999
            moves = self.get_ordered_moves(board)
            for move in moves:
                board.push(chess.Move.from_uci(move))
                value = self.minimax(depth-1,alpha,beta,False,board)
                board.pop()
                if value > bestValue:
                    bestValue = value
                    bestMove = move
            return bestMove
        except Exception as e:
            print('[!] Error getting best move')
            print('[!] BEGIN ERROR MESSAGE')
            print(e)
            print('[!] END ERROR MESSAGE')

    def get_game_state(self):
        return self.board.fen()
    
    def get_valid_moves(self, board):
        return [str(move) for move in board.legal_moves]

    def get_ordered_moves(self,board):
        moves = self.get_valid_moves(board)
        ordered_moves = sorted(
            moves,
            key=lambda move: (
                -self.get_captured_piece_value(move),
                self.get_attacker_piece_value(move)
            )
        )
        return ordered_moves

    def get_captured_piece_value(self, move):
        captured_square = chess.Move.from_uci(move).to_square
        captured_piece = self.board.piece_at(captured_square)
        if captured_piece is None:
            return 0
        return captured_piece.piece_type

    def get_attacker_piece_value(self, move):
        from_square = chess.Move.from_uci(move).from_square
        attacker_piece = self.board.piece_at(from_square)
        if attacker_piece is None:
            return 0
        return -attacker_piece.piece_type
