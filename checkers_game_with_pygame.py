"""
This is a test file for the checkers game.
"""

from typing import Dict, Optional, Tuple, List
import random
import pygame
from pygame.colordict import THECOLORS
import time

DIMENSION = 6
RECT_SIZE = 80
OFFSET = 100
START_POS_BLACK = {'a2', 'b1', 'c2', 'd1', 'e2', 'f1'}
START_POS_WHITE = {'a6', 'b5', 'c6', 'd5', 'e6', 'f5'}
VALID_POSITIONS = [letter + str(2 * x) for x in range(1, 4) for letter in 'ace'] + \
                  [letter + str(2 * x + 1) for x in range(0, 3) for letter in 'bdf']
PLAYER_COLORS = ('white', 'black')

MOVE_LIMIT = 40


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
      - white_pieces: A list of all the white pieces.
      - black_pieces: A list of all the black pieces
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

    def make_move(self, move: tuple[str, str, str], screen) -> None:
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
                start = (
                OFFSET + RECT_SIZE // 2 + y * RECT_SIZE, OFFSET + RECT_SIZE // 2 + x * RECT_SIZE)
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

    def make_move(self, game: Checkers, previous_move: str, continuing_from_previous_move: bool) -> \
    tuple[tuple[str, str, str], bool]:
        """
        Make a move based on the given checkers game
        Preconditions:
            - There should at least be one valid moves.
        """
        raise NotImplementedError


class RandomPlayer(Player):
    """
    Just a random player
    """

    def make_move(self, game: Checkers, previous_move: str, continuing_from_previous_move: bool) -> \
    tuple[tuple[str, str, str], bool]:
        """
        makes a random move from valid moves
        """
        moves = game.get_valid_moves()
        return (random.choice(moves), False)


def run_game(white: Player, black: Player) -> tuple[str, list]:
    """
    Runs the game
    """

    game_board = Checkers()
    moves_so_far = []
    is_continued = False
    previous_move = ''
    move_count = 0

    size = (800, 800)
    allow = [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]
    screen = initialize_screen(size, allow)
    create_board(game_board, screen)

    while game_board.get_winner(move_count) is None:
        time.sleep(1)
        if game_board.is_white_move:
            move, is_continued = white.make_move(game_board, previous_move, is_continued)
        else:
            move, is_continued = black.make_move(game_board, previous_move, is_continued)

        # if game_board.get_valid_moves() != []: # We have to get rid of this if statement -Why are there no moves valid?
        game_board.make_move(move, screen)

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

        if is_continued is not True:
            # Change who is current player
            game_board.is_white_move = not game_board.is_white_move
        move_count += 1

        moves_so_far.append(move)
        previous_move = move

        # does the crowning- what we have talked
        # if game_board.is_white_move and move[2][1] == 1:
        #     piece = game_board.white_pieces[move[2][1]]
        #     piece.crown_piece()
        # elif not game_board.is_white_move and move[2][1] == 6:
        #     # (also assuming that the piece is not already crowned)
        #     piece = game_board.black_pieces[move[2][1]]
        #     piece.crown_piece()
        #
        pygame.display.update()
        event = pygame.event.wait()
        # if event.type == pygame.QUIT:
        #     pygame.display.quit()
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
    points = [(left + 30, top + 10), (left + 50, top + 10), (left + 50, top + 30),
              (left + 70, top + 30), (left + 70, top + 50), (left + 50, top + 50),
              (left + 50, top + 70), (left + 30, top + 70), (left + 30, top + 50),
              (left + 10, top + 50), (left + 10, top + 30), (left + 30, top + 30)]
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

    # pygame.event.clear()
    # pygame.event.set_blocked(None)
    # pygame.event.set_allowed([pygame.QUIT] + allowed)

    return screen


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

    # draws the pieces:
    for piece in game.black_pieces.keys():
        s = pos_to_square(piece)
        start = (
        OFFSET + RECT_SIZE // 2 + s[0] * RECT_SIZE, OFFSET + RECT_SIZE // 2 + s[1] * RECT_SIZE)
        pygame.draw.circle(screen, (0, 0, 0), start, 31, 1)
        pygame.draw.circle(screen, (50, 50, 50), start, 30, 0)

    for piece in game.white_pieces.keys():
        s = pos_to_square(piece)
        start = (
        OFFSET + RECT_SIZE // 2 + s[0] * RECT_SIZE, OFFSET + RECT_SIZE // 2 + s[1] * RECT_SIZE)
        pygame.draw.circle(screen, (0, 0, 0), start, 31, 1)
        pygame.draw.circle(screen, (245, 245, 245), start, 30, 0)

    pygame.display.flip()
    pygame.event.wait()
    # pygame.display.quit()


def pos_to_square(pos: str) -> tuple:
    """
    posiiton to tuple
    """
    return ((ord(pos[0]) - 97), int(pos[1]) - 1)


def num_to_color(x: int, y: int) -> tuple:
    if (x + y) % 2 == 0:
        return (255, 255, 255)
    else:
        return (84, 84, 84)


if __name__ == '__main__':
    game = run_game(RandomPlayer(), RandomPlayer())
    print('The winner:' + game[0])
    print(game[1])
