import pygame
import numpy as np

pygame.init()

win = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Chess GPT")

chessboard = pygame.image.load('./images/chessboard.svg')

square_size = 60

pieces = {}
pieces[b'0'] = None
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

board = np.matrix([
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
], dtype=np.character)

piece_held = b'0'

run = True

while run:
    pygame.time.delay(10)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_column = mouse_x // 60
    mouse_row = mouse_y // 60

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            piece_held = board[mouse_row, mouse_column]
            board[mouse_row, mouse_column] = b'0'
        if event.type == pygame.MOUSEBUTTONUP:
            if piece_held != b'0':
                board[mouse_row, mouse_column] = piece_held
                piece_held = b'0'

    win.blit(chessboard, (0,0))

    for i in range(8):
        for j in range(8):
            if pieces[board[i, j]] is not None:
                win.blit(pieces[board[i, j]], (60*j, 60*i))

    if piece_held != b'0':
        win.blit(pieces[piece_held], (mouse_x - 30, mouse_y - 30))

    pygame.display.update()

pygame.quit() 