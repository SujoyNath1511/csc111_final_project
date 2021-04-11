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
PLAYER_TYPES = ['Random Player', 'Aggressive Player', 'Defensive Player', 'Human Player']


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
                   'Defensive Player': DefensivePlayer(game_tree), 'Human Player': checkers_pygame.HumanPlayer()}
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
                        draw_text(screen, ' Start the Game', (5 * OFFSET, OFFSET))
                    else:
                        return (player1, player2)

        elif event.type == pygame.QUIT:
            break
        pygame.display.update()


def draw_choose_players(screen: pygame.Surface) -> None:
    rect_height = 70
    rect_width = 150

    screen.fill((23, 153, 195))
    rect1 = pygame.Rect((OFFSET, OFFSET), (rect_width, rect_height))
    pygame.draw.rect(screen, (93, 73, 83), rect1, width=0)
    draw_text(screen, ' Player1', (OFFSET, OFFSET + rect_height // 3))
    rect1 = pygame.Rect((OFFSET, OFFSET), (rect_width + 1, rect_height + 1))
    pygame.draw.rect(screen, (0, 0, 0), rect1, width=1)

    rect2 = pygame.Rect((3 * OFFSET, OFFSET), (rect_width, rect_height))
    pygame.draw.rect(screen, (93, 73, 83), rect2, width=0)
    draw_text(screen, ' Player2', (3 * OFFSET, OFFSET + rect_height // 3))
    rect1 = pygame.Rect((3 * OFFSET, OFFSET), (rect_width + 1, rect_height + 1))
    pygame.draw.rect(screen, (0, 0, 0), rect1, width=1)

    rect3 = pygame.Rect((5 * OFFSET, OFFSET), (rect_width, rect_height))
    pygame.draw.rect(screen, (148, 126, 193), rect3, width=0)
    draw_text(screen, ' Start the Game', (5 * OFFSET, OFFSET + rect_height // 3))
    rect1 = pygame.Rect((5 * OFFSET, OFFSET), (rect_width + 1, rect_height + 1))
    pygame.draw.rect(screen, (0, 0, 0), rect1, width=1)

    for x in range(0, len(PLAYER_TYPES)):
        rect = pygame.Rect((OFFSET, OFFSET + (x + 1) * rect_height), (rect_width, rect_height))
        pygame.draw.rect(screen, (224, 81, 42), rect, width=0)
        draw_text(screen, ' ' + PLAYER_TYPES[x],
                  (OFFSET, OFFSET + (x + 1) * rect_height + rect_height // 3))

        # draw the edges
        rect = pygame.Rect((OFFSET, OFFSET + (x + 1) * rect_height),
                           (rect_width + 1, rect_height + 1))
        pygame.draw.rect(screen, (0, 0, 0), rect, width=1)

    for x in range(0, len(PLAYER_TYPES)):
        rect = pygame.Rect((3 * OFFSET, OFFSET + (x + 1) * rect_height), (rect_width, rect_height))
        pygame.draw.rect(screen, (155, 73, 83), rect, width=0)
        draw_text(screen, ' ' + PLAYER_TYPES[x],
                  (3 * OFFSET, OFFSET + (x + 1) * rect_height + rect_height // 3))

        # draw the edges
        rect = pygame.Rect((3 * OFFSET, OFFSET + (x + 1) * rect_height),
                           (rect_width + 1, rect_height + 1))
        pygame.draw.rect(screen, (0, 0, 0), rect, width=1)


def green_box(p1: tuple, p2: tuple, screen: pygame.Surface) -> None:
    rect_height = 70
    rect_width = 150

    if p1[2] != '':
        rect = pygame.Rect((p1[1] * OFFSET, OFFSET + (p1[2] + 1) * rect_height),
                           (rect_width, rect_height))
        pygame.draw.rect(screen, (0, 255, 0), rect, width=0)
        draw_text(screen, ' ' + p1[0],
                  (p1[1] * OFFSET, OFFSET + (p1[2] + 1) * rect_height + rect_height // 3))
        pygame.display.update()
    if p2[2] != '':
        rect = pygame.Rect((p2[1] * OFFSET, OFFSET + (p2[2] + 1) * rect_height),
                           (rect_width, rect_height))
        pygame.draw.rect(screen, (0, 255, 0), rect, width=0)
        draw_text(screen, ' ' + p2[0],
                  (p2[1] * OFFSET, OFFSET + rect_height // 3 + (p2[2] + 1) * rect_height))
        pygame.display.update()


def draw_text(screen: pygame.Surface, text: str, pos: tuple[int, int]) -> None:
    """Draw the given text to the pygame screen at the given position.

    pos represents the *upper-left corner* of the text.
    """
    font = pygame.font.SysFont('inconsolata', 26)
    text_surface = font.render(text, True, THECOLORS['black'])
    width, height = text_surface.get_size()
    screen.blit(text_surface,
                pygame.Rect(pos, (pos[0] + width, pos[1] + height)))
