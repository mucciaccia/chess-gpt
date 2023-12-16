import pygame
import numpy as np
from chess import ChessGame

pygame.init()

square_size = 90
screen_size = (8 * square_size, 8 * square_size)
win = pygame.display.set_mode(screen_size)
font = pygame.font.Font(None, 36)
text_white_won = font.render('Check mate! White won!', True, (255, 255, 255))
text_black_won = font.render('Check mate! Black won!', True, (255, 255, 255))
pygame.display.set_caption("Chess GPT")

chessboard = pygame.image.load('./images/chessboard.svg')
chessboard = pygame.transform.scale(chessboard, screen_size)
chessboard = pygame.transform.flip(chessboard, False, True)

pieces = {}
pieces[b'0'] = None
pieces[b'x'] = pygame.image.load('./images/cancel.svg')
pieces[b'k'] = pygame.image.load('./images/theme_gpt/black_king.png')
pieces[b'q'] = pygame.image.load('./images/theme_gpt/black_queen.png')
pieces[b'r'] = pygame.image.load('./images/theme_gpt/black_rook.png')
pieces[b'b'] = pygame.image.load('./images/theme_gpt/black_bishop.png')
pieces[b'n'] = pygame.image.load('./images/theme_gpt/black_knight.png')
pieces[b'p'] = pygame.image.load('./images/theme_gpt/black_pawn.png')
pieces[b'K'] = pygame.image.load('./images/theme_gpt/white_king.png')
pieces[b'Q'] = pygame.image.load('./images/theme_gpt/white_queen.png')
pieces[b'R'] = pygame.image.load('./images/theme_gpt/white_rook.png')
pieces[b'B'] = pygame.image.load('./images/theme_gpt/white_bishop.png')
pieces[b'N'] = pygame.image.load('./images/theme_gpt/white_knight.png')
pieces[b'P'] = pygame.image.load('./images/theme_gpt/white_pawn.png')
for key in pieces:
    if pieces[key] is not None:
        pieces[key] = pygame.transform.smoothscale(pieces[key], (square_size, square_size))


pygame.display.set_icon(pieces[b'k'])

piece_held = {
    'code': b'0',
    'position_before': (-1, -1),
    'position_after': (-1, -1),

}

promotion = {
    'is_active': False,
    'column': 0,
    'top': True,
    'choosen_piece': b'0',
    'pieces': {
        False: [b'x', b'n', b'b', b'r', b'q'],
        True: [b'Q', b'R', b'B', b'N', b'x']
    }
}

chessGame = ChessGame()
board = chessGame.get_board()

a_x = None
a_y = None
b_x = None
b_y = None

white = True
result = 0
run = True

def update_promotion(piece_held, promotion, white, move):
    b_x, b_y = move

    if (piece_held['code'] == b'p') and (b_y == 0) and (white == False):
        promotion['is_active'] = True
        promotion['column'] = b_x
        promotion['top'] = False
        piece_held['code'] = b'0'
    elif (piece_held['code'] == b'P') and (b_y == 7) and (white == True):
        promotion['is_active'] = True
        promotion['column'] = b_x
        promotion['top'] = True
        piece_held['code'] = b'0'

    return promotion

def mouse_down_promotion(board, piece_held, promotion, white, mouse_x, mouse_y):
    x_min = square_size * promotion['column']
    x_max = square_size * promotion['column'] + square_size
    if promotion['top'] == True:
        y_min = 0
        y_max = 4 * square_size
    else:
        y_min = 4 * square_size
        y_max = 8 * square_size

    if (mouse_x < x_min) or (mouse_x > x_max) or (mouse_y < y_min) or (mouse_y > y_max):
        promotion['is_active'] = False
        piece_held['code'] = b'0'
        result = 0
    else:
        option = (mouse_y - y_min) // square_size
        if white == False:
            option += 1
        choosen_piece = promotion['pieces'][white][option]
        board = chessGame.move(piece_held['position_before'], piece_held['position_after'], choosen_piece)
        white = chessGame.position.white_turn
        result = chessGame.is_check_mate()
        promotion['is_active'] = False
        piece_held['code'] = b'0'

    return board, result, white

while run:
    pygame.time.delay(10)
 
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_column = mouse_x // square_size
    mouse_row = 7 - mouse_y // square_size

    if (result == 0) and (promotion['is_active'] == False) and (chessGame.gpt_mode == True) and (chessGame.position.white_turn != chessGame.player_white):
        board = chessGame.gpt_move()
        white = chessGame.position.white_turn
        result = chessGame.is_check_mate()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):
            a_x = mouse_column
            a_y = mouse_row

            if promotion['is_active']:
                board, result, white = mouse_down_promotion(board, piece_held, promotion, white, mouse_x, mouse_y)
            else:
                piece_held['code'] = board[a_y, a_x]
                piece_held['position_before'] = (a_x, a_y)

        if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
            b_x = mouse_column
            b_y = mouse_row
            piece_held['position_after'] = (b_x, b_y)
            promotion = update_promotion(piece_held, promotion, white, (b_x, b_y))

            if promotion['is_active'] == False:
                board = chessGame.move((a_x, a_y), (b_x, b_y))
                white = chessGame.position.white_turn
                result = chessGame.is_check_mate()
                piece_held['code'] = b'0'
                a_x = None
                a_y = None
                b_x = None
                b_y = None

    win.blit(chessboard, (0,0))

    for i in range(8):
        for j in range(8):
            if pieces[board[i, j]] is not None and not (i == a_y and j == a_x):
                win.blit(pieces[board[i, j]], (square_size*j, square_size*(7 - i)))

    if piece_held['code'] != b'0':
        win.blit(pieces[piece_held['code']], (mouse_x - 30, mouse_y - 30))

    if promotion['is_active'] == True:
        color = (255,255,255)
        if promotion['top'] == True:
            y_min = 0
        else:
            y_min = 3 * square_size
        pygame.draw.rect(win, color, pygame.Rect(square_size*promotion['column'], y_min, square_size, 5*square_size))
        win.blit(pieces[promotion['pieces'][white][0]], (square_size * promotion['column'], y_min + 0))
        win.blit(pieces[promotion['pieces'][white][1]], (square_size * promotion['column'], y_min + square_size))
        win.blit(pieces[promotion['pieces'][white][2]], (square_size * promotion['column'], y_min + 2*square_size))
        win.blit(pieces[promotion['pieces'][white][3]], (square_size * promotion['column'], y_min + 3*square_size))
        win.blit(pieces[promotion['pieces'][white][4]], (square_size * promotion['column'], y_min + 4*square_size))

    if result == 1:
        pygame.draw.rect(win, (0,0,0), pygame.Rect(square_size * 2, square_size * 3, square_size * 4, square_size * 2))
        win.blit(text_white_won, (square_size * 2.5, square_size * 3.8))
    if result == -1:
        win.blit(text_black_won, (square_size * 2.5, square_size * 3.8))

    pygame.display.update()

pygame.quit() 