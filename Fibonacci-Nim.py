import pygame
import sys
from random import *


def coins():
    # Drawing a green rectangle in the top of the window
    pygame.draw.rect(screen, (47, 230, 222), (0, 0, width, square_size))
    # Drawing a blue square and yellow coin in top of the square for the rest of the window
    for i in range(coin // col):
        for j in range(col):
            pygame.draw.rect(screen, (28, 48, 65), (j * square_size, i * square_size + square_size,
                                                    square_size, square_size))
            screen.blit(icon, (j * square_size + 5, i * square_size + square_size + 5))


def moves(x, y):
    global player, move, remaining
    # Checking if the click is on one of the coins and the coin is not selected before
    if y >= 0 and move < Max and (x, y) not in selected:
        # Turning the coin color from yellow to black
        pygame.draw.circle(screen, (0, 0, 0), (x * square_size + square_size // 2,
                                               y * square_size + 3 * square_size // 2), square_size // 2 - 5)
        # Increasing the player move every time he select a coin
        move += 1
        # Decreasing the number of coins every time the player select a coin
        remaining -= 1
        # Adding the selected coins to the list to make it not selectable
        selected.append((x, y))
        # Adding the selected coins of the player who is playing in case if he wants to reset his turn
        player_moves.append((x, y))


def reset():
    global player_moves
    # Turning all the selected coins of the player who has just played from black to yellow again to be selectable again
    for x, y in player_moves:
        screen.blit(icon, (x * square_size + 5, y * square_size + square_size + 5))
        # Removing the coin from the list of selected coins
        selected.remove((x, y))
    # Clearing the current player selected coins from the list
    player_moves.clear()


def winner():
    # Checking if the player selected the last coin
    if len(selected) == coin:
        return True


game_over = False
# Declaring the size of a square to make the window on aspect of it
square_size = 130
col = 14
selected = []
player_moves = []
move = 0
player = 1
# Making random number of coins
coin = choice([i for i in range(4 * col, 7 * col, col)])
remaining = coin
# Declaring the max input of the first turn
Max = coin - 1

pygame.init()
# Changing the caption and the icon of the window
icon = pygame.image.load("dollar.png")
pygame.display.set_caption("Fibonacci Nim")
pygame.display.set_icon(icon)
# Declaring the used fonts in the project and their size and if they bold or italic
font_1 = pygame.font.SysFont("Arial", 60, True, False)
font_2 = pygame.font.SysFont("Arial", 250, True, True)
# Declaring the ratio of the window
width = col * square_size
height = (coin // col + 1) * square_size
# Making the window
screen = pygame.display.set_mode((width, height))
# Importing the buttons used in the project
submit_button = pygame.image.load("submit.png")
reset_button = pygame.image.load("reset.png")
icon = pygame.transform.scale(icon, (square_size - 10.01, square_size - 10.01))
# Creating the board
coins()

while not game_over:
    # Drawing a green rectangle in the top of the window and displaying the text with fonts we declared and the buttons
    pygame.draw.rect(screen, (47, 230, 222), (0, 0, width, square_size))
    # Displaying player turn in the top right corner of the window
    screen.blit(font_1.render(f"Player {player} Move", True, (137, 4, 61)), (1450, 30))
    # Displaying the buttons in the top left corner of the window
    screen.blit(submit_button, (25, 25))
    screen.blit(reset_button, (178, 20))
    # Displaying max move and selected coins of the player who is playing
    screen.blit(font_1.render(f"Selected Coins: {move}", True, (137, 4, 61)), (650, 0))
    screen.blit(font_1.render(f"The Most You Can Select: {Max}", True, (137, 4, 61)), (550, 60))
    # Updating the window to display the changes we made
    pygame.display.update()

    for action in pygame.event.get():
        # Checking if the user closed the game and closing it
        if action.type == pygame.QUIT:
            sys.exit()

        # Checking if the user clicked in the window using the mouse
        if action.type == pygame.MOUSEBUTTONDOWN:
            # Drawing a green rectangle in the top of the window and displaying the text with fonts we declared and the buttons
            pygame.draw.rect(screen, (47, 230, 222), (0, 0, width, square_size))
            # Displaying player turn in the top right corner of the window
            screen.blit(font_1.render(f"Player {player} Move", True, (137, 4, 61)), (1450, 30))
            # Displaying the buttons in the top left corner of the window
            screen.blit(submit_button, (25, 25))
            screen.blit(reset_button, (178, 20))
            # Displaying max move and selected coins of the player who is playing
            screen.blit(font_1.render(f"Selected Coins: {move}", True, (137, 4, 61)), (650, 0))
            screen.blit(font_1.render(f"The Most You Can Select: {Max}", True, (137, 4, 61)), (550, 60))
            # Taking the coordinates of the click in the window
            if pygame.mouse.get_pressed()[0]:
                position = action.pos

                # First player turn
                if player == 1:
                    # Assigning the coordinates of the click to two variables
                    one_move_x, one_move_y = position
                    # Dividing the coordinates of the click by the square size to make it number from 0 to col
                    moves(one_move_x // square_size, one_move_y // square_size - 1)

                # Second player turn
                elif player == 2:
                    # Assigning the coordinates of the click to two variables
                    two_move_x, two_move_y = position
                    # Dividing the coordinates of the click by the square size to make it number from 0 to col
                    moves(two_move_x // square_size, two_move_y // square_size - 1)

                # Checking if the player clicked in submit button
                if position[0] in range(25, 154) and position[1] in range(25, 154):
                    if winner():
                        # If the player wins the window will be filled with blue square and text of the player who won will be displayed on the window
                        pygame.draw.rect(screen, (10, 16, 69), (0, 0, width, height))
                        screen.blit(font_2.render(f"Player {player} Wins ! !", True, (214, 40, 40)), (width // col,
                                                                                                      height // 3.5))
                        game_over = True

                    # Checking if the player selected any coins or not if not then he will continue playing
                    elif player_moves:
                        # Changing the player turn
                        player = 1 if player == 2 else 2
                        # Clearing The list with last player moves
                        player_moves.clear()
                        # Changing the max select possible
                        Max = move * 2 if move < remaining else remaining
                        # Resetting player moves
                        move = 0

                # Checking if the player clicked in reset button
                elif position[0] in range(178, 274) and position[1] in range(20, 116):
                    # Resetting player moves
                    move = 0
                    reset()

            # Updating the window to display the changes we made
            pygame.display.update()

            # if the game is over don't close unless 2 seconds pass to display the winner
            if game_over:
                pygame.time.wait(2000)
