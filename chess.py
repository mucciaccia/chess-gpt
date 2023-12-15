import numpy as np
from chess_position import ChessPosition
from gpt_api import GptApi

class ChessGame:

    def __init__(self) -> None:
        self.position = ChessPosition()
        self.move_number = 0
        self.history = [self.position]
        self.move_history = []

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

        move = (x, y + d)
        if position.is_empty(move):
            move_list.append(move)
        move = (x, y + 2*d)
        if white == True and y == 1 and position.is_empty(move):
            move_list.append(move)
        elif white == False and y == 6 and position.is_empty(move):
            move_list.append(move)
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
                for k in moves:
                    all_moves.append(((i, j), k))

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
    
    def is_move_blocked_by_check(position : ChessPosition, a, b, white):
        copy = position.unrestricted_move(a, b)
        in_check = ChessGame.is_in_check(copy, white)
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
                    if ChessGame.is_move_blocked_by_check(position, coordinates, move, white) == False:
                        return 0
                    
        if white == True:
            return -1
        elif white == False:
            return 1
        else:
            return 0

    def castling_info(a, b):
        if a == (4, 0) and b in [(0, 0), (1, 0), (2, 0)]:
            kingside = False
            white = True
        elif a == (4, 0) and b in [(7, 0), (6,0)]:
            kingside = True
            white = True
        elif a == (4, 7) and b in [(0, 7), (1, 7), (2, 7)]:
            kingside = False
            white = False
        elif a == (4, 7) and b in [(7, 7), (6, 7)]:
            kingside = True
            white = False

        return kingside, white

    def is_castling(self, a, b):
        if a == (4, 0) and b in [(0, 0), (1, 0), (2, 0)]:
            kingside = False
            white = True
        elif a == (4, 0) and b in [(7, 0), (6,0)]:
            kingside = True
            white = True
        elif a == (4, 7) and b in [(0, 7), (1, 7), (2, 7)]:
            kingside = False
            white = False
        elif a == (4, 7) and b in [(7, 7), (6, 7)]:
            kingside = True
            white = False
        else:
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

        kingside, white = ChessGame.castling_info(a, b)

        copy = np.copy(self.position.board)
        if (kingside == False) and (white == True):
            copy[0, 0] = b'0'
            copy[0, 1] = b'0'
            copy[0, 2] = b'K'
            copy[0, 3] = b'R'
            copy[0, 4] = b'0'
        elif (kingside == True) and (white == True):
            copy[0, 4] = b'0'
            copy[0, 5] = b'R'
            copy[0, 6] = b'K'
            copy[0, 7] = b'0'
        elif (kingside == False) and (white == False):
            copy[7, 0] = b'0'
            copy[7, 1] = b'0'
            copy[7, 2] = b'K'
            copy[7, 3] = b'R'
            copy[7, 4] = b'0'
        elif (kingside == True) and (white == False):
            copy[7, 4] = b'0'
            copy[7, 5] = b'R'
            copy[7, 6] = b'K'
            copy[7, 7] = b'0'
        position = ChessPosition()
        position.board = copy
        return position
    
    def update_castling(self, a):
        if a == (0, 0):
            self.position.white_queenside_castling = False
        elif a == (7, 0):
            self.position.white_kingside_castling = False
        elif a == (4, 0):
            self.position.white_kingside_castling = False
            self.position.white_queenside_castling = False
        elif a == (0, 7):
            self.position.black_queenside_castling = False
        elif a == (7, 7):
            self.position.black_kingside_castling = False
        elif a == (4, 7):
            self.position.black_kingside_castling = False
            self.position.black_queenside_castling = False
        return
    
    def is_en_passant(self, a, b):

        print('Tem que entrar aqui')

        a_x, a_y = a
        b_x, b_y = b
        
        piece1 = self.position.get_piece(a)
        piece2 = self.position.get_piece((b_x, a_y))
        en_passant = self.position.en_passant

        print(a)
        print(b)
        print(piece1)
        print(piece2)

        if (piece1 == b'P') and (piece2 == b'p') and (a_y == 4) and (b_y == 5) and (abs(a_x - b_x) == 1) and (b_x == en_passant):
            print('chegoualajsld')
            return True

        if (piece1 == b'p') and (piece2 == b'P') and (a_y == 3) and (b_y == 2) and (abs(a_x - b_x) == 1) and (b_x == en_passant):
            print('chegoualajsld')
            return True

        return False

    def execute_en_passant(self, a, b):
        _, a_y = a
        b_x, _ = b
        new_position = self.position.remove_piece((b_x, a_y))
        new_position = new_position.unrestricted_move(a, b)
        new_position.en_passant = None
        return new_position

    def update_en_passant(self, a, b):
        _, a_y = a
        b_x, b_y = b
        piece = self.position.get_piece(b)

        if (a_y == 1) and (b_y == 3) and (piece == b'P'):
            self.position.en_passant = b_x
        elif (a_y == 6) and (b_y == 4) and (piece == b'p'):
            self.position.en_passant = b_x
        else:
            self.position.en_passant = None
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
        a_x, a_y = a
        b_x, b_y = b
        piece = self.position.get_piece(a)
        copy = np.copy(self.position.board)
        if (piece == b'P') and (b_y == 7):
            copy[a_y, a_x] = b'0'
            copy[b_y, b_x] = promotion_piece
        if (piece == b'p') and (b_y == 0):
            copy[a_y, a_x] = b'0'
            copy[b_y, b_x] = promotion_piece
        return copy

    def is_valid_move(self, a, b):
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

        position_after = self.position.copy()
        if self.is_castling(a, b) == True:
            position_after = self.execute_castling(a, b)
        else:
            position_after = self.position.unrestricted_move(a, b)

        if ChessGame.is_in_check(position_after, white=white_turn):
            return False

        return True
    
    def move(self, a, b, promotion_piece = None):
        is_valid = self.is_valid_move(a, b)

        if is_valid:
            print(f'Move {self.to_long_algebraic_notation(a, b)} /', end=' ')
            print(f'Move {self.from_long_algebraic_notation(self.to_long_algebraic_notation(a, b))} /', end=' ')
        else:
            return self.position.board

        if promotion_piece is not None:
            print(f'Promotion: {promotion_piece} /', end=' ')

        if self.is_promotion(a, b):
            self.position.board = self.execute_promotion(a, b, promotion_piece)
        elif self.is_castling(a, b):
            self.position.board = self.execute_castling(a, b)
        elif self.is_en_passant(a, b):
            self.position = self.execute_en_passant(a, b)
        else:
            self.position = self.position.unrestricted_move(a, b)

        self.update_castling(a)
        self.update_en_passant(a, b)

        copy = np.copy(self.position.board)
        self.history.append(copy)

        if self.position.white_turn == True:
            self.position.white_turn = False
        else:
            self.move_number += 1
            self.position.white_turn = True

        print(self.game_info())

        if self.is_check_mate() != 0:
            print('Check Mate!!')

        return self.position.board
    
    def move_2_players(self, a, b, promotion_piece = None):

        valid = self.is_valid_move(a, b)
        if valid == True:
            self.move_history.append(self.to_long_algebraic_notation(a, b))
        else:
            return self.move(a, b, promotion_piece)    
        self.move(a, b, promotion_piece)
        fen_str = self.position.to_FEN_notation()
        print(f'FEN: {self.position.to_FEN_notation()}')

        valid = False
        while valid == False:
            text = GptApi.move("\n".join(self.move_history))
            (a, b) = self.from_long_algebraic_notation(text)
            valid = self.is_valid_move(a, b)
        self.move_history.append(self.to_long_algebraic_notation(a, b))
        self.move(a, b)
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

    def game_info(self):
        info = f'Move number: {self.move_number} / '
        info += self.position.info()
        return info
    
