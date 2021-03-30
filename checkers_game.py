"""
This is a test file for the checkers game.
"""

from typing import Dict, Optional, Tuple, List

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
        position"""
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
                if check not in self.white_pieces and check not in self.black_pieces and\
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

    def make_move(self, game: Checkers, previous_move: str, continuing_from_previous_move: bool) -> tuple[str, str, str]:
        """
        Make a move based on the given checkers game
        Preconditions:
            - There should at least be one valid moves.
        """
        raise NotImplementedError
