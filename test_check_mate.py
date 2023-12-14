from chess import ChessGame
import numpy as np

board = np.matrix([
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
    ['P', 'P', 'P', 'P', 'P', 'p', '0', 'P'],
    ['0', '0', '0', '0', '0', '0', 'p', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
], dtype=np.character)

chessGame = ChessGame()
chessGame.board = board

in_check_mate = ChessGame.is_in_check_mate(board, white=True)
print(f'in_check_mate: {in_check_mate}')