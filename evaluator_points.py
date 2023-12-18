import numpy as np
from chess import ChessGame
from chess_position import ChessPosition

class PointEvaluator:

    def evaluate(position : ChessPosition):
        board = position.board
        evaluation = 0
        for i in range(0, 8):
            for j in range(0, 8):
                if board[i, j] == b'K':
                    evaluation += 1000
                elif board[i, j] == b'Q':
                    evaluation += 9
                elif board[i, j] == b'R':
                    evaluation += 5
                elif board[i, j] == b'B':
                    evaluation += 3
                elif board[i, j] == b'N':
                    evaluation += 3
                elif board[i, j] == b'P':
                    evaluation += 1
                elif board[i, j] == b'k':
                    evaluation -= 1000
                elif board[i, j] == b'q':
                    evaluation -= 9
                elif board[i, j] == b'r':
                    evaluation -= 5
                elif board[i, j] == b'b':
                    evaluation -= 3
                elif board[i, j] == b'n':
                    evaluation -= 3
                elif board[i, j] == b'p':
                    evaluation -= 1
        return evaluation

    def rmini(position : ChessPosition, depth : int):
        if depth > 0:
            min = 2000
            for move in ChessGame.possible_moves(position):
                (a, b) = move
                new_position = position.unrestricted_move(a, b)
                new_position.white_turn = not new_position.white_turn
                points = PointEvaluator.rmax(new_position, depth - 1)
                if points < min:
                    min = points
            return min
        else:
            return PointEvaluator.evaluate(position)

    def rmax(position : ChessPosition, depth : int):
        if depth > 0:
            max = 0
            for move in ChessGame.possible_moves(position):
                (a, b) = move
                new_position = position.unrestricted_move(a, b)
                new_position.white_turn = not new_position.white_turn
                points = PointEvaluator.rmini(new_position, depth - 1)
                if points > max:
                    max = points
            return max
        else:
            return PointEvaluator.evaluate(position)
        
    def white_best_move(position : ChessPosition, depth : int):
        best_move = None
        max = 0
        for move in ChessGame.possible_moves(position):
            (a, b) = move
            new_position = position.unrestricted_move(a, b)
            new_position.white_turn = not new_position.white_turn
            points = PointEvaluator.rmax(new_position, depth - 1)
            if points > max:
                max = points
                best_move = move
        return best_move

board = np.matrix([
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
], dtype=np.character)

chessPosition = ChessPosition()
chessPosition.board = board

eva = PointEvaluator.white_best_move(chessPosition, 4)

print(eva)