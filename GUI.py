import numpy as np
import pygame
import sys

COLOR_BLUE = (0, 0, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_YELLOW = (255, 255, 0)


# create initial board
def create_board():
    return np.zeros((6, 7))


# drop the piece in the board according to the user selection
def drop_piece(board, row, col, piece):
    board[row][col] = piece


# check if the move the user chose is valid
def check_valid_move(board, column):
    if board[0, column] != 0:
        return False
    return True


# get the right row in the chosen column
def get_next_open_row(board, col):
    for i in range(5, -1, -1):
        if board[i][col] == 0:
            return i


# check if the last move is a finish move for the game
def check_winning_move(board, piece):

    for i in range(6):
        for j in range(7):
            if j <= 3:
                if board[i][j] == board[i][j + 1] == board[i][j + 2] == board[i][j + 3] == piece:
                    return True
            if i < 3:
                if board[i][j] == board[i + 1][j] == board[i + 2][j] == board[i + 3][j] == piece:
                    return True
            if i < 3 and j <= 3:
                if board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3] == piece:
                    return True
            if i >= 3 and 3 >= j:
                if board[i][j] == board[i - 1][j + 1] == board[i - 2][j + 2] == board[i - 3][j + 3] == piece:
                    return True
    return False


def draw_board(board):
    for c in range(7):
        for r in range(6):
            pygame.draw.rect(screen, COLOR_BLUE, (c*100, r*100 + 100, 100, 100))
            if board[r][c] == 0:
                pygame.draw.circle(screen, COLOR_BLACK, (c*100+50, r*100+150), 45)
            elif board[r][c] == 1:
                pygame.draw.circle(screen, COLOR_YELLOW, (c*100+50, r*100+150), 45)
            else:
                pygame.draw.circle(screen, COLOR_RED, (c*100+50, r*100+150), 45)

    pygame.display.update()


board = create_board()
game_over = False
turn = 0

pygame.init()
width = height = 700

screen = pygame.display.set_mode((width, height))
draw_board(board)
pygame.display.update()
message = pygame.font.SysFont('monospace', 75)

while not game_over:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit(0)

        if e.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, COLOR_BLACK, (0, 0, width, 100))
            pos = e.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, COLOR_YELLOW, (pos, 50), 45)
            else:
                pygame.draw.circle(screen, COLOR_RED, (pos, 50), 45)
        pygame.display.update()

        if e.type == pygame.MOUSEBUTTONDOWN:
            if turn == 0:
                selected_column = e.pos[0] // 100
                if check_valid_move(board, selected_column):
                    row = get_next_open_row(board, selected_column)
                    drop_piece(board, row, selected_column, 1)
                if check_winning_move(board, 1):
                    pygame.draw.rect(screen, COLOR_BLACK, (0, 0, width, 100))
                    win_message = message.render("player 1 wins", True, COLOR_YELLOW)
                    screen.blit(win_message, (40, 10))
                    game_over = True

            elif turn == 1:
                print("player 2 turn")
                selected_column = e.pos[0] // 100
                if check_valid_move(board, selected_column):
                    row = get_next_open_row(board, selected_column)
                    drop_piece(board, row, selected_column, 2)
                if check_winning_move(board, 2):
                    pygame.draw.rect(screen, COLOR_BLACK, (0, 0, width, 100))
                    win_message = message.render("player 2 wins", True, COLOR_RED)
                    screen.blit(win_message, (40, 10))
                    game_over = True

            draw_board(board)
            turn = (turn + 1) % 2

            if game_over:
                pygame.time.wait(3000)

