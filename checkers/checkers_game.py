"""
This is a test file for the checkers game.
"""

from typing import Set, Optional, Tuple

START_POS_BLACK = {'a2', 'b1', 'c2', 'd1', 'e2', 'f1'}
START_POS_WHITE = {'a6', 'b5', 'c6', 'd5', 'e6', 'f5'}
VALID_POSITIONS = [letter + str(2 * x) for x in range(1, 4) for letter in 'ace'] + \
                  [letter + str(2 * x + 1) for x in range(0, 3) for letter in 'bdf']
PLAYER_COLORS = ('white', 'black')


class Piece:
    """This class will be used to represent each counter/piece on the checkers board.
    It will keep track of where the piece is and what possible moves it can make, as well as
    the piece's color.

    Instance attributes:
        - white: Whether the color of this piece is white
        - position: The position of self on the board

    Representation Invariants:
        - self.position in VALID_POSITIONS
    """
    # Private Instance Attributes:
    #   - crown: Whether this piece is a crown piece
    _crown: bool
    white: bool
    position: str

    def __init__(self, is_white: bool, start_pos: str) -> None:
        self._crown = False
        self.white = is_white
        self.position = start_pos

    def crown_piece(self) -> None:
        """This method changes the crown attribute so that self is now crowned.
        self can now move in all diagonal adjacent squares.
        """
        self._crown = True

    def is_crown(self) -> bool:
        """Returns whether self is a crown piece or not."""
        return self._crown


class Checkers:
    """A class that represents the game checkers.

    Instance Attributes:
        - white_pieces: A list of all the white pieces.
        - black_pieces: A list of all the black pieces
        - current_player: Which color is currently making a move.
    """
    white_pieces: list[Piece]
    black_pieces: list[Piece]
    current_player: str

    def __init__(self, white: Optional[list[Piece]] = None,
                 black: Optional[list[Piece]] = None,
                 curr_player: Optional[str] = None) -> None:

        # Mainly for being able to copy the board
        if white is not None and black is not None and curr_player is not None:
            self.white_pieces = white
            self.black_pieces = black
            self.current_player = curr_player

        else:   # For starting a new game.
            self.white_pieces = [Piece(is_white=True, start_pos=pos) for pos in START_POS_WHITE]
            self.black_pieces = [Piece(is_white=False, start_pos=pos) for pos in START_POS_BLACK]
            current_player = PLAYER_COLORS[0]

    def get_valid_moves(self) -> list[list[Tuple[str, str, str]]]:
        """Returns all the valid moves for a specific player. The returned item is
        a list of lists of tuples of strings. Here is the breakdown of the returned list
        from smallest to largest:

        1. Each string corresponds to a position on the board.

        2. A tuple of these strings is considered a move (a change in position).
            - first item: The initial position of the piece.
            - second item: Can be blank or a position coordinate if it goes over a piece.
            - third item: The final position.

        3. A list of tuples is a sequence of consecutive moves. In checkers, players are
        able to capture multiple pieces consecutively in one move.

        4. A list of list of tuples are all possible move sequences for a player. The smallest
        length should be 1 and the largest should be 4 times the number of pieces the player has.

            Note*: The 4 times above comes from the fact that a crowned piece can move in any
            diagonal direction like a queen in chess. As long as all diagonal positions
            are unoccupied or an opponent piece is diagonally adjacent to the crown.
        """
        white_pos = [p.position for p in self.white_pieces]
        black_pos = [p.position for p in self.black_pieces]

        # Get the color of the player
        if self.current_player == 'white':
            # Player is playing white

            # ACCUMULATOR valid_moves_so_far tracks the number of valid move sequences
            # found so far.
            valid_moves_so_far = []

            # Check positions and valid moves for each piece.
            for piece in self.white_pieces:

                # Start a new move_sequence
                move_seq = []

                # Get the piece's position.
                original_position = piece.position

        else:
            # Player is playing black
            ...

    def winner(self):
        ...
