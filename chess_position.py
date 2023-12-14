import numpy as np
import copy

class ChessPosition:

    def __init__(self) -> None:
        self.board = np.matrix([
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        ], dtype=np.character)
        self.white_turn = True
        self.white_kingside_castling = True
        self.white_queenside_castling = True
        self.black_kingside_castling = True
        self.black_queenside_castling = True
        self.en_passant = []

    def copy(self):
        return copy.deepcopy(self)

    def get_board(self):
        return self.board

    def is_on_board(self, coordinates):
        (x, y) = coordinates
        return (x >= 0) and (x < 8) and (y >= 0) and (y < 8)

    def get_piece(self, coordinates):
        x, y = coordinates
        if self.is_on_board(coordinates):
            return self.board[y, x]
        else:
            return None

    def set_piece(self, coordinates, piece):
        x, y = coordinates
        self.board[y, x] = piece
        return

    def find_piece(self, piece):
        for i in range(0, 8):
            for j in range(0, 8):
                if self.board[i, j] == piece:
                    return (j, i)
        return None

    def is_empty(self, coordinates):
        if not self.is_on_board(coordinates):
            return False
        elif self.get_piece(coordinates) == b'0':
            return True
        else:
            return False

    def is_occupied_by_friend(self, coordinates, white):
        (x, y) = coordinates
        if not self.is_on_board(coordinates=coordinates):
            return False
        elif (white == True) and (self.board[y, x] in (b'K', b'Q', b'B', b'N', b'R', b'P')):
            return True
        elif (white == False) and (self.board[y, x] in (b'k', b'q', b'b', b'n', b'r', b'p')):
            return True
        else:
            return False

    def is_occupied_by_enemy(self, coordinates, white):
        (x, y) = coordinates
        if not self.is_on_board(coordinates=coordinates):
            return False
        elif (white == False) and (self.board[y, x] in (b'K', b'Q', b'B', b'N', b'R', b'P')):
            return True
        elif (white == True) and (self.board[y, x] in (b'k', b'q', b'b', b'n', b'r', b'p')):
            return True
        else:
            return False
  
    def is_white(piece):
        if (piece in [b'K', b'Q', b'R', b'B', b'N', b'P']):
            return True
        else:
            return False

    def is_black(piece):
        if (piece in [b'k', b'q', b'r', b'b', b'n', b'p']):
            return True
        else:
            return False
        
    def unrestricted_move(self, a, b):
        a_x, a_y = a
        b_x, b_y = b

        copy_position = copy.deepcopy(self)
        piece = copy_position.get_piece(a)
        copy_position.board[a_y, a_x] = b'0'
        copy_position.board[b_y, b_x] = piece
        return copy_position

    def info(self):
        info = ''
        if self.white_turn == True:
            info += 'White plays! / '
        else:
            info += 'Black plays! / '
        
        info += 'Castling: '
        if self.white_kingside_castling == True:
            info += 'K'
        else:
            info += '-'
        if self.white_queenside_castling == True:
            info += 'Q'
        else:
            info += '-'
        if self.black_kingside_castling == True:
            info += 'k'
        else:
            info += '-'
        if self.black_queenside_castling == True:
            info += 'q'
        else:
            info += '-'
        info += ' / En passant: '
        info += str(self.en_passant)
        return info