import numpy as np


class ChessGame:

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
        self.move_number = 0
        self.white_turn = True
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

    def is_in_check(board, white):
        if white == True:
            king_coordinates = ChessGame.find_piece(board, b'K')
        else:
            king_coordinates = ChessGame.find_piece(board, b'k')
        king_is_atacked = ChessGame.is_atacked(board, king_coordinates, white)
        return (king_is_atacked > 0)


    def is_valid_move(board, a, b, white_turn):
        a_x, a_y = a
        b_x, b_y = b

        print(f'Move ({a_x},{a_y}){board[a_y, a_x]} ({b_x},{b_y}){board[b_y, b_x]}')

        piece = board[a_y, a_x]

        if (white_turn == True) and (piece in [b'k', b'q', b'r', b'b', b'n', b'p']):
            return False
        if (white_turn == False) and (piece in [b'K', b'Q', b'R', b'B', b'N', b'P']):
            return False

        if (piece == b'K') and (b not in ChessGame.king_movements(board, a, white=True)):
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
            return False

        if (piece == b'k') and (b not in ChessGame.king_movements(board, a, white=False)):
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
            return False

        board_after = np.copy(board)
        board_after[a_y, a_x] = b'0'
        board_after[b_y, b_x] = piece

        if ChessGame.is_in_check(board_after, white=False):
            return False

        return True
    
    def move(self, a, b):
        is_valid = ChessGame.is_valid_move(self.board, a, b, self.white_turn)

        if is_valid == False:
            return self.board

        a_x, a_y = a
        b_x, b_y = b
        piece = self.board[a_y, a_x]
        self.board[a_y, a_x] = b'0'
        self.board[b_y, b_x] = piece

        copy = np.copy(self.board)
        self.history.append(copy)

        if self.white_turn == True:
            self.white_turn = False
        else:
            self.move_number += 1
            self.white_turn = True

        return self.board
