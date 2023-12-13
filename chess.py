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


    def find_piece(board, piece):
        for i in range(0, 8):
            for j in range(0, 8):
                if board[i, j] == piece:
                    return (j, i)
        return None

    def is_on_board(coordinates):
        (x, y) = coordinates
        return (x >= 0) and (x < 8) and (y >= 0) and (y < 8)

    def is_empty(board, coordinates):
        (x, y) = coordinates
        if not ChessGame.is_on_board(coordinates=coordinates):
            return False
        elif board[y, x] == b'0':
            return True
        else:
            return False

    def is_occupied_by_friend(board, coordinates, white):
        (x, y) = coordinates
        if not ChessGame.is_on_board(coordinates=coordinates):
            return False
        elif (white == True) and (board[y, x] in (b'K', b'Q', b'B', b'N', b'R', b'P')):
            return True
        elif (white == False) and (board[y, x] in (b'k', b'q', b'b', b'n', b'r', b'p')):
            return True
        else:
            return False

    def is_occupied_by_enemy(board, coordinates, white):
        (x, y) = coordinates
        if not ChessGame.is_on_board(coordinates=coordinates):
            return False
        elif (white == False) and (board[y, x] in (b'K', b'Q', b'B', b'N', b'R', b'P')):
            return True
        elif (white == True) and (board[y, x] in (b'k', b'q', b'b', b'n', b'r', b'p')):
            return True
        else:
            return False

    def direction_movements(board, coordinates, direction, white):
        (x, y) = coordinates
        (dx, dy) = direction
        move_list = []
        x += dx
        y += dy
        while ChessGame.is_on_board((x, y)):
            move = (x, y)
            if ChessGame.is_empty(board, move):
                move_list.append(move)
            elif ChessGame.is_occupied_by_friend(board, move, white):
                break
            elif ChessGame.is_occupied_by_enemy(board, move, white):
                move_list.append(move)
                break
            x += dx
            y += dy
        return move_list

    def bishop_movements(board, coordinates, white):
        move_list = []
        move_list.extend(ChessGame.direction_movements(board, coordinates, (1, 1), white))
        move_list.extend(ChessGame.direction_movements(board, coordinates, (1, -1), white))
        move_list.extend(ChessGame.direction_movements(board, coordinates, (-1, 1), white))
        move_list.extend(ChessGame.direction_movements(board, coordinates, (-1, -1), white))
        return move_list

    def rook_movements(board, coordinates, white):
        move_list = []
        move_list.extend(ChessGame.direction_movements(board, coordinates, (0, 1), white))
        move_list.extend(ChessGame.direction_movements(board, coordinates, (0, -1), white))
        move_list.extend(ChessGame.direction_movements(board, coordinates, (1, 0), white))
        move_list.extend(ChessGame.direction_movements(board, coordinates, (-1, 0), white))
        return move_list

    def queen_movements(board, coordinates, white):
        move_list = []
        move_list.extend(ChessGame.bishop_movements(board, coordinates, white))
        move_list.extend(ChessGame.rook_movements(board, coordinates, white))
        return move_list
    
    def horse_movements(board, coordinates, white):
        (x, y) = coordinates
        move_list = []

        unrestricted_moves = [
            (x + 1, y + 2),
            (x + 2, y + 1),
            (x + 2, y - 1),
            (x + 1, y - 2),
            (x - 1, y - 2),
            (x - 2, y - 1),
            (x - 2, y + 1),
            (x - 1, y + 2)
        ]

        for move in unrestricted_moves:
            if ChessGame.is_on_board(move) and not ChessGame.is_occupied_by_friend(board, move, white):
                move_list.append(move)

        return move_list
    
    def pawn_movements(board, coordinates, white=True):
        (x, y) = coordinates
        move_list = []

        if white:
            d = 1
        else:
            d = -1

        move = (x, y + d)
        if ChessGame.is_empty(board, move):
            move_list.append(move)
        move = (x, y + 2*d)
        if white == True and y == 1 and ChessGame.is_empty(board, move):
            move_list.append(move)
        elif white == False and y == 6 and ChessGame.is_empty(board, move):
            move_list.append(move)
        move = (x - 1, y + d)
        if ChessGame.is_occupied_by_enemy(board, move, white):
            move_list.append(move)
        move = (x + 1, y + d)
        if ChessGame.is_occupied_by_enemy(board, move, white):
            move_list.append(move)

        return move_list
    
    def king_movements(board, coordinates, white=True):
        (x, y) = coordinates
        move_list = []

        unrestricted_moves = [
            (x + 1, y),
            (x + 1, y - 1),
            (x, y - 1),
            (x - 1, y - 1),
            (x - 1, y),
            (x - 1, y + 1),
            (x, y + 1),
            (x + 1, y + 1)
        ]

        for move in unrestricted_moves:
            if ChessGame.is_on_board(move) and not ChessGame.is_occupied_by_friend(board, move, white):
                move_list.append(move)

        return move_list

    def is_atacked(board, coordinates, white):
        atacked = 0

        for move in ChessGame.pawn_movements(board, coordinates, white):
            (hx, hy) = move
            if white == True and board[hy, hx] == b'p':
                atacked += 1
            elif white == False and board[hy, hx] == b'P':
                atacked += 1

        for move in ChessGame.king_movements(board, coordinates, white):
            (hx, hy) = move
            if white == True and board[hy, hx] == b'k':
                atacked += 1
            elif white == False and board[hy, hx] == b'K':
                atacked += 1

        for move in ChessGame.bishop_movements(board, coordinates, white):
            (hx, hy) = move
            if white == True and board[hy, hx] in (b'q', b'b'):
                atacked += 1
            elif white == False and board[hy, hx] in (b'Q', b'B'):
                atacked += 1

        for move in ChessGame.rook_movements(board, coordinates, white):
            (hx, hy) = move
            if white == True and board[hy, hx] in (b'q', b'r'):
                atacked += 1
            elif white == False and board[hy, hx] in (b'Q', b'R'):
                atacked += 1

        for move in ChessGame.horse_movements(board, coordinates, white):
            (hx, hy) = move
            if white == True and board[hy, hx] == b'n':
                atacked += 1
            elif white == False and board[hy, hx] == b'N':
                atacked += 1

        return atacked

    def is_in_check(self, board, white):
        if white == True:
            king_coordinates = ChessGame.find_piece(board, b'K')
        else:
            king_coordinates = ChessGame.find_piece(board, b'k')
        print(f'king_coordinates : {king_coordinates}')
        king_is_atacked = ChessGame.is_atacked(board, king_coordinates, white)
        print(f'king_is_atacked : {king_is_atacked}')
        return king_is_atacked > 0


