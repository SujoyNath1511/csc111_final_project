"""
This is a test file for the checkers game.
"""

from typing import Dict, Optional, Tuple

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
        elif move_count == MOVE_LIMIT:
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

    def capture(self, position: str) -> None:
        """
        removes the piece that is on the given position from the game
        """
        if self.is_white_move:
            self.black_pieces.pop(position)
        else:
            self.white_pieces.pop(position)


class Player:
    """
    An abstract class representing a checkers player.
    This class will be used to create subclasses of different players
    """

    def make_move(self, game: Checkers, previous_move: str, continuing_from_previous_move: bool) -> tuple[str, str, str]:
        """
        Make a move based on the given checkers game
        Preconditions:
            - There should at least be one valid moves.
        """
        raise NotImplementedError
