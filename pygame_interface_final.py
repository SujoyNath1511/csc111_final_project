"""CSC111 Winter 2021 Final Project: Building A Checkers AI Player

This is the file that handles the pygame interface of the project. This includes the menu
and the ability to look back at previous moves.

Copyright and Usage Information:
======================================
This file is provided solely for the use of the CSC111 Teaching team and for the
use of people who made this file, Mohamed Abdullahi, Benjamin Lee, Eren Findik and Sujoy
Deb Nath. Any other forms of distribution of this code is strictly prohibited without express
permission of the aforementioned group.
This file is Copyright (c) 2021 Sujoy Deb Nath, Benjamin Lee, Mohamed Abdullahi and Eren Findik.
"""
import time
import pygame
from ai_players_final import AggressivePlayer, RandomPlayer, DefensivePlayer, print_ai_statistics
import checkers_game_tree_final as checkers_game_tree
import checkers_game_with_pygame_final as checkers_pygame

DIMENSION = 6
RECT_SIZE = 100
OFFSET = 100
START_POS_BLACK = {'a2', 'b1', 'c2', 'd1', 'e2', 'f1'}
START_POS_WHITE = {'a6', 'b5', 'c6', 'd5', 'e6', 'f5'}
VALID_POSITIONS = [letter + str(2 * x) for x in range(1, 4) for letter in 'ace'] + \
                  [letter + str(2 * x + 1) for x in range(0, 3) for letter in 'bdf']
PLAYER_COLORS = ('white', 'black')

MOVE_LIMIT = 60
PLAYER_TYPES = ['Random Player', 'Aggressive Player', 'Defensive Player', 'Human Player']
RECT_HEIGHT = 70
RECT_WIDTH = 150


def choose_players(game_tree: checkers_game_tree.CheckersGameTree) -> \
        tuple[checkers_pygame.Player, checkers_pygame.Player]:
    """
    Handles the mouse events for the pygame interface before the game stars. Returns the chosen
    players.
    """
    player1 = None
    player2 = None
    player1_st = ('', '', '')
    player2_st = ('', '', '')

    player_dict = {'Random Player': RandomPlayer(),
                   'Aggressive Player': AggressivePlayer(game_tree),
                   'Defensive Player': DefensivePlayer(game_tree),
                   'Human Player': checkers_pygame.HumanPlayer()}
    size = (800, 800)

    allow = [pygame.MOUSEBUTTONDOWN]
    screen = checkers_pygame.initialize_screen(size, allow)
    draw_choose_players(screen)

    while True:
        draw_choose_players(screen)
        green_box(player1_st, player2_st, screen)
        pygame.display.update()
        event = pygame.event.wait()

        if event.type == pygame.MOUSEBUTTONDOWN:
            green = checkers_pygame.position_to_index(event.pos)
            if green is not None:
                if green[0] == 3:
                    # If a player on the Player2 block is clicked, it stores that player type
                    # and makes that box green
                    player2 = player_dict[PLAYER_TYPES[green[1]]]
                    player2_st = (PLAYER_TYPES[green[1]], green[0], green[1])
                elif green[0] == 1:
                    # If a player on the Player1 block is clicked, it stores that player type
                    # and makes that box green
                    player1 = player_dict[PLAYER_TYPES[green[1]]]
                    player1_st = (PLAYER_TYPES[green[1]], green[0], green[1])
                pygame.display.update()
            else:
                if 5 * OFFSET <= event.pos[0] <= 5 * OFFSET + RECT_WIDTH and OFFSET \
                        <= event.pos[1] <= OFFSET + RECT_HEIGHT:
                    # Handles starting game
                    if player1 is None or player2 is None:
                        rect3 = pygame.Rect((5 * OFFSET, OFFSET), (RECT_WIDTH, RECT_HEIGHT))
                        pygame.draw.rect(screen, (255, 0, 0), rect3, width=0)
                        rect4 = pygame.Rect((5 * OFFSET, OFFSET), (RECT_WIDTH + 1, RECT_HEIGHT + 1))
                        pygame.draw.rect(screen, (0, 0, 0), rect4, width=1)
                        checkers_pygame.draw_text(screen, ' Start the Game',
                                                  (5 * OFFSET, OFFSET + RECT_HEIGHT // 3), 26)
                        pygame.display.update()
                        time.sleep(0.4)
                    else:
                        return (player1, player2)
                elif 5 * OFFSET <= event.pos[0] <= 5 * OFFSET + RECT_WIDTH and OFFSET + RECT_HEIGHT\
                        <= event.pos[1] <= OFFSET + 2 * RECT_HEIGHT:
                    print_ai_statistics(game_tree)

        elif event.type == pygame.QUIT:
            pygame.display.quit()
            break


def draw_choose_players(screen: pygame.Surface) -> None:
    """
    Draws the choose player blocks
    """
    rect_height = 70
    rect_width = 150
    screen.fill((23, 153, 195))

    # Draws the rectengle writing 'Player1' on it
    rect1 = pygame.Rect((OFFSET, OFFSET), (rect_width, rect_height))
    pygame.draw.rect(screen, (93, 73, 83), rect1, width=0)
    checkers_pygame.draw_text(screen, ' Player1', (OFFSET, OFFSET + rect_height // 3), 26)
    rect1 = pygame.Rect((OFFSET, OFFSET), (rect_width + 1, rect_height + 1))
    pygame.draw.rect(screen, (0, 0, 0), rect1, width=1)

    # Draws the rectengle writing 'Player2' on it
    rect1 = pygame.Rect((3 * OFFSET, OFFSET), (rect_width, rect_height))
    pygame.draw.rect(screen, (93, 73, 83), rect1, width=0)
    checkers_pygame.draw_text(screen, ' Player2', (3 * OFFSET, OFFSET + rect_height // 3), 26)
    rect1 = pygame.Rect((3 * OFFSET, OFFSET), (rect_width + 1, rect_height + 1))
    pygame.draw.rect(screen, (0, 0, 0), rect1, width=1)

    # Draws the rectengle writing 'Start the Game' on it
    rect1 = pygame.Rect((5 * OFFSET, OFFSET), (rect_width, rect_height))
    pygame.draw.rect(screen, (148, 126, 193), rect1, width=0)
    checkers_pygame.draw_text(screen, ' Start the Game', (5 * OFFSET, OFFSET + rect_height // 3),
                              26)
    rect1 = pygame.Rect((5 * OFFSET, OFFSET), (rect_width + 1, rect_height + 1))
    pygame.draw.rect(screen, (0, 0, 0), rect1, width=1)

    # Draws the rectengle writing 'Run AI Statistics' on it
    rect1 = pygame.Rect((5 * OFFSET, OFFSET + rect_height), (rect_width, rect_height))
    pygame.draw.rect(screen, (148, 126, 193), rect1, width=0)
    checkers_pygame.draw_text(screen, ' Run AI Statistics',
                              (5 * OFFSET, OFFSET + 4 * rect_height // 3),
                              26)
    rect1 = pygame.Rect((5 * OFFSET, OFFSET + rect_height), (rect_width + 1, rect_height + 1))
    pygame.draw.rect(screen, (0, 0, 0), rect1, width=1)

    # Draws the rectangles that have player type names on it for the Player1 block
    for x in range(0, len(PLAYER_TYPES)):
        rect = pygame.Rect((OFFSET, OFFSET + (x + 1) * rect_height), (rect_width, rect_height))
        pygame.draw.rect(screen, (224, 81, 42), rect, width=0)
        checkers_pygame.draw_text(screen, ' ' + PLAYER_TYPES[x],
                                  (OFFSET, OFFSET + (x + 1) * rect_height + rect_height // 3), 26)

        # draw the edges
        rect = pygame.Rect((OFFSET, OFFSET + (x + 1) * rect_height),
                           (rect_width + 1, rect_height + 1))
        pygame.draw.rect(screen, (0, 0, 0), rect, width=1)

    # Draws the rectangles that have player type names on it for the Player2 block
    for z in range(0, len(PLAYER_TYPES)):
        rect = pygame.Rect((3 * OFFSET, OFFSET + (z + 1) * rect_height), (rect_width, rect_height))
        pygame.draw.rect(screen, (155, 73, 83), rect, width=0)
        checkers_pygame.draw_text(screen, ' ' + PLAYER_TYPES[z],
                                  (3 * OFFSET, OFFSET + (z + 1) * rect_height + rect_height // 3),
                                  26)

        # draw the edges
        rect = pygame.Rect((3 * OFFSET, OFFSET + (z + 1) * rect_height),
                           (rect_width + 1, rect_height + 1))
        pygame.draw.rect(screen, (0, 0, 0), rect, width=1)


def green_box(p1: tuple, p2: tuple, screen: pygame.Surface) -> None:
    """
    Paints the square of the chosen player green.
    """

    # Colors the chosen box green for Player1
    if p1[2] != '':
        rect = pygame.Rect((p1[1] * OFFSET, OFFSET + (p1[2] + 1) * RECT_HEIGHT),
                           (RECT_WIDTH, RECT_HEIGHT))
        pygame.draw.rect(screen, (0, 255, 0), rect, width=0)
        checkers_pygame.draw_text(screen, ' ' + p1[0],
                                  (p1[1] * OFFSET,
                                   OFFSET + (p1[2] + 1) * RECT_HEIGHT + RECT_HEIGHT // 3), 26)
        pygame.display.update()
    # Colors the chosen box green for Player2
    if p2[2] != '':
        rect = pygame.Rect((p2[1] * OFFSET, OFFSET + (p2[2] + 1) * RECT_HEIGHT),
                           (RECT_WIDTH, RECT_HEIGHT))
        pygame.draw.rect(screen, (0, 255, 0), rect, width=0)
        checkers_pygame.draw_text(screen, ' ' + p2[0],
                                  (p2[1] * OFFSET,
                                   OFFSET + RECT_HEIGHT // 3 + (p2[2] + 1) * RECT_HEIGHT), 26)
        pygame.display.update()


def look_back_to_moves(moves_list: list) -> None:
    """
    After the game is finished, it allows you to look back to what moves made visually
    """
    size = (800, 800)
    allow = [pygame.MOUSEBUTTONDOWN]
    screen = checkers_pygame.initialize_screen(size, allow)

    # Draws the text 'Look back to moves made' on the screen
    text = 'Look back to moves made'
    pos = (300, 50)
    checkers_pygame.draw_text(screen, text, pos, 30)
    checkers_pygame.draw_text(screen, text, pos, 30)

    checkers_pygame.draw_moves(moves_list, screen)
    i = len(moves_list)
    y = OFFSET + 6 * RECT_SIZE
    x = OFFSET + 3 * RECT_SIZE

    while True:
        # handles the mouse events
        event = pygame.event.wait()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the left triangle, show the previous move
            if x - 40 <= event.pos[0] <= x - 1 and y + 20 <= event.pos[1] <= y + 60 and i >= 1:
                i -= 1
                checkers_pygame.draw_moves(moves_list[:i], screen)
            # If the user clicked on the right triangle, show the next move
            if x + 40 >= event.pos[0] > 1 + x and y + 20 <= event.pos[1] <= y + 60 and i <= len(
                    moves_list) - 1:
                i += 1
                checkers_pygame.draw_moves(moves_list[:i], screen)

        elif event.type == pygame.QUIT:
            pygame.display.quit()
            break


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ["pygame", "time", "pygame.colordict", "typing", "ai_players_final",
                          "checkers_game_with_pygame_final", "checkers_game_tree_final"],
        'allowed-io': [],
        'max-nested-blocks': 6,
        'max-line-length': 100,
        'disable': ['E1136'],
        'generated-members': ['pygame.*']
    })

    import python_ta.contracts
    python_ta.contracts.check_all_contracts()
