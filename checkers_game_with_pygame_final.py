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
import time
import pygame


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
            if self.position in ['b1', 'd1', 'f1']:  # The top end of the board
                self.is_crowned = True
        else:
            if self.position in ['a6', 'c6', 'e6']:  # The bottom end of the board
                self.is_crowned = True


class Checkers:
    """A class that represents the game checkers.
  Instance Attributes:
      - white_pieces: A dictionary mapping positions of the white pieces to the pieces themselves.
      - black_pieces: A dictionary mapping positions of the black pieces to the pieces themselves.
      - is_white_move: Whether white is the current player.
      - screen: An optional pygame Surface object that represents the pygame window.
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

    def get_winner(self, move_count: int) -> Optional[str]:
        """Return the winner of the game, if there is one or if it is a draw.
        Return None if the move limit has not been reached and there is no winner yet.
        Preconditions:
            - 0 <= move_count <= MOVE_LIMIT
        """
        if len(self.black_pieces) == 0:
            # There are no black pieces left on the board.
            return 'white'
        elif len(self.white_pieces) == 0:
            # There are no white pieces left on the board.
            return 'black'
        elif move_count == MOVE_LIMIT or self.get_valid_moves() == []:
            # The move limit has been reached, or a player can't make any moves.
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
            pieces = self.white_pieces
        else:
            piece = self.black_pieces[move[0]]
            pieces = self.black_pieces
        if move[1] != '':
            #   the piece on that position is captured and removed from the game
            self.capture(move[1])
        pieces[move[2]] = piece
        piece.position = move[2]
        pieces.pop(move[0])

    def make_move_pygame(self, move: tuple[str, str, str], screen: pygame.Surface) -> None:
        """
        This is the make_move method, but with pygame methods added on inorder
        to visualize a move being made.
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
        Removes the piece that is on the given position from the game board.
        """
        if self.is_white_move:
            self.black_pieces.pop(position)
        else:
            self.white_pieces.pop(position)

    def get_neighbours(self, piece: Piece) -> List[tuple]:
        """Returns the pieces diagonal to piece. The list contains tuples of length two if it is a
        space on the board. If it is impossible for a piece to be diagonal, the tuple is empty.
        The first index in the tuple says 'none' if there is no piece, 'same' if the piece is the
        same colour, diff if the piece is a different colour. The second index contains
        the position
        Preconditions:
            - (piece in self.black_pieces) or (piece in self.white_pieces)
        """
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
            elif corners[i] not in self.white_pieces and corners[i] not in self.black_pieces:
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

    def get_valid_moves(self) -> List[Tuple[str, str, str]]:
        """Returns all the valid moves for a player. The valid moves are stored as a tuple,
        where the first index is the initial position, the second is empty if no capture is made
        otherwise, it contains the position of the piece captured, and the third is the final
        position"""

        capture_moves = []
        non_capture_moves = []
        if self.is_white_move:
            pieces_to_check = [self.white_pieces[piece] for piece in self.white_pieces]
        else:
            pieces_to_check = [self.black_pieces[piece] for piece in self.black_pieces]
        for piece_to_check in pieces_to_check:
            moves, is_capture = self.get_valid_move_piece(piece_to_check)
            if is_capture:
                capture_moves.extend(moves)
            else:
                non_capture_moves.extend(moves)
        if capture_moves != []:
            return capture_moves
        else:
            return non_capture_moves

    def get_valid_move_piece(self, piece: Piece) -> Tuple[List[Tuple[str, str, str]], bool]:
        """Returns a tuple where the first index is a list of all the valid moves for a piece and
        the second index is whether they are capture moves. The valid moves are stored as a tuple,
        where the first index is the initial position, the second is empty if no capture is made
        otherwise, it contains the position of the piece captured, and the third is the final
        position.
        Preconditions:
            - (piece in self.black_pieces) or (piece in self.white_pieces)
        """
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
                # Finds the letter of the piece's final position after a jump
                letter = chr(ord(corner[1][0]) - ord(piece.position[0]) + ord(corner[1][0]))
                # Finds the number of the piece's final position after a jump
                num = str(int(corner[1][1]) - int(piece.position[1]) + int(corner[1][1]))
                check = letter + num
                # Checks to see if the position after jump is valid and empty
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


def copy_game(game: Checkers) -> Checkers:
    """
    Returns a copy of the checkers game given
    """
    new_game = Checkers(game.white_pieces, game.black_pieces, game.is_white_move)
    return new_game


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
        # makes the moves
        if game_board.is_white_move:
            move = white.make_move(game_board, previous_move, is_continued)
        else:
            move = black.make_move(game_board, previous_move, is_continued)
        is_continued = False

        game_board.make_move(move)
        # does the crowning
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
    Works exactly as run_game but it also uses pygame to show the moves made. Returns a tuple which
    includes the winner as str and moves as a list
    """

    game_board = Checkers()
    moves_so_far = []
    is_continued = False
    previous_move = ('', '', '')
    move_count = 0

    size = (800, 800)
    allow = [pygame.MOUSEBUTTONDOWN]
    screen = initialize_screen(size, allow)
    create_board(game_board, screen)

    while game_board.get_winner(move_count) is None:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.display.quit()
        moves_left(MOVE_LIMIT - move_count - 1, screen)

        # If its the human player's turn, then it doesn't suspend the execution of the code,
        # otherwise it suspends the execution of the code for the game animation
        if not (game_board.is_white_move and isinstance(white, HumanPlayer)) and not (
                not game_board.is_white_move and isinstance(black, HumanPlayer)):
            time.sleep(1)

        # makes the moves
        if game_board.is_white_move:
            move = white.make_move(game_board, previous_move, is_continued)
        else:
            move = black.make_move(game_board, previous_move, is_continued)

        game_board.make_move_pygame(move, screen)

        # does the crowning
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
    time.sleep(0.8)
    pygame.display.quit()
    return (game_board.get_winner(move_count), moves_so_far)


def draw_crown(move: tuple[str, str, str], screen: pygame.Surface,
               color: tuple[int, int, int]) -> None:
    """
    Draws a crowned piece after a move on the given screen and color.
    """
    y, x = pos_to_square(move[2])
    rect2 = pygame.Rect((OFFSET + y * RECT_SIZE, OFFSET + x * RECT_SIZE),
                        (RECT_SIZE, RECT_SIZE))
    pygame.draw.rect(screen, (84, 84, 84), rect2, width=0)
    left = OFFSET + y * RECT_SIZE
    top = OFFSET + x * RECT_SIZE

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
    screen.fill((255, 255, 255))
    pygame.display.flip()

    pygame.event.set_allowed([pygame.QUIT] + allowed)

    return screen


def moves_left(count: int, screen: pygame.Surface) -> None:
    """
    Draws a text on the given screen which indicates how many moves are left.
    """
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
    text_surface = font.render(text, True, (0, 0, 0))
    width, height = text_surface.get_size()
    screen.blit(text_surface,
                pygame.Rect(pos, (pos[0] + width, pos[1] + height)))


def create_board(game: Checkers, screen: pygame.Surface) -> None:
    """
    Draws a checkers board and the pieces on the given screen
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
        if game.black_pieces[piece].is_crowned:
            draw_crown(('', '', piece), screen, (50, 50, 50))
        else:
            draw_piece(screen, piece, 'black')

    for piece in game.white_pieces.keys():
        if game.white_pieces[piece].is_crowned:
            draw_crown(('', '', piece), screen, (255, 255, 255))
        else:
            draw_piece(screen, piece, 'white')

    pygame.display.flip()


def draw_piece(screen: pygame.Surface, pos: str, color: str) -> None:
    """
    Draws a checkers piece in the given board and position with given color

    Representation Invariants:
    - color in {'black', 'white'}
    """

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
    Returns the corresponding square (e.g. (1, 2) -first square from the second last row-)
    from a given position (e.g. a5, f3, e1)
    """
    return ((ord(pos[0]) - 97), int(pos[1]) - 1)


def square_to_pos(pos: tuple[int, int]) -> str:
    """
    Returns the corresponding position (e.g. a5, f3, e1)
    from a given square (e.g. (1, 2) -first square from the second last row-)
    """

    x = ((pos[0] - OFFSET) // RECT_SIZE) + 1
    y = ((pos[1] - OFFSET) // RECT_SIZE) + 1

    if pos[0] >= OFFSET and pos[1] >= OFFSET and x <= 6 and y <= 6:
        return chr(96 + x) + str(y)
    else:
        return ''


def num_to_color(x: int, y: int) -> tuple:
    """
    Used when drawing the Checkers board. It returns the corresponding color to the given square
    """
    if (x + y) % 2 == 0:
        # white
        return (255, 255, 255)
    else:
        # black
        return (84, 84, 84)


def position_to_index(pos: tuple[int, int]) -> Optional[tuple[int, int]]:
    """
    Used when finding out which button in the player columns the user clicked in
    choose_player window.
    """
    rect_height = 70
    rect_width = 150

    if OFFSET + rect_height <= pos[1] <= (
            len(PLAYER_TYPES) + 1) * rect_height + OFFSET and OFFSET <= pos[0] <= OFFSET \
            + rect_width:
        i = (pos[1] - OFFSET - rect_height) // rect_height
        # returns this if the user clicked on the column starting with Player1
        # i represents the row of the chosen rectangle
        return (1, i)
    elif OFFSET + rect_height <= pos[1] <= (
            len(PLAYER_TYPES) + 1) * rect_height + OFFSET and 3 * OFFSET <= pos[0] <= 3 * OFFSET \
            + rect_width:
        i = (pos[1] - OFFSET - rect_height) // rect_height
        # returns this if the user clicked on the column starting with Player2
        # i represents the row of the chosen rectangle
        return (3, i)
    else:
        # if user clicked somewhere outside of the player columns then it returns none
        return None


def find_pieces_between(pos1: str, pos2: str, game: Checkers) -> str:
    """
    Used when HumanPlayer makes a move. It searches if the move that the human player makes
    remove pieces.
    """
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
    A player that is run by a human from the pygame interface

    Instance Attributes:
    -clicked: the square of the piece that is gonna be moved
    -released: the new position of the piece chosen
    """
    clicked: str
    released: str

    def __init__(self) -> None:
        self.clicked = ''
        self.released = ''

    def make_move(self, game: Checkers, previous_move: tuple[str, str, str],
                  continuing_from_previous_move: bool) -> tuple[str, str, str]:
        """
        By tracking the mouse events of the user, it returns the move that the player makes.
        """
        while True:
            event = pygame.event.wait()
            # If the clicked square is valid it stores its position in self.clicked
            if event.type == pygame.MOUSEBUTTONDOWN and ((game.is_white_move and square_to_pos(
                    event.pos) in game.white_pieces.keys()) or (
                        not game.is_white_move
                        and square_to_pos(event.pos) in game.black_pieces.keys())):

                self.clicked = square_to_pos(event.pos)

            if event.type == pygame.MOUSEBUTTONDOWN and self.clicked != '':
                self.released = square_to_pos(event.pos)
                if self.released != '':
                    # checks if there is an opponent's piece between the chosen squares and
                    # according to that creates a move tuple
                    other_piece = find_pieces_between(self.clicked, self.released, game)
                    move = (self.clicked, other_piece, self.released)

                    # If the move is valid it is returned, else everything is reset
                    if move in game.get_valid_moves():
                        return move
                    else:
                        self.clicked: ''
                        self.released: ''


def draw_moves(moves: list, screen: pygame.Surface) -> Checkers:
    """
    Draws the chosen move on the game board. moves list contains the moves played in that game.
    """

    # initializes a game at a starting point
    game_board = Checkers()

    # makes the moves in the given list
    for move in moves:
        if move[0] not in game_board.white_pieces.keys() and game_board.is_white_move:
            game_board.is_white_move = not game_board.is_white_move
        if move[0] not in game_board.black_pieces.keys() and not game_board.is_white_move:
            game_board.is_white_move = not game_board.is_white_move

        game_board.make_move(move)

        if game_board.is_white_move:
            piece = game_board.white_pieces[move[2]]
            if not piece.is_crowned and move[2][1] == '1':
                piece.crown_piece()
        else:
            piece = game_board.black_pieces[move[2]]
            if not piece.is_crowned and move[2][1] == '6':
                piece.crown_piece()

    # Draws the triangles that allow the user to display the next and the previous move
    y = OFFSET + 6 * RECT_SIZE
    x = OFFSET + 3 * RECT_SIZE
    create_board(game_board, screen)
    points = [(x - 40, y + 40), (x - 1, y + 20), (x - 1, y + 60)]
    pygame.draw.polygon(screen, (170, 226, 76), points)
    points2 = [(x + 40, y + 40), (x + 1, y + 20), (x + 1, y + 60)]
    pygame.draw.polygon(screen, (170, 226, 76), points2)

    pygame.display.update()

    return game_board


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ["pygame", "time", "pygame.colordict", "typing"],
        'allowed-io': [],
        'max-nested-blocks': 6,
        'max-line-length': 100,
        'disable': ['E1136'],
        'generated-members': ['pygame.*']

    })
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()
