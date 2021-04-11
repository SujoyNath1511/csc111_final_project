from typing import Dict, Optional, Tuple, List
import random
import pygame
from pygame.colordict import THECOLORS
import time

from AI_players_v2 import AggressivePlayer, RandomPlayer, DefensivePlayer
import checkers_game_tree_v5 as checkers_game_tree
import checkers_game_with_pygame_v5 as checkers_pygame

DIMENSION = 6
RECT_SIZE = 80
OFFSET = 100
START_POS_BLACK = {'a2', 'b1', 'c2', 'd1', 'e2', 'f1'}
START_POS_WHITE = {'a6', 'b5', 'c6', 'd5', 'e6', 'f5'}
VALID_POSITIONS = [letter + str(2 * x) for x in range(1, 4) for letter in 'ace'] + \
                  [letter + str(2 * x + 1) for x in range(0, 3) for letter in 'bdf']
PLAYER_COLORS = ('white', 'black')

MOVE_LIMIT = 35
PLAYER_TYPES = ['Random Player', 'Aggressive Player', 'Defensive Player']


def choose_players() -> tuple[checkers_pygame.Player, checkers_pygame.Player]:
    player1 = None
    player2 = None
    player1_st = ('', '', '')
    player2_st = ('', '', '')
    rect_height = 70
    rect_width = 150

    list_of_games = checkers_game_tree.read_moves_from_csv('game_tree_data.csv')
    game_tree = checkers_game_tree.build_game_tree_from_list(list_of_games)

    player_dict = {'Random Player': RandomPlayer(), 'Aggressive Player': AggressivePlayer(game_tree),
                   'Defensive Player': DefensivePlayer(game_tree)}
    size = (800, 800)

    allow = [pygame.MOUSEBUTTONDOWN]
    screen = checkers_pygame.initialize_screen(size, allow)
    checkers_pygame.draw_choose_players(screen)

    while True:
        checkers_pygame.draw_choose_players(screen)
        checkers_pygame.green_box(player1_st, player2_st, screen)
        pygame.display.update()
        event = pygame.event.wait()

        if event.type == pygame.MOUSEBUTTONDOWN:
            green = checkers_pygame.position_to_index(event.pos)
            print(green)
            if green is not None:
                if green[0] == 3 and player2 is None:
                    player2 = player_dict[PLAYER_TYPES[green[1]]]
                    player2_st = (PLAYER_TYPES[green[1]], green[0], green[1])
                elif green[0] == 1 and player1 is None:
                    player1 = player_dict[PLAYER_TYPES[green[1]]]
                    player1_st = (PLAYER_TYPES[green[1]], green[0], green[1])
            else:
                if 5 * OFFSET <= event.pos[0] <= 5 * OFFSET + rect_width and OFFSET <= event.pos[1] \
                        <= OFFSET + rect_height:
                    # start the game
                    if player1 is None or player2 is None:
                        rect3 = pygame.Rect((5 * OFFSET, OFFSET), (rect_height, rect_width))
                        pygame.draw.rect(screen, (255, 0, 0), rect3, width=0)
                        checkers_pygame.draw_text(screen, ' Start the Game', (5 * OFFSET, OFFSET))
                    else:
                        return (player1, player2)

        elif event.type == pygame.QUIT:
            break
        pygame.display.update()
