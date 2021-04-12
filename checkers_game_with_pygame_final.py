"""
CSC111 Winter 2021 Final Project: Building A Checkers AI Player

... (Description goes here.)

Copyright and Usage Information:
======================================

This file is provided solely for the use of the CSC111 Teaching team and for the
use of people who made this file, Mohamed Abdullahi, Benjamin Lee, Eren Findik and Sujoy
Deb Nath. Any other forms of distribution of this code is strictly prohibited without express
permission of the aforementioned group.

This file is Copyright (c) 2021 Sujoy Deb Nath, Benjamin Lee, Mohamed Abdullahi and Eren Findik.
"""

from typing import Dict, Optional, Tuple, List
import random
import pygame
from pygame.colordict import THECOLORS
import time

DIMENSION = 6
RECT_SIZE = 100
OFFSET = 100
START_POS_BLACK = {'a2', 'b1', 'c2', 'd1', 'e2', 'f1'}
START_POS_WHITE = {'a6', 'b5', 'c6', 'd5', 'e6', 'f5'}
VALID_POSITIONS = [letter + str(2 * x) for x in range(1, 4) for letter in 'ace'] + \
                  [letter + str(2 * x + 1) for x in range(0, 3) for letter in 'bdf']
PLAYER_COLORS = ('white', 'black')

MOVE_LIMIT = 35
PLAYER_TYPES = ['Random Player', 'Aggressive Player', 'Defensive Player', 'Human Player']


class Piece:
    """This class will be used to represent each counter/piece on the checkers board.
  It will keep track of where the piece is and what possible moves it can make, as well as
  the piece's color.
  Instance attributes:
      - white: Whether the color of this piece is white
      - position: The position of self on the board
      - is_crowned: Whether this piece is crowned or not.
  Representation Invariants:
      - self.position in VALID_POSITIONS
  """
    is_crowned: bool
    white: bool
    position: str

    def __init__(self, is_white: bool, start_pos: str) -> None:
        self.is_crowned = False
        self.white = is_white
        self.position = start_pos

    def crown_piece(self) -> None:
        """This method changes the crown attribute so that self is now crowned.
    self can now move in all diagonal adjacent squares.
    """
        if self.white is True:
            if self.position in ['b1', 'd1', 'f1']:
                self.is_crowned = True
        else:
            if self.position in ['a6', 'c6', 'e6']:
                self.is_crowned = True


class Checkers:
    """A class that represents the game checkers.
  Instance Attributes:
      - white_pieces: A dictionary mapping positions of the white pieces to the pieces themselves.
      - black_pieces: A dictionary mapping positions of the black pieces to the pieces themselves.
      - is_white_move: Whether white is the current player.
  Representation Invariants:
      - all(pos == self.white_pieces[pos].position for pos in self.white_pieces)
      - all(pos == self.black_pieces[pos].position for pos in self.black_pieces)
      - 0 <= len(self.white_pieces) <= 6
      - 0 <= len(self.black_pieces) <= 6
  """
    white_pieces: Dict[str, Piece]
    black_pieces: Dict[str, Piece]
    is_white_move: bool
    screen: pygame.Surface

    def __init__(self, white: Optional[Dict[str, Piece]] = None,
                 black: Optional[Dict[str, Piece]] = None,
                 curr_player: Optional[bool] = None) -> None:

        # Mainly for being able to copy the board
        if white is not None and black is not None and curr_player is not None:
            self.white_pieces = white
            self.black_pieces = black
            self.is_white_move = curr_player

        else:  # For starting a new game.
            self.white_pieces = {pos: Piece(is_white=True, start_pos=pos)
                                 for pos in START_POS_WHITE}

            self.black_pieces = {pos: Piece(is_white=False, start_pos=pos)
                                 for pos in START_POS_BLACK}

            self.is_white_move = True

    def set_screen(self, screen: pygame.Surface) -> None:
        """
        Sets the ..
        """
        self.screen = screen

    def get_winner(self, move_count) -> Optional[str]:
        """Return the winner of the game, if there is one or if it is a draw.
    Return None if the move limit has not been reached and there is no winner yet.
    """
        if len(self.black_pieces) == 0:
            return 'white'
        elif len(self.white_pieces) == 0:
            return 'black'
        elif move_count == MOVE_LIMIT or self.get_valid_moves() == []:
            return 'draw'
        else:
            return None

    def make_move(self, move: tuple[str, str, str]) -> None:
        """
        Makes a move based on the tuple, move.
        The first element of the tuple is the initial position of the game piece
        The second element is the position of the piece that was jumped over/captured.
        (Can be an empty string if no capture was made.)
        The third element is the final position of the piece.
        Preconditions:
            - move[2] not in self.white_pieces or move[2] not in self.black_pieces
        """
        if self.is_white_move:
            piece = self.white_pieces[move[0]]
            if move[1] != '':
                #   the piece on that position is captured and removed from the game
                self.capture(move[1])

            self.white_pieces[move[2]] = piece
            piece.position = move[2]
            self.white_pieces.pop(move[0])

        else:
            piece = self.black_pieces[move[0]]
            if move[1] != '':
                #   the piece on that position is captured and removed from the game
                self.capture(move[1])

            self.black_pieces[move[2]] = piece
            piece.position = move[2]
            self.black_pieces.pop(move[0])

    def make_move_pygame(self, move: tuple[str, str, str], screen) -> None:
        """
        Makes a move based on the tuple, move.
        The first element of the tuple is the initial position of the game piece
        The second element is the position of the piece that was jumped over/captured.
        (Can be an empty string if no capture was made.)
        The third element is the final position of the piece.
        Preconditions:
            - move[2] not in self.white_pieces or move[2] not in self.black_pieces
        """
        if self.is_white_move:
            piece = self.white_pieces[move[0]]
            if move[1] != '':
                #   the piece on that position is captured and removed from the game
                self.capture(move[1])
                # handles the pygame
                y, x = pos_to_square(move[1])
                rect = pygame.Rect((OFFSET + y * RECT_SIZE, OFFSET + x * RECT_SIZE),
                                   (RECT_SIZE, RECT_SIZE))
                pygame.draw.rect(screen, (84, 84, 84), rect, width=0)
            self.white_pieces[move[2]] = piece
            piece.position = move[2]
            self.white_pieces.pop(move[0])

            # handles the pygame
            y, x = pos_to_square(move[0])
            rect2 = pygame.Rect((OFFSET + y * RECT_SIZE, OFFSET + x * RECT_SIZE),
                                (RECT_SIZE, RECT_SIZE))
            pygame.draw.rect(screen, (84, 84, 84), rect2, width=0)

            # draws the piece again
            if piece.is_crowned:
                draw_crown(move, screen, (245, 245, 245))
            else:
                y, x = pos_to_square(move[2])
                start = (
                    OFFSET + RECT_SIZE // 2 + y * RECT_SIZE,
                    OFFSET + RECT_SIZE // 2 + x * RECT_SIZE)
                pygame.draw.circle(screen, (0, 0, 0), start, 31, 1)
                pygame.draw.circle(screen, (245, 245, 245), start, 30, 0)
        else:
            piece = self.black_pieces[move[0]]
            if move[1] != '':
                #   the piece on that position is captured and removed from the game
                self.capture(move[1])
                # handles the pygame
                y, x = pos_to_square(move[1])
                rect = pygame.Rect((OFFSET + y * RECT_SIZE, OFFSET + x * RECT_SIZE),
                                   (RECT_SIZE, RECT_SIZE))
                pygame.draw.rect(screen, (84, 84, 84), rect, width=0)
            self.black_pieces[move[2]] = piece
            piece.position = move[2]
            self.black_pieces.pop(move[0])

            # handles the pygame
            y, x = pos_to_square(move[0])
            rect2 = pygame.Rect((OFFSET + y * RECT_SIZE, OFFSET + x * RECT_SIZE),
                                (RECT_SIZE, RECT_SIZE))
            pygame.draw.rect(screen, (84, 84, 84), rect2, width=0)

            # draws the piece again
            if piece.is_crowned:
                draw_crown(move, screen, (50, 50, 50))
            else:
                y, x = pos_to_square(move[2])
                start = (OFFSET + RECT_SIZE // 2 + y * RECT_SIZE,
                         OFFSET + RECT_SIZE // 2 + x * RECT_SIZE)
                pygame.draw.circle(screen, (0, 0, 0), start, 31, 1)
                pygame.draw.circle(screen, (50, 50, 50), start, 30, 0)

    def capture(self, position: str) -> None:
        """
        removes the piece that is on the given position from the game
        """
        if self.is_white_move:
            self.black_pieces.pop(position)
        else:
            self.white_pieces.pop(position)

    def get_neighbours(self, piece: Piece) -> list:
        """Returns the pieces diagonal to the piece. The list contains tuples where the
        of length two. If it is impossible for a piece to be diagonal, the tuple is empty.
        The first index in the tuple says 'none' if there is no piece, 'same' if the
        piece is the same colour, diff if the piece is a different colour. The second index contains
        the position"""
        position = piece.position
        # Gets the coordinates of the corners
        top_right = chr(ord(position[0]) + 1) + str(int(position[1]) + 1)
        top_left = chr(ord(position[0]) - 1) + str(int(position[1]) + 1)
        bottom_right = chr(ord(position[0]) + 1) + str(int(position[1]) - 1)
        bottom_left = chr(ord(position[0]) - 1) + str(int(position[1]) - 1)
        # Puts the corners in a list
        corners = [top_right, top_left, bottom_right, bottom_left]
        neighbours_so_far = []
        for i in range(0, 4):
            # Means that it is not on the game board
            if corners[i] not in VALID_POSITIONS:
                neighbours_so_far.append(())
            # The space is not occupied
            elif (corners[i] not in self.white_pieces and
                  corners[i] not in self.black_pieces):
                neighbours_so_far.append(('none', corners[i]))
            # The space is occupied by a white piece
            elif corners[i] in self.white_pieces:
                if piece.white:
                    neighbours_so_far.append(('same', corners[i]))
                else:
                    neighbours_so_far.append(('diff', corners[i]))
            # The space is occupied by a black piece
            elif corners[i] in self.black_pieces:
                if piece.white:
                    neighbours_so_far.append(('diff', corners[i]))
                else:
                    neighbours_so_far.append(('same', corners[i]))
        return neighbours_so_far

    def get_valid_moves(self) -> List[tuple]:
        """Returns all the valid moves for a player. The valid moves are stored as a tuple,
        where the first index is the initial position, the second is empty if no capture is made
        otherwise, it contains the position of the piece captured, and the third is the final
        position
        """

        capture_moves = []
        non_capture_moves = []
        if self.is_white_move:
            pieces_to_check = [self.white_pieces[piece] for piece in self.white_pieces]
        else:
            pieces_to_check = [self.black_pieces[piece] for piece in self.black_pieces]
        for piece in pieces_to_check:
            moves, is_capture = self.get_valid_move_piece(piece)
            if is_capture:
                capture_moves.extend(moves)
            else:
                non_capture_moves.extend(moves)
        if capture_moves != []:
            return capture_moves
        else:
            return non_capture_moves

    def get_valid_move_piece(self, piece) -> Tuple[list, bool]:
        """Returns all the valid moves for a piece. The valid moves are stored as a tuple,
        where the first index is the initial position, the second is empty if no capture is made
        otherwise, it contains the position of the piece captured, and the third is the final
        position"""
        capture_moves = []
        non_capture_moves = []
        corners = self.get_neighbours(piece)
        # Checks the bottom two corners to see find valid moves.
        if piece.white and not piece.is_crowned:
            start = 2
            end = 4
        # Checks the top to corners to see valid moves
        elif not (piece.white or piece.is_crowned):
            start = 0
            end = 2
        # Checks all diagonals
        else:
            start = 0
            end = 4
        for i in range(start, end):
            corner = corners[i]
            if corner == ():
                continue
            elif corner[0] == 'none':
                non_capture_moves.append((piece.position, '', corner[1]))
            elif corner[0] == 'diff':
                letter = chr(ord(corner[1][0]) - ord(piece.position[0]) + ord(corner[1][0]))
                num = str(int(corner[1][1]) - int(piece.position[1]) + int(corner[1][1]))
                check = letter + num
                if check not in self.white_pieces and check not in self.black_pieces and \
                        check in VALID_POSITIONS:
                    capture_moves.append((piece.position, corner[1], check))
        if capture_moves != []:
            return (capture_moves, True)
        else:
            return (non_capture_moves, False)


class Player:
    """
    An abstract class representing a checkers player.
    This class will be used to create subclasses of different players
    """

    def make_move(self, game: Checkers, previous_move: tuple[str, str, str],
                  continuing_from_previous_move: bool) -> tuple[str, str, str]:
        """
        Make a move based on the given checkers game
        Preconditions:
            - There should at least be one valid moves.
        """
        raise NotImplementedError

def run_game(white: Player, black: Player) -> tuple[str, list[tuple[bool, tuple[str, str, str]]]]:
    """
    Runs the checkers game and returns a tuple.
    The first element of the tuple is the winner of the game, corresponding to the return
    values of the get_winner() method in Checkers().
    The second element is a list of tuples, corresponding to the moves made in the game.
        - The first element of the tuple corresponds to if the player who made that move was
        white.
        - The second element corresponds to the move tuple as defined in the make_move method
        of Checkers().
    """

    game_board = Checkers()
    moves_so_far = []
    is_continued = False
    previous_move = ('', '', '')

    while game_board.get_winner(len(moves_so_far)) is None:
        if game_board.is_white_move:
            move = white.make_move(game_board, previous_move, is_continued)
        else:
            move = black.make_move(game_board, previous_move, is_continued)
        is_continued = False

        game_board.make_move(move)
        # alternate crowning
        if game_board.is_white_move:
            piece = game_board.white_pieces[move[2]]
            if not piece.is_crowned and move[2][1] == '1':
                piece.crown_piece()

        else:
            piece = game_board.black_pieces[move[2]]
            if not piece.is_crowned and move[2][1] == '6':
                piece.crown_piece()
        if move[1] != '':
            is_continued = game_board.get_valid_move_piece(piece)[1]
        moves_so_far.append((game_board.is_white_move, move))

        if is_continued is not True:
            # Change who is current player
            game_board.is_white_move = not game_board.is_white_move

        previous_move = move

    return (game_board.get_winner(len(moves_so_far)), moves_so_far)


def run_game_pygame(white: Player, black: Player) -> tuple[str, list]:
    """
    Runs the game
    """

    game_board = Checkers()
    moves_so_far = []
    is_continued = False
    previous_move = ''
    move_count = 0

    size = (800, 800)
    allow = [pygame.MOUSEBUTTONDOWN, pygame.quit()]
    screen = initialize_screen(size, allow)
    game_board.set_screen(screen)
    create_board(game_board, screen)

    while game_board.get_winner(move_count) is None:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.display.quit()
        moves_left(MOVE_LIMIT - move_count - 1, screen)
        if not (game_board.is_white_move and isinstance(white, HumanPlayer)) and not (
                not game_board.is_white_move and isinstance(black, HumanPlayer)):
            time.sleep(1)
        if game_board.is_white_move:
            move = white.make_move(game_board, previous_move, is_continued)
        else:
            move = black.make_move(game_board, previous_move, is_continued)

        game_board.make_move_pygame(move, screen)

        # alternate crowning
        if game_board.is_white_move:
            piece = game_board.white_pieces[move[2]]
            if not piece.is_crowned and move[2][1] == '1':
                piece.crown_piece()
                draw_crown(move, screen, (245, 245, 245))

        else:
            piece = game_board.black_pieces[move[2]]
            if not piece.is_crowned and move[2][1] == '6':
                piece.crown_piece()
                draw_crown(move, screen, (50, 50, 50))
        if move[1] != '':
            is_continued = game_board.get_valid_move_piece(piece)[1]
        if is_continued is not True:
            # Change who is current player
            game_board.is_white_move = not game_board.is_white_move
        move_count += 1

        moves_so_far.append(move)
        previous_move = move

        pygame.display.update()
    time.sleep(2)
    pygame.display.quit()
    return (game_board.get_winner(move_count), moves_so_far)


def draw_crown(move: tuple[str, str, str], screen: pygame.Surface,
               color: tuple[int, int, int]) -> None:
    y, x = pos_to_square(move[2])
    rect2 = pygame.Rect((OFFSET + y * RECT_SIZE, OFFSET + x * RECT_SIZE),
                        (RECT_SIZE, RECT_SIZE))
    pygame.draw.rect(screen, (84, 84, 84), rect2, width=0)
    left = OFFSET + y * RECT_SIZE
    top = OFFSET + x * RECT_SIZE
    # points = [(left + 30, top + 10), (left + 50, top + 10), (left + 50, top + 30),
    #           (left + 70, top + 30), (left + 70, top + 50), (left + 50, top + 50),
    #           (left + 50, top + 70), (left + 30, top + 70), (left + 30, top + 50),
    #           (left + 10, top + 50), (left + 10, top + 30), (left + 30, top + 30)]
    points = [(left + 35, top + 10), (left + 60, top + 10), (left + 60, top + 35),
              (left + 85, top + 35), (left + 85, top + 60), (left + 60, top + 60),
              (left + 60, top + 85), (left + 35, top + 85), (left + 35, top + 60),
              (left + 10, top + 60), (left + 10, top + 35), (left + 35, top + 35)]
    pygame.draw.polygon(screen, color, points)


def initialize_screen(screen_size: tuple[int, int], allowed: list) -> pygame.Surface:
    """Initialize pygame and the display window.
    allowed is a list of pygame event types that should be listened for while pygame is running.
    """
    pygame.display.init()
    pygame.font.init()
    screen = pygame.display.set_mode(screen_size)
    screen.fill(THECOLORS['white'])
    pygame.display.flip()

    return screen


def moves_left(count, screen: pygame.Surface) -> None:
    rect = pygame.Rect(100, 0, 400, 90)
    pygame.draw.rect(screen, (255, 255, 255), rect, width=0)

    text = str(count) + ' moves left'
    pos = (300, 50)

    draw_text(screen, text, pos, 30)


def draw_text(screen: pygame.Surface, text: str, pos: tuple[int, int], size: int) -> None:
    """Draw the given text to the pygame screen at the given position.

    pos represents the *upper-left corner* of the text.
    """
    font = pygame.font.SysFont('inconsolata', size)
    text_surface = font.render(text, True, THECOLORS['black'])
    width, height = text_surface.get_size()
    screen.blit(text_surface,
                pygame.Rect(pos, (pos[0] + width, pos[1] + height)))


def create_board(game: Checkers, screen: pygame.Surface) -> None:
    """
    creates board
    """

    # draws the squares
    for x in range(0, DIMENSION):
        for y in range(0, DIMENSION):
            rect = pygame.Rect((OFFSET + y * RECT_SIZE, OFFSET + x * RECT_SIZE),
                               (RECT_SIZE, RECT_SIZE))
            pygame.draw.rect(screen, num_to_color(x, y), rect, width=0)

    # draws the borders
    rect = pygame.Rect((OFFSET - 2, OFFSET - 2),
                       (RECT_SIZE * DIMENSION + 4, RECT_SIZE * DIMENSION + 4))
    pygame.draw.rect(screen, (0, 0, 0), rect, width=3)

    for piece in game.black_pieces.keys():
        draw_piece(screen, piece, 'black')

    for piece in game.white_pieces.keys():
        draw_piece(screen, piece, 'white')

    pygame.display.flip()
    pygame.event.wait()
    # pygame.display.quit()


def draw_piece(screen: pygame.Surface, pos: str, color: str):
    """
    Representation Invariants:
    - color in {'black', 'white'}
    """
    rgb = ()
    if color == 'black':
        rgb = (50, 50, 50)
    else:
        rgb = (245, 245, 245)
    s = pos_to_square(pos)
    start = (
        OFFSET + RECT_SIZE // 2 + s[0] * RECT_SIZE, OFFSET + RECT_SIZE // 2 + s[1] * RECT_SIZE)
    pygame.draw.circle(screen, (0, 0, 0), start, 34, 1)
    pygame.draw.circle(screen, rgb, start, 33, 0)


def pos_to_square(pos: str) -> tuple:
    """
    posiiton to tuple
    """
    return ((ord(pos[0]) - 97), int(pos[1]) - 1)


def square_to_pos(pos: tuple[int, int]) -> str:
    """
    posiiton to tuple
    """

    x = ((pos[0] - OFFSET) // RECT_SIZE) + 1
    y = ((pos[1] - OFFSET) // RECT_SIZE) + 1

    if pos[0] >= OFFSET and pos[1] >= OFFSET and x <= 6 and y <= 6:
        return chr(96 + x) + str(y)
    else:
        return ''


def num_to_color(x: int, y: int) -> tuple:
    if (x + y) % 2 == 0:
        return (255, 255, 255)
    else:
        return (84, 84, 84)


def position_to_index(pos: tuple[int, int]) -> Optional[tuple[int, int]]:
    """
    Used when finding out which square the user clicked in choose_player window.
    """
    rect_height = 70
    rect_width = 150

    if OFFSET + rect_height <= pos[1] <= (
            len(PLAYER_TYPES) + 1) * rect_height + OFFSET and OFFSET <= pos[
        0] <= OFFSET + rect_width:
        i = (pos[1] - OFFSET - rect_height) // rect_height
        return (1, i)
    elif OFFSET + rect_height <= pos[1] <= (
            len(PLAYER_TYPES) + 1) * rect_height + OFFSET and 3 * OFFSET <= pos[
        0] <= 3 * OFFSET + rect_width:
        i = (pos[1] - OFFSET - rect_height) // rect_height
        return (3, i)
    else:
        return None


def find_pieces_between(pos1: str, pos2: str, game: Checkers) -> str:
    y = str((int(pos1[1]) + int(pos2[1])) // 2)
    x = chr((ord(pos1[0]) + ord(pos2[0])) // 2)

    coordinate = x + y

    if game.is_white_move and coordinate in game.black_pieces.keys():
        return coordinate
    elif not game.is_white_move and coordinate in game.white_pieces.keys():
        return coordinate
    else:
        return ''


class HumanPlayer(Player):
    """
    A player that is run by a human
    """
    _clicking: bool
    clicked: str
    released: str

    def __init__(self) -> None:
        self.clicked = ''
        self.released = ''

    def make_move(self, game: Checkers, previous_move: tuple[str, str, str],
                  continuing_from_previous_move: bool) -> tuple[str, str, str]:

        while True:
            event = pygame.event.wait()

            if (game.is_white_move and event.type == pygame.MOUSEBUTTONDOWN and square_to_pos(
                    event.pos) in game.white_pieces.keys()) or (
                    not game.is_white_move and event.type == pygame.MOUSEBUTTONDOWN and square_to_pos(
                event.pos) in game.black_pieces.keys()):
                self.clicked = square_to_pos(event.pos)

            event = pygame.event.wait()

            if event.type == pygame.MOUSEBUTTONDOWN and self.clicked != '':
                self.released = square_to_pos(event.pos)
                if self.released != '':
                    other_piece = find_pieces_between(self.clicked, self.released, game)
                    move = (self.clicked, other_piece, self.released)

                    if move in game.get_valid_moves():
                        return move
                    else:
                        self._clicking: False
                        self.clicked: ''
                        self.released: ''
