from chess import ChessGame
import numpy as np

board = np.matrix([
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0'],
    ['p', 'p', 'p', 'p', '0', 'p', '0', 'p'],
    ['r', 'n', 'b', 'q', '0', 'b', 'n', 'r']
], dtype=np.character)


print(board.shape)

chessGame = ChessGame()
chessGame.board = board

in_check = chessGame.is_in_check_mate(white=True)

print(in_check)