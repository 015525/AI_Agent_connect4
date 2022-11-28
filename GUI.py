from ab.alpha_beta import alphabeta
from minimax.MiniMax import MiniMax
from state.State import State
import numpy as np
import pygame
import sys

# constant values in the code
COLOR_WHITE = (250, 250, 250)  # white color RGB values
COLOR_BLUE = (0, 0, 255)  # blue color RGB values
COLOR_BLACK = (0, 0, 0)  # black color RGB values
COLOR_RED = (255, 0, 0)  # red color RGB values
COLOR_YELLOW = (255, 255, 0)  # yellow color RGB values
SQUARE_SIZE = 100  # size of each square in the board
RADIUS = 45  # radius of the board pieces


# create initial board
def create_board():
    return np.zeros((6, 7))  # start the game with empty board


# drop the piece in the board according to the user selection
def drop_piece(board, row, col, piece):
    board[row][col] = piece


# check if the move the user chose is valid
def check_valid_move(board, column):
    if board[0, column] != 0:  # check the first row in the board if not 0 then its not empty to drop the piece
        return False
    return True


# get the right row in the chosen column
def get_next_open_row(board, col):
    for i in range(5, -1, -1):  # go through all rows in the column col to find the current empty slot
        if board[i][col] == 0:
            return i


# draw the board in GUI
def draw_board(screen, board):
    for c in range(7):  # go through 7 columns
        for r in range(6):  # go through 6 rows
            pygame.draw.rect(screen, COLOR_BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + 130, SQUARE_SIZE, SQUARE_SIZE))  # board in shape of squares
            if board[r][c] == 0:
                pygame.draw.circle(screen, COLOR_BLACK, (c * SQUARE_SIZE + 50, r * SQUARE_SIZE + 180), RADIUS)  # empty slots is black circle
            elif board[r][c] == 1:
                pygame.draw.circle(screen, COLOR_YELLOW, (c * SQUARE_SIZE + 50, r * SQUARE_SIZE + 180), RADIUS)  # player 1 plays yellow pieces
            else:
                pygame.draw.circle(screen, COLOR_RED, (c * SQUARE_SIZE + 50, r * SQUARE_SIZE + 180), RADIUS)  # player 2 plays red pieces

    pygame.display.update()  # display the board after checking the last status


def check_end_game(board):
    for i in range(7):
        if board[0, i] == 0:
            return False
    return True


# display the score of the computer and the player
def display_score(h_score, c_score, score_message, screen):
    pygame.draw.rect(screen, COLOR_BLACK, (0, 0, 700, 30))  # empty area to represents the score
    print(f"human score = : {h_score}, and computer score  = {c_score}")
    score_label = score_message.render(f"player: {h_score}        computer:{c_score}", 1, COLOR_WHITE)
    screen.blit(score_label, (20, 0))
    pygame.display.update()


# start the game
def play_game(algorithm, depth):
    current_state = State(6485768453102907528)
    board = create_board()  # create the board
    game_over = False
    turn = 0
    algo = MiniMax(depth)
    if algorithm == 1:
        algo = alphabeta(depth)

    pygame.init()
    width = 700
    height = 730
    screen = pygame.display.set_mode((width, height))
    draw_board(screen, board)
    score_message = pygame.font.SysFont('monospace', 20)  # score message properties
    winner_message = pygame.font.SysFont('monospace', 60)  # winner message properties
    h_score = c_score = 0  # initial value of the scores
    display_score(h_score, c_score, score_message, screen)  # display the score on the board

    while not game_over:

        # check for the end of the game before any play
        game_over = check_end_game(board)
        # if the game ended announce who is the winner
        if game_over:
            pygame.draw.rect(screen, COLOR_BLACK, (0, 0, 700, 130))  # empty area to represents the score
            # in case the player was the winner
            if h_score > c_score:
                print(f"human is the winner")
                winner_label = winner_message.render(f"the player wins", True, COLOR_YELLOW)
                screen.blit(winner_label, (30, 20))
            # in case the computer was the winner
            elif c_score > h_score:
                print("computer wins")
                winner_label = winner_message.render("the computer wins", True, COLOR_RED)
                screen.blit(winner_label, (30, 20))
            # in case of tie
            else:
                print("Tie")
                winner_label = winner_message.render("Tie! no Winners", True, COLOR_WHITE)
                screen.blit(winner_label, (30, 20))
            pygame.display.update()

            # keep the window open until the user close it
            keep_running = True
            while keep_running:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:  # quit the game if we pressed exit button
                        pygame.display.quit()
                        pygame.quit()  # end the program
                        keep_running = False
                        break

        # the computer turn
        if turn == 1:

            pygame.draw.rect(screen, COLOR_BLACK, (0, 30, width, SQUARE_SIZE))  # clear an empty area before each step to move the pieces in it
            pygame.display.update()

            col = algo.get_next_state(current_state)
            print(f"column is: {col}")
            next_state = current_state.update_state(col, State.computer)
            current_state = next_state
            if check_valid_move(board, 7 - col):
                row = get_next_open_row(board, 7 - col)
                drop_piece(board, row, 7 - col, 2)
                draw_board(screen, board)
                turn = (turn + 1) % 2
                draw_board(screen, board)
                h_score, c_score = current_state.get_total_score()
                display_score(h_score, c_score, score_message, screen)

        # if the user wants to quit in the middle of the game
        for e in pygame.event.get():
            if e.type == pygame.QUIT:  # quit the game if we pressed exit button
                pygame.display.quit()
                pygame.quit()  # end the program
                game_over = True
                break;

            # let the pieces move with the mouse
            if e.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, COLOR_BLACK, (0, 30, width, 100))  # clear an empty area before each step
                pos = e.pos[0]  # get the x axis of the mouse
                if turn == 0:
                    pygame.draw.circle(screen, COLOR_YELLOW, (pos, 80), 45)  # player 1 plays with yellow pieces
                pygame.display.update()

            # the player turn and he clicked the mouse
            elif e.type == pygame.MOUSEBUTTONDOWN:
                print("this is user turn")
                if turn == 0:
                    col = e.pos[0] // 100
                    next_s = current_state.update_state(7 - col, State.human)
                    current_state = next_s
                    if check_valid_move(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)
                        turn = (turn + 1) % 2

                draw_board(screen, board)
                h_score, c_score = current_state.get_total_score()
                display_score(h_score, c_score, score_message, screen)
