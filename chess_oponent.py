import numpy as np
from chess_position import ChessPosition
from gpt_api import GptApi
from chess import ChessGame
from chess_engine import ChessEngine

class ChessOponent:

    def __init__(self, oponent) -> None:
        self.player_white = False
        self.oponent = oponent
        if oponent == 2:
            self.mlp_engine = ChessEngine('./models/MLP.torch', oponent)
        if oponent == 3:
            self.cnn_engine = ChessEngine('./models/CNN.torch', oponent)

    def oponent_move(self, chessGame : ChessGame):
        board = chessGame.position.board
        if self.oponent == 1:
            board = self.gpt_move(chessGame)
        elif self.oponent == 2:
            board = self.mlp_move(chessGame)
        elif self.oponent == 3:
            board = self.cnn_move(chessGame)
        return board

    def mlp_move(self, chessGame : ChessGame):
        if chessGame.player_white == False:
            (a, b) = self.mlp_engine.white_best_move(chessGame.position, 1)
        else:
            (a, b) = self.mlp_engine.black_best_move(chessGame.position, 1)
        board = chessGame.player_move(a, b)    
        return board
        
    def cnn_move(self, chessGame : ChessGame):
        if chessGame.player_white == False:
            (a, b) = self.cnn_engine.white_best_move(chessGame.position, 1)
        else:
            (a, b) = self.cnn_engine.black_best_move(chessGame.position, 1)
        board = chessGame.player_move(a, b)    
        return board

    def gpt_move(self, chessGame : ChessGame):
        fen_str = chessGame.position.to_FEN_notation()
        move_history_str = "\n".join(chessGame.move_history)
        possible_moves_str = ""
        possible_moves = ChessGame.possible_moves(chessGame.position)
        for move in possible_moves:
            a, b = move
            possible_moves_str += chessGame.to_long_algebraic_notation(a, b)
            possible_moves_str += "\n"

        valid = False
        attempts = 1
        while (valid == False) and (attempts > 0):
            move_text = GptApi.move(fen_str, move_history_str, possible_moves_str)
            (a, b) = chessGame.from_long_algebraic_notation(move_text)
            valid = chessGame.is_valid_move(a, b, promotion_piece='q')
            attempts -= 1
        if valid == True:
            chessGame.player_move(a, b)
        else:
            print('All Chat GPT attempts were invalid movements! A random movement will be chosen!')
            a, b = possible_moves[0]
            chessGame.player_move(a, b)
        return chessGame.position.board

