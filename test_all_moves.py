from chess import ChessGame
import numpy as np

board = np.matrix([
    ['R', 'N', 'B', 'Q', 'K', '0', '0', 'R'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0'],
    ['p', 'p', 'p', 'p', 'p', 'p', '0', 'p'],
    ['r', 'n', 'b', 'q', 'p', 'b', 'n', 'r']
], dtype=np.character)


chessGame = ChessGame()
chessGame.position.board = board
chessGame.position.white_turn = True

moves = ChessGame.possible_moves(chessGame.position)

for x in moves:
    a, b = x
    print(chessGame.to_long_algebraic_notation(a, b))