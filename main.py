import pygame
import numpy as np
from chess import ChessGame

pygame.init()

win = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Chess GPT")

chessboard = pygame.image.load('./images/chessboard.svg')

square_size = 60

pieces = {}
pieces[b'0'] = None
pieces[b'x'] = pygame.image.load('./images/cancel.svg')
pieces[b'k'] = pygame.image.load('./images/black_king.svg')
pieces[b'q'] = pygame.image.load('./images/black_queen.svg')
pieces[b'r'] = pygame.image.load('./images/black_rook.svg')
pieces[b'b'] = pygame.image.load('./images/black_bishop.svg')
pieces[b'n'] = pygame.image.load('./images/black_knight.svg')
pieces[b'p'] = pygame.image.load('./images/black_pawn.svg')
pieces[b'K'] = pygame.image.load('./images/white_king.svg')
pieces[b'Q'] = pygame.image.load('./images/white_queen.svg')
pieces[b'R'] = pygame.image.load('./images/white_rook.svg')
pieces[b'B'] = pygame.image.load('./images/white_bishop.svg')
pieces[b'N'] = pygame.image.load('./images/white_knight.svg')
pieces[b'P'] = pygame.image.load('./images/white_pawn.svg')
for key in pieces:
    if pieces[key] is not None:
        pieces[key] = pygame.transform.smoothscale(pieces[key], (60, 60))


piece_held = b'0'
promotion = None
promotion_pieces = [b'q', b'r', b'b', b'n']

chessGame = ChessGame()
board = chessGame.get_board()

a_x = None
a_y = None
b_x = None
b_y = None

run = True

while run:
    pygame.time.delay(10)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_column = mouse_x // 60
    mouse_row = 7 - mouse_y // 60

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            a_x = mouse_column
            a_y = mouse_row
            piece_held = board[mouse_row, mouse_column]

            print(f'Clicked {mouse_row}, {mouse_column}, piece_held: {piece_held}')
            if promotion is None:
                piece_held = board[a_y, a_x]
                piece_held_last_row = mouse_row
                piece_held_last_column = mouse_column
            elif promotion == mouse_column and mouse_row > 3:
                board[7, promotion] = promotion_pieces[mouse_row]
                piece_held = b'0'
                promotion = None
            else:
                promotion = None
                board[piece_held_last_row, piece_held_last_column] = promoted_piece

        if event.type == pygame.MOUSEBUTTONUP:
            b_x = mouse_column
            b_y = mouse_row
            if piece_held == b'p' and mouse_row == 0:
                promotion = mouse_column
                promoted_piece = piece_held
            board = chessGame.move((a_x, a_y), (b_x, b_y))
            piece_held = b'0'
            a_x = None
            a_y = None
            b_x = None
            b_y = None

    win.blit(chessboard, (0,0))

    for i in range(8):
        for j in range(8):
            if pieces[board[i, j]] is not None and not (i == a_y and j == a_x):
                win.blit(pieces[board[i, j]], (60*j, 60*(7 - i)))

    if piece_held != b'0':
        win.blit(pieces[piece_held], (mouse_x - 30, mouse_y - 30))

    if promotion is not None:
        color = (255,255,255)
        pygame.draw.rect(win, color, pygame.Rect(60*promotion, 0, 60, 300))
        win.blit(pieces[b'q'], (60 * promotion, 0))
        win.blit(pieces[b'r'], (60 * promotion, 60))
        win.blit(pieces[b'b'], (60 * promotion, 120))
        win.blit(pieces[b'n'], (60 * promotion, 180))
        win.blit(pieces[b'x'], (60 * promotion, 240))

    pygame.display.update()

pygame.quit() 