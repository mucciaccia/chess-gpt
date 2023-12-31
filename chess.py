import numpy as np
from chess_position import ChessPosition
from gpt_api import GptApi

class ChessGame:

    def __init__(self, player_white) -> None:
        self.position = ChessPosition()
        self.move_number = 0
        self.history = [self.position]
        self.move_history = []
        self.player_white = player_white
        self.gpt_mode = True

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

    def get_board(self):
        return self.position.board

    def direction_movements(position : ChessPosition, coordinates, direction, white):
        (x, y) = coordinates
        (dx, dy) = direction
        move_list = []
        x += dx
        y += dy
        while position.is_on_board((x, y)):
            move = (x, y)
            if position.is_empty(move):
                move_list.append(move)
            elif position.is_occupied_by_friend(move, white):
                break
            elif position.is_occupied_by_enemy(move, white):
                move_list.append(move)
                break
            x += dx
            y += dy
        return move_list

    def bishop_movements(position : ChessPosition, coordinates, white):
        move_list = []
        move_list.extend(ChessGame.direction_movements(position, coordinates, (1, 1), white))
        move_list.extend(ChessGame.direction_movements(position, coordinates, (1, -1), white))
        move_list.extend(ChessGame.direction_movements(position, coordinates, (-1, 1), white))
        move_list.extend(ChessGame.direction_movements(position, coordinates, (-1, -1), white))
        return move_list

    def rook_movements(position : ChessPosition, coordinates, white):
        move_list = []
        move_list.extend(ChessGame.direction_movements(position, coordinates, (0, 1), white))
        move_list.extend(ChessGame.direction_movements(position, coordinates, (0, -1), white))
        move_list.extend(ChessGame.direction_movements(position, coordinates, (1, 0), white))
        move_list.extend(ChessGame.direction_movements(position, coordinates, (-1, 0), white))
        return move_list

    def queen_movements(position : ChessPosition, coordinates, white):
        move_list = []
        move_list.extend(ChessGame.bishop_movements(position, coordinates, white))
        move_list.extend(ChessGame.rook_movements(position, coordinates, white))
        return move_list
    
    def horse_movements(position : ChessPosition, coordinates, white):
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
            if position.is_on_board(move) and not position.is_occupied_by_friend(move, white):
                move_list.append(move)

        return move_list
    
    def pawn_movements(position : ChessPosition, coordinates, white):
        (x, y) = coordinates
        move_list = []

        if white:
            d = 1
        else:
            d = -1

        move1 = (x, y + d)
        if position.is_empty(move1):
            move_list.append(move1)
        move2 = (x, y + 2*d)
        if (white == True) and (y == 1) and position.is_empty(move1) and position.is_empty(move2):
            move_list.append(move2)
        elif white == False and y == 6 and position.is_empty(move1) and position.is_empty(move2):
            move_list.append(move2)
        move = (x - 1, y + d)
        if position.is_occupied_by_enemy(move, white):
            move_list.append(move)
        move = (x + 1, y + d)
        if position.is_occupied_by_enemy(move, white):
            move_list.append(move)

        return move_list
    
    def king_movements(position : ChessPosition, coordinates, white):
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
            if position.is_on_board(move) and not position.is_occupied_by_friend(move, white):
                move_list.append(move)

        return move_list
    
    def en_passant_movements(position : ChessPosition, coordinates):
        if position.en_passant is None:
            return []
        
        move_list = []

        d = 1
        (a_x, a_y) = coordinates
        b_x = position.en_passant
        b_y = a_y + d
        
        piece1 = position.get_piece((a_x, a_y))
        piece2 = position.position.get_piece((b_x, a_y))

        if (piece1 == b'P') and (piece2 == b'p') and (a_y == 4) and (b_y == 5) and (abs(a_x - b_x) == 1):
            move_list.append((a_x, a_y), (b_x, b_y))
        if (piece1 == b'p') and (piece2 == b'P') and (a_y == 3) and (b_y == 2) and (abs(a_x - b_x) == 1):
            move_list.append((a_x, a_y), (b_x, b_y))

        return False
    

    def any_piece_movements(position : ChessPosition, coordinates, white):
        x, y = coordinates
        piece = position.board[y, x]

        if white == True and ChessGame.is_white(piece) == False:
            return []
        if white == False and ChessGame.is_black(piece) == False:
            return []
        if (piece == b'K') or (piece == b'k'):
            return ChessGame.king_movements(position, coordinates, white)
        elif (piece == b'Q') or (piece == b'q'):
            return ChessGame.queen_movements(position, coordinates, white)
        elif (piece == b'R') or (piece == b'r'):
            return ChessGame.rook_movements(position, coordinates, white)
        elif (piece == b'B') or (piece == b'b'):
            return ChessGame.bishop_movements(position, coordinates, white)
        elif (piece == b'N') or (piece == b'n'):
            return ChessGame.horse_movements(position, coordinates, white)
        elif (piece == b'P') or (piece == b'p'):
            return ChessGame.pawn_movements(position, coordinates, white)
        else:
            return []

    def possible_moves(position: ChessPosition):
        all_moves = []
        for i in range(0, 8):
            for j in range(0, 8):
                moves = ChessGame.any_piece_movements(position, (i, j), position.white_turn)
                for b in moves:
                    a = (i, j)
                    if not ChessGame.is_move_blocked_by_check(position, a, b):
                        all_moves.append((a, b))

        return all_moves

    def is_atacked(position : ChessPosition, coordinates, white):
        atacked = 0

        for move in ChessGame.pawn_movements(position, coordinates, white):
            (hx, hy) = move
            if white == True and position.board[hy, hx] == b'p':
                atacked += 1
            elif white == False and position.board[hy, hx] == b'P':
                atacked += 1

        for move in ChessGame.king_movements(position, coordinates, white):
            (hx, hy) = move
            if white == True and position.board[hy, hx] == b'k':
                atacked += 1
            elif white == False and position.board[hy, hx] == b'K':
                atacked += 1

        for move in ChessGame.bishop_movements(position, coordinates, white):
            (hx, hy) = move
            if white == True and position.board[hy, hx] in (b'q', b'b'):
                atacked += 1
            elif white == False and position.board[hy, hx] in (b'Q', b'B'):
                atacked += 1

        for move in ChessGame.rook_movements(position, coordinates, white):
            (hx, hy) = move
            if white == True and position.board[hy, hx] in (b'q', b'r'):
                atacked += 1
            elif white == False and position.board[hy, hx] in (b'Q', b'R'):
                atacked += 1

        for move in ChessGame.horse_movements(position, coordinates, white):
            (hx, hy) = move
            if white == True and position.board[hy, hx] == b'n':
                atacked += 1
            elif white == False and position.board[hy, hx] == b'N':
                atacked += 1

        return atacked

    def is_in_check(position : ChessPosition, white):
        if white == True:
            king_coordinates = position.find_piece(b'K')
        else:
            king_coordinates = position.find_piece(b'k')

        king_is_atacked = ChessGame.is_atacked(position, king_coordinates, white)
        return (king_is_atacked > 0)
    
    def is_move_blocked_by_check(position : ChessPosition, a, b):
        copy = position.unrestricted_move(a, b)
        in_check = ChessGame.is_in_check(copy, position.white_turn)
        return in_check

    def is_check_mate(self):
        position = self.position
        white = self.position.white_turn
        if ChessGame.is_in_check(position, white) == False:
            return 0
        for i in range(0, 8):
            for j in range(0, 8):
                coordinates = (i, j)
                moves = ChessGame.any_piece_movements(position, coordinates, white)
                for move in moves:
                    if ChessGame.is_move_blocked_by_check(position, coordinates, move) == False:
                        return 0
                    
        if white == True:
            return -1
        elif white == False:
            return 1
        else:
            return 0

    def castling_info(a, b):
        if (a == (4, 0)) and (b in [(0, 0), (1, 0), (2, 0)]):
            kingside = False
            white = True
            is_castling_attempt = True
        elif (a == (4, 0)) and (b in [(7, 0), (6,0)]):
            kingside = True
            white = True
            is_castling_attempt = True
        elif (a == (4, 7)) and (b in [(0, 7), (1, 7), (2, 7)]):
            kingside = False
            white = False
            is_castling_attempt = True
        elif (a == (4, 7)) and (b in [(7, 7), (6, 7)]):
            kingside = True
            white = False
            is_castling_attempt = True
        else:
            kingside = None
            white = None
            is_castling_attempt = False

        return kingside, white, is_castling_attempt

    def is_castling(self, a, b):

        kingside, white, is_castling_attempt = ChessGame.castling_info(a, b)
        if is_castling_attempt == False:
            return False

        position = self.position
        if (kingside == True) and (white == True) and (self.position.white_kingside_castling == True):
            return position.is_empty((5, 0)) and position.is_empty((6, 0))
        elif (kingside == False) and (white == True) and (self.position.white_queenside_castling == True):
            return position.is_empty((1, 0)) and position.is_empty((2, 0)) and position.is_empty((3, 0))
        elif (kingside == True) and (white == False) and (self.position.black_kingside_castling == True):
            return position.is_empty((5, 7)) and position.is_empty((6, 7))
        elif (kingside == False) and (white == False) and (self.position.black_queenside_castling == True):
            return position.is_empty((1, 7)) and position.is_empty((2, 7)) and position.is_empty((3, 7))
        else:
            return False
      
    def execute_castling(self, a, b):
        new_position = self.position.copy()

        kingside, white, _ = ChessGame.castling_info(a, b)

        if (kingside == False) and (white == True):
            new_position.board[0, 0] = b'0'
            new_position.board[0, 1] = b'0'
            new_position.board[0, 2] = b'K'
            new_position.board[0, 3] = b'R'
            new_position.board[0, 4] = b'0'
        elif (kingside == True) and (white == True):
            new_position.board[0, 4] = b'0'
            new_position.board[0, 5] = b'R'
            new_position.board[0, 6] = b'K'
            new_position.board[0, 7] = b'0'
        elif (kingside == False) and (white == False):
            new_position.board[7, 0] = b'0'
            new_position.board[7, 1] = b'0'
            new_position.board[7, 2] = b'k'
            new_position.board[7, 3] = b'r'
            new_position.board[7, 4] = b'0'
        elif (kingside == True) and (white == False):
            new_position.board[7, 4] = b'0'
            new_position.board[7, 5] = b'r'
            new_position.board[7, 6] = b'k'
            new_position.board[7, 7] = b'0'
        return new_position
    
    def update_castling(position, a, b):
        if (a == (0, 0)) or (b == (0, 0)):
            position.white_queenside_castling = False
        elif a == (7, 0) or (b == (7, 0)):
            position.white_kingside_castling = False
        elif a == (4, 0):
            position.white_kingside_castling = False
            position.white_queenside_castling = False
        elif a == (0, 7) or (b == (0, 7)):
            position.black_queenside_castling = False
        elif a == (7, 7) or (b == (7, 7)):
            position.black_kingside_castling = False
        elif a == (4, 7):
            position.black_kingside_castling = False
            position.black_queenside_castling = False
        return
    
    def is_en_passant(self, a, b):

        a_x, a_y = a
        b_x, b_y = b
        
        piece1 = self.position.get_piece(a)
        piece2 = self.position.get_piece((b_x, a_y))
        en_passant = self.position.en_passant

        if (piece1 == b'P') and (piece2 == b'p') and (a_y == 4) and (b_y == 5) and (abs(a_x - b_x) == 1) and (b_x == en_passant):
            return True

        if (piece1 == b'p') and (piece2 == b'P') and (a_y == 3) and (b_y == 2) and (abs(a_x - b_x) == 1) and (b_x == en_passant):
            return True

        return False

    def execute_en_passant(self, a, b):
        _, a_y = a
        b_x, _ = b
        new_position = self.position.remove_piece((b_x, a_y))
        new_position = new_position.unrestricted_move(a, b)
        new_position.en_passant = None
        return new_position

    def update_en_passant(position, a, b):
        _, a_y = a
        b_x, b_y = b
        piece = position.get_piece(b)

        if (a_y == 1) and (b_y == 3) and (piece == b'P'):
            position.en_passant = b_x
        elif (a_y == 6) and (b_y == 4) and (piece == b'p'):
            position.en_passant = b_x
        else:
            position.en_passant = None
        return

    def is_promotion(self, a, b):
        a_x, a_y = a
        _, b_y = b
        piece = self.position.board[a_y, a_x]
        if (piece == b'P') and (b_y == 7):
            return True
        if (piece == b'p') and (b_y == 0):
            return True
        return False

    def execute_promotion(self, a, b, promotion_piece):
        new_position = self.position.unrestricted_move(a, b, promotion_piece)
        return new_position

    def execute_move(self, a, b, promotion_piece):
        new_position = self.position.copy()
        if self.is_promotion(a, b):
            new_position = self.execute_promotion(a, b, promotion_piece)
        elif self.is_castling(a, b):
            new_position = self.execute_castling(a, b)
        elif self.is_en_passant(a, b):
            new_position = self.execute_en_passant(a, b)
        else:
            new_position = self.position.unrestricted_move(a, b)

        ChessGame.update_castling(new_position, a, b)
        ChessGame.update_en_passant(new_position, a, b)

        if self.position.white_turn == True:
            new_position.white_turn = False
        else:
            new_position.move_number += 1
            new_position.white_turn = True

        return new_position

    def is_valid_move(self, a, b, promotion_piece):
        position = self.position
        white_turn = self.position.white_turn

        piece = position.get_piece(a)

        if position.is_empty(a):
            return False
        if (white_turn == True) and ChessGame.is_black(piece):
            return False
        if (white_turn == False) and ChessGame.is_white(piece):
            return False

        if (piece == b'K') and (b not in ChessGame.king_movements(position, a, white=True)):
            if (self.is_castling(a, b) == False):
                return False
        if (piece == b'Q') and (b not in ChessGame.queen_movements(position, a, white=True)):
            return False
        if (piece == b'R') and (b not in ChessGame.rook_movements(position, a, white=True)):
            return False
        if (piece == b'B') and (b not in ChessGame.bishop_movements(position, a, white=True)):
            return False
        if (piece == b'N') and (b not in ChessGame.horse_movements(position, a, white=True)):
            return False
        if (piece == b'P') and (b not in ChessGame.pawn_movements(position, a, white=True)):
            if (self.is_en_passant(a, b) == False):
                return False

        if (piece == b'k') and (b not in ChessGame.king_movements(position, a, white=False)):
            if (self.is_castling(a, b) == False):
                return False
        if (piece == b'q') and (b not in ChessGame.queen_movements(position, a, white=False)):
            return False
        if (piece == b'r') and (b not in ChessGame.rook_movements(position, a, white=False)):
            return False
        if (piece == b'b') and (b not in ChessGame.bishop_movements(position, a, white=False)):
            return False
        if (piece == b'n') and (b not in ChessGame.horse_movements(position, a, white=False)):
            return False
        if (piece == b'p') and (b not in ChessGame.pawn_movements(position, a, white=False)):
            if (self.is_en_passant(a, b) == False):
                return False

        position_after = self.execute_move(a, b, promotion_piece)

        if ChessGame.is_in_check(position_after, white=white_turn):
            return False

        return True

    def move_info(self, a, b, promotion_piece = None):
        info = ''
        info += f'Move {self.to_long_algebraic_notation(a, b)} / '
        if promotion_piece is not None:
            info += f'Promotion: {promotion_piece} / '
        info += f'Move number: {self.move_number} / '
        info += self.position.info()
        return info

    def iso_move(self, a, b, promotion_piece = None):
        is_valid = self.is_valid_move(a, b, promotion_piece)

        if is_valid == False:
            return self.position.board

        self.position = self.execute_move(a, b, promotion_piece)

        copy = self.position.copy()
        self.history.append(copy)
        self.move_history.append(self.to_long_algebraic_notation(a, b))

        print(self.move_info(a, b, promotion_piece))

        if self.is_check_mate() != 0:
            print('Check Mate!!')

        return self.position.board

    def player_move(self, a, b, promotion_piece = None):
        is_valid = self.is_valid_move(a, b, promotion_piece)

        if is_valid == False:
            return self.position.board

        self.position = self.execute_move(a, b, promotion_piece)

        copy = self.position.copy()
        self.history.append(copy)
        self.move_history.append(self.to_long_algebraic_notation(a, b))

        print(self.move_info(a, b, promotion_piece))

        if self.is_check_mate() != 0:
            print('Check Mate!!')

        return self.position.board
    
    def to_long_algebraic_notation(self, a, b):
        a_x, a_y = a
        b_x, b_y = b
        move_str = ''
        move_str += chr(a_x + 97)
        move_str += str(a_y + 1)
        move_str += '-'
        move_str += chr(b_x + 97)
        move_str += str(b_y + 1)
        return move_str

    def from_long_algebraic_notation(self, move_str):
        move_str = move_str.lower()

        a_x = ord(move_str[0]) - 97
        a_y = ord(move_str[1]) - 49

        b_x = ord(move_str[3]) - 97
        b_y = ord(move_str[4]) - 49

        return [(a_x, a_y), (b_x, b_y)]   
