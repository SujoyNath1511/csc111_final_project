"""
This file contains the code for the game tree that the checkers AI will use to make decisions in
the game.

This file is under copyright by Sujoy Deb Nath, Benjamin Lee, Mohamed Abdullahi and Eren Findik.
"""
from typing import Optional

# May be subject to change later
import checkers_game_with_pygame as checkers

START_MOVE = ('', '', '')


class CheckersGameTree:
    """A tree object that stores the possible moves and move sequences within a simplified
    checkers game.

    Instance Attributes:
        - is_white: Whether white will make the next move
        - prev_move: The move made on the previous turn.
        - lost_white_pcs: The average number of pieces white could lose
        - lost_black_pcs: The average number of pieces black could lose
        - subtrees: The subtrees of this tree.

    Representation Invariants:
        - prev_move is a valid move
        - all(pos in checkers.VALID_POSITIONS for pos in prev_move)
        - 0 <= lost_white_pcs <= 6
        - 0 <= lost_black_pcs <= 6
    """
    is_white: bool
    prev_move: tuple[str, str, str]
    lost_white_pcs: float
    lost_black_pcs: float
    subtrees: list[CheckersGameTree]

    def __init__(self, curr_player: bool,
                 move: Optional[tuple[str, str, str]]) -> None:
        self.is_white = curr_player

        if move is None:
            self.prev_move = ('', '', '')
        else:
            self.prev_move = move

        # At the beginning of the game, you have the potential to lose all the pieces
        # because the game could go either way.
        self.lost_black_pcs = 6
        self.lost_white_pcs = 6
        self.subtrees = []

    def is_empty(self) -> bool:
        """Returns whether this tree is empty or not."""
        if self.prev_move == START_MOVE:
            return True
        return False

    def add_subtree(self, subtree: CheckersGameTree) -> None:
        """Adds a subtree to the current tree."""
        self.subtrees.append(subtree)
        self.update_lost_pcs()

    def update_lost_pcs(self) -> None:
        """Updates the self.lost_black_pcs and self.lost_white_pcs.

        Preconditions:
            - self.is_empty() is False
        """
        if self.is_white is True:
            # White is the current player

            # Get the average for all the subtrees
            lst_of_lost_white = [subtree.lost_white_pcs for subtree in self.subtrees]
            self.lost_white_pcs = sum(lst_of_lost_white)/len(lst_of_lost_white)

            # Get the average for all the subtrees, plus one for each subtree that as a capture.
            lost_black_pcs_so_far = []
            for subtree in self.subtrees:
                lost_pcs = subtree.lost_black_pcs

                if subtree.prev_move[1] != '':
                    lost_black_pcs_so_far.append(lost_pcs + 1)
                else:
                    lost_black_pcs_so_far.append(lost_pcs)

            self.lost_black_pcs = sum(lost_black_pcs_so_far)/len(lost_black_pcs_so_far)
        else:
            # Black is the current player
            lst_of_lost_black = [subtree.lost_black_pcs for subtree in self.subtrees]
            self.lost_black_pcs = sum(lst_of_lost_black) / len(lst_of_lost_black)

            lost_white_pcs_so_far = []
            for subtree in self.subtrees:
                lost_pcs = subtree.lost_white_pcs

                if subtree.prev_move[1] != '':
                    lost_white_pcs_so_far.append(lost_pcs + 1)
                else:
                    lost_white_pcs_so_far.append(lost_pcs)

            self.lost_white_pcs = sum(lost_white_pcs_so_far) / len(lost_white_pcs_so_far)

    def insert_move_sequence(self, move_list: list[tuple[bool, tuple[str, str, str]]],
                             i: int) -> None:
        """Inserts a move sequence into the game tree.

        Preconditions:
            - The list of moves is a reverse of the one that occurs in the game. In other words,
            move_list[0][1] represents the last move in the game.
        """
        if move_list == []:  # There are no moves in the move_list.
            return None
        else:
            player = not move_list[0][0]
            new_tree = CheckersGameTree(curr_player=, move=)
