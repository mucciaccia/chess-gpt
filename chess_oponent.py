import numpy as np
from chess_position import ChessPosition
from gpt_api import GptApi
from chess import ChessGame
from chess_engine import ChessEngine

class ChessOponent:

    def __init__(self) -> None:
        self.player_white = False
        self.engine = ChessEngine()

    def mlp_move(self, chessGame : ChessGame):
        (a, b) = self.engine.white_best_move(chessGame.position, 1)
        board = chessGame.player_move(a, b)    
        return board
        
    def cnn_move(self, chessGame : ChessGame):
        (a, b) = self.engine.white_best_move(chessGame.position, 1)
        board = chessGame.player_move(a, b)    
        return board

    def gpt_move(self, chessGame : ChessGame):
        (a, b) = self.engine.white_best_move(chessGame.position, 1)
        board = chessGame.player_move(a, b)    
        return board

