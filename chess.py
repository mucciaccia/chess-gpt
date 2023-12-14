import numpy as np


class ChessGame:

    def __init__(self) -> None:
        self.board = np.matrix([
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'p', 'P'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'P', 'p'],
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        ], dtype=np.character)
        self.move_number = 0
        self.white_turn = True
        self.white_kingside_castling = True
        self.white_queenside_castling = True
        self.black_kingside_castling = True
        self.black_queenside_castling = True
        self.en_passant = []
        self.history = [self.board]

    def get_board(self):
        return self.board

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
    
    def pawn_movements(board, coordinates, white):
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
    
    def king_movements(board, coordinates, white):
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

    def any_piece_movements(board, coordinates, white):
        x, y = coordinates
        piece = board[y, x]

        if white == True and ChessGame.is_white(piece) == False:
            return []
        if white == False and ChessGame.is_black(piece) == False:
            return []
        if (piece == b'K') or (piece == b'k'):
            return ChessGame.king_movements(board, coordinates, white)
        elif (piece == b'Q') or (piece == b'q'):
            return ChessGame.queen_movements(board, coordinates, white)
        elif (piece == b'R') or (piece == b'r'):
            return ChessGame.rook_movements(board, coordinates, white)
        elif (piece == b'B') or (piece == b'b'):
            return ChessGame.bishop_movements(board, coordinates, white)
        elif (piece == b'N') or (piece == b'n'):
            return ChessGame.horse_movements(board, coordinates, white)
        elif (piece == b'P') or (piece == b'p'):
            return ChessGame.pawn_movements(board, coordinates, white)
        else:
            return []

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

    def is_in_check(board, white):
        if white == True:
            king_coordinates = ChessGame.find_piece(board, b'K')
        else:
            king_coordinates = ChessGame.find_piece(board, b'k')
        king_is_atacked = ChessGame.is_atacked(board, king_coordinates, white)
        return (king_is_atacked > 0)
    
    def is_move_blocked_by_check(board, a, b, white):
        a_x, a_y = a
        b_x, b_y = b
        copy = np.copy(board)
        piece = copy[a_y, a_x]
        copy[a_y, a_x] = b'0'
        copy[b_y, b_x] = piece
        in_check = ChessGame.is_in_check(copy, white)
        return in_check

    def is_in_check_mate(board, white):
        if ChessGame.is_in_check(board, white) == False:
            return False
        for i in range(0, 8):
            for j in range(0, 8):
                coordinates = (i, j)
                moves = ChessGame.any_piece_movements(board, coordinates, white)
                for move in moves:
                    if ChessGame.is_move_blocked_by_check(board, coordinates, move, white) == False:
                        return False
        return True

    def is_castling(self, a, b):
        if a == (4, 0) and b == (0, 0):
            kingside = False
            white = True
        elif a == (4, 0) and b == (7, 0):
            kingside = True
            white = True
        elif a == (4, 7) and b == (0, 7):
            kingside = False
            white = False
        elif a == (4, 7) and b == (7, 7):
            kingside = True
            white = False
        else:
            return False

        board = self.board
        if (kingside == True) and (white == True) and (self.white_kingside_castling == True):
            return ChessGame.is_empty(board, (5, 0)) and ChessGame.is_empty(board, (6, 0))
        elif (kingside == False) and (white == True) and (self.white_queenside_castling == True):
            return ChessGame.is_empty(board, (1, 0)) and ChessGame.is_empty(board, (2, 0)) and ChessGame.is_empty(board, (3, 0))
        elif (kingside == True) and (white == False) and (self.black_kingside_castling == True):
            return ChessGame.is_empty(board, (5, 7)) and ChessGame.is_empty(board, (6, 7))
        elif (kingside == False) and (white == False) and (self.black_queenside_castling == True):
            return ChessGame.is_empty(board, (1, 7)) and ChessGame.is_empty(board, (2, 7)) and ChessGame.is_empty(board, (3, 7))
        else:
            return False
      
    def execute_castling(self, a, b):
        copy = np.copy(self.board)
        if a == (4, 0) and b == (0, 0):
            copy[0, 0] = b'0'
            copy[0, 1] = b'0'
            copy[0, 2] = b'K'
            copy[0, 3] = b'R'
            copy[0, 4] = b'0'
        elif a == (4, 0) and b == (7, 0):
            copy[0, 4] = b'0'
            copy[0, 5] = b'R'
            copy[0, 6] = b'K'
            copy[0, 7] = b'0'
        elif a == (4, 7) and b == (0, 7):
            copy[7, 0] = b'0'
            copy[7, 1] = b'0'
            copy[7, 2] = b'K'
            copy[7, 3] = b'R'
            copy[7, 4] = b'0'
        elif a == (4, 7) and b == (7, 7):
            copy[7, 4] = b'0'
            copy[7, 5] = b'R'
            copy[7, 6] = b'K'
            copy[7, 7] = b'0'
        return copy
    
    def update_castling(self, a):
        if a == (0, 0):
            self.white_queenside_castling = False
        elif a == (7, 0):
            self.white_kingside_castling = False
        elif a == (4, 0):
            self.white_kingside_castling = False
            self.white_queenside_castling = False
        elif a == (0, 7):
            self.black_queenside_castling = False
        elif a == (7, 7):
            self.black_kingside_castling = False
        elif a == (4, 7):
            self.black_kingside_castling = False
            self.black_queenside_castling = False
        return
    
    def is_en_passant(self, a, b):
        for x in self.en_passant:
            if (x['a'] == a) and (x['b'] == b):
                return True
        return False

    def update_en_passant(self, a, b):
        a_x, a_y = a
        b_x, b_y = b
        piece = self.board[b_y, b_x]
        if (a_y == 1) and (b_y == 3) and (piece == b'P') and (self.board[3, a_x - 1] == b'p'):
            self.en_passant.append({'a': (a_x - 1, 3), 'b': (a_x, 2), 'c': (b_x, b_y)})
        if (a_y == 1) and (b_y == 3) and (piece == b'P') and (self.board[3, a_x + 1] == b'p'):
            self.en_passant.append({'a': (a_x + 1, 3), 'b': (a_x, 2), 'c': (b_x, b_y)})
        if (a_y == 6) and (b_y == 4) and (piece == b'p') and (self.board[4, a_x - 1] == b'P'):
            self.en_passant.append({'a': (a_x - 1, 4), 'b': (a_x, 5), 'c': (b_x, b_y)})
        if (a_y == 6) and (b_y == 4) and (piece == b'p') and (self.board[4, a_x + 1] == b'P'):
            self.en_passant.append({'a': (a_x + 1, 4), 'b': (a_x, 5), 'c': (b_x, b_y)})
        return
    
    def is_promotion(self, a, b):
        a_x, a_y = a
        b_x, b_y = b
        piece = self.board[a_y, a_x]
        if (piece == b'P') and (b_y == 7):
            return True
        if (piece == b'p') and (b_y == 0):
            return True
        return False

    def execute_promotion(self, a, b, promotion_piece):
        a_x, a_y = a
        b_x, b_y = b
        piece = self.board[a_y, a_x]
        copy = np.copy(self.board)
        if (piece == b'P') and (b_y == 7):
            copy[a_y, a_x] = b'0'
            copy[b_y, b_x] = promotion_piece
        if (piece == b'p') and (b_y == 0):
            copy[a_y, a_x] = b'0'
            copy[b_y, b_x] = promotion_piece
        return copy

    def is_valid_move(self, a, b):
        board = self.board
        white_turn = self.white_turn
        a_x, a_y = a
        b_x, b_y = b

        piece = board[a_y, a_x]

        if ChessGame.is_empty(board, a):
            return False
        if (white_turn == True) and (piece in [b'k', b'q', b'r', b'b', b'n', b'p']):
            return False
        if (white_turn == False) and (piece in [b'K', b'Q', b'R', b'B', b'N', b'P']):
            return False

        if (piece == b'K') and (b not in ChessGame.king_movements(board, a, white=True)):
            if (self.is_castling(a, b) == False):
                return False
        if (piece == b'Q') and (b not in ChessGame.queen_movements(board, a, white=True)):
            return False
        if (piece == b'R') and (b not in ChessGame.rook_movements(board, a, white=True)):
            return False
        if (piece == b'B') and (b not in ChessGame.bishop_movements(board, a, white=True)):
            return False
        if (piece == b'N') and (b not in ChessGame.horse_movements(board, a, white=True)):
            return False
        if (piece == b'P') and (b not in ChessGame.pawn_movements(board, a, white=True)):
            if (self.is_en_passant(a, b) == False):
                return False

        if (piece == b'k') and (b not in ChessGame.king_movements(board, a, white=False)):
            if (self.is_castling(a, b) == False):
                return False
        if (piece == b'q') and (b not in ChessGame.queen_movements(board, a, white=False)):
            return False
        if (piece == b'r') and (b not in ChessGame.rook_movements(board, a, white=False)):
            return False
        if (piece == b'b') and (b not in ChessGame.bishop_movements(board, a, white=False)):
            return False
        if (piece == b'n') and (b not in ChessGame.horse_movements(board, a, white=False)):
            return False
        if (piece == b'p') and (b not in ChessGame.pawn_movements(board, a, white=False)):
            if (self.is_en_passant(a, b) == False):
                return False

        board_after = np.copy(board)
        if self.is_castling(a, b) == True:
            board_after = self.execute_castling(a, b)
        else:
            board_after[a_y, a_x] = b'0'
            board_after[b_y, b_x] = piece

        if ChessGame.is_in_check(board_after, white=white_turn):
            return False

        return True
    
    def move(self, a, b, promotion_piece = None):
        a_x, a_y = a
        b_x, b_y = b

        is_valid = self.is_valid_move(a, b)

        if is_valid:
            print(f'Move {a} -> {b} /', end=' ')
        else:
            return self.board

        if promotion_piece is not None:
            print(f'Promotion: {promotion_piece} /', end=' ')

        if self.is_promotion(a, b):
            self.board = self.execute_promotion(a, b, promotion_piece)
        elif self.is_castling(a, b) == True:
            self.board = self.execute_castling(a, b)
        else:
            piece = self.board[a_y, a_x]
            self.board[a_y, a_x] = b'0'
            self.board[b_y, b_x] = piece

        self.update_castling(a)
        self.update_en_passant(a, b)

        copy = np.copy(self.board)
        self.history.append(copy)

        if self.white_turn == True:
            self.white_turn = False
        else:
            self.move_number += 1
            self.white_turn = True

        print(self.game_info())

        if ChessGame.is_in_check_mate(self.board, self.white_turn):
            print('Check Mate!!')

        return self.board

    def is_check_mate(self):
        board = self.board
        white = self.white_turn
        check_mate = ChessGame.is_in_check_mate(board, white)

        if (check_mate == True) and (white == True):
            return -1
        elif (check_mate == True) and (white == False):
            return 1
        else:
            return 0

    def game_info(self):
        info = f'Move number: {self.move_number} / '
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