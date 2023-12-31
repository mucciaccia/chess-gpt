import numpy as np
import torch
from chess import ChessGame
from chess_position import ChessPosition
from evaluator_MLP import MLPChessEvaluator
from evaluator_CNN import CNNChessEvaluator
from eval_reader import EvalReader

class ChessEngine:

    def __init__(self, model_path, oponent):
        self.model = torch.load(model_path)
        self.oponent = oponent
        self.eval = EvalReader()

    def evaluate(self, position: ChessPosition):
        fen_str = position.to_FEN_notation_2()
        tensor = EvalReader.fen_to_tensor(fen_str)
        if self.oponent == 2:
            tensor = tensor.reshape(768)
        if self.oponent == 3:
            tensor = tensor.permute(2, 0, 1).unsqueeze(dim=0)
        evaluation = self.model(tensor)
        return evaluation

    def rmini(self, position : ChessPosition, depth : int):
        if depth > 0:
            min = 2000
            for move in ChessGame.possible_moves(position):
                (a, b) = move
                new_position = position.unrestricted_move(a, b)
                new_position.white_turn = not new_position.white_turn
                points = self.rmax(new_position, depth - 1)
                if points < min:
                    min = points
            return min
        else:
            return self.evaluate(position)

    def rmax(self, position : ChessPosition, depth : int):
        if depth > 0:
            max = 0
            for move in ChessGame.possible_moves(position):
                (a, b) = move
                new_position = position.unrestricted_move(a, b)
                new_position.white_turn = not new_position.white_turn
                points = self.rmini(new_position, depth - 1)
                if points > max:
                    max = points
            return max
        else:
            return self.evaluate(position)
        
    def white_best_move(self, position : ChessPosition, depth : int):
        best_move = None
        max = 0
        for move in ChessGame.possible_moves(position):
            (a, b) = move
            new_position = position.unrestricted_move(a, b)
            new_position.white_turn = not new_position.white_turn
            points = self.rmax(new_position, depth - 1)
            if points > max:
                max = points
                best_move = move
        return best_move
    
    def black_best_move(self, position : ChessPosition, depth : int):
        best_move = None
        max = 0
        for move in ChessGame.possible_moves(position):
            (a, b) = move
            new_position = position.unrestricted_move(a, b)
            new_position.white_turn = not new_position.white_turn
            points = self.rmini(new_position, depth - 1)
            if points > max:
                max = points
                best_move = move
        return best_move
