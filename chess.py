import numpy as np



class ChessGame:

    player = 1

    def __init__(self, board) -> None:      
        self.board = board
        self.white_playing = False
        self.white_turn = True

    def is_valid_move(self, a, b):
        a_x, a_y = a
        b_x, b_y = b
        print(f'Move ({a_x},{a_y}){self.board[a_y, a_x]} ({b_x},{b_y}){self.board[b_y, b_x]}')

        is_empty_square = (self.board[b_y, b_x] == b'0')

        is_valid = True

        if (a_x, a_y) == (b_x, b_y):
            is_valid = False

        if b_x == a_x or b_y == a_y:
            is_straight = True
        else:
            is_straight = False

        if abs(b_x - a_x) == abs(b_y - a_y):
            is_diagonal = True
        else:
            is_diagonal = False

        if (b_x == a_x - 1 or b_x == a_x + 1) and (b_y == a_y - 2 or b_y == a_y + 2):
            is_L = True
        elif (b_x == a_x - 2 or b_x == a_x + 2) and (b_y == a_y - 1 or b_y == a_y + 1):
            is_L = True
        else:
            is_L = False

        if abs(b_x - a_x) == 1 and abs(b_y - a_y) == 1:
            is_adjoining = True
        elif abs(b_x - a_x) == 1 and abs(b_y - a_y) == 0:
            is_adjoining = True
        elif abs(b_x - a_x) == 0 and abs(b_y - a_y) == 1:
            is_adjoining = True
        else:
            is_adjoining = False

        if self.white_playing and self.white_turn and (b_y - a_y) < 0:
            is_forward = True
        elif not self.white_playing and not self.white_turn and (b_y - a_y) < 0:
            is_forward = True
        elif self.white_playing and not self.white_turn and (b_y - a_y) > 0:
            is_forward = True
        elif not self.white_playing and self.white_turn and (b_y - a_y) > 0:
            is_forward = True
        else:
            is_forward = False

        if a_y == 6 and b_y == 4:
            is_double = True
        elif a_y == 1 and b_y == 3:
            is_double = True
        else:
            is_double = False

        # Check if there are any pieces in the middle
        if is_straight or is_diagonal:
            d_x = 0
            d_y = 0
            if b_x != a_x:
                d_x = (b_x - a_x) // abs(b_x - a_x)
                d_n = abs(b_x - a_x)
            if b_y != a_y:    
                d_y = (b_y - a_y) // abs(b_y - a_y)
                d_n = abs(b_y - a_y)
            for i in range(1, d_n):
                if self.board[a_y + i*d_y, a_x + i*d_x] != b'0':
                    return False

        piece = self.board[a_y, a_x]

        if self.white_turn == True and piece in [b'p', b'q', b'k', b'b', b'n', b'r']:
            is_valid = False

        if self.white_turn == False and piece in [b'P', b'Q', b'K', b'B', b'N', b'R']:
            is_valid = False

        if self.white_turn == True and self.board[b_y, b_x] in [b'P', b'Q', b'K', b'B', b'N', b'R']:
            is_valid = False

        if self.white_turn == False and self.board[b_y, b_x] in [b'p', b'q', b'k', b'b', b'n', b'r']:
            is_valid = False

        if piece in [b'p', b'P']:
            if not is_adjoining and not is_double:
                is_valid = False
            if not is_forward:
                is_valid = False
            if is_diagonal and is_empty_square:
                is_valid = False
            if is_straight and not is_empty_square:
                is_valid = False

        if piece in [b'k', b'K']:
            if not is_adjoining:
                is_valid = False

        if piece in [b'q', b'Q']:
            if not is_straight and not is_diagonal:
                is_valid = False

        if piece in [b'r', b'R']:
            if not is_straight:
                is_valid = False

        if piece in [b'b', b'B']:
            if not is_diagonal:
                is_valid = False

        if piece in [b'n', b'N']:
            if not is_L:
                is_valid = False

        return is_valid



