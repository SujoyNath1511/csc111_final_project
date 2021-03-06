"""
This file contains the code for the game tree that the checkers AI will use to make decisions in
the game.

This file is under copyright by Sujoy Deb Nath, Benjamin Lee, Mohamed Abdullahi and Eren Findik.
"""
from __future__ import annotations
from typing import Optional

# May be subject to change later
import checkers_game_with_pygame_v2 as checkers

START_MOVE = ('', '', '')
STARTING_PLAYER = True


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
            self.prev_move = START_MOVE
        else:
            self.prev_move = move

        self.lost_black_pcs = 0
        self.lost_white_pcs = 0
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
            - 0 <= i < len(move_list)
            - The last element in move_list represents the last move made in the game.
            - All moves in move_list are valid moves.
        """

        if i >= len(move_list):
            return None

        # 1. Find the subtree corresponding to the current move.
        subtree = self.find_subtree_by_move(move_list[i][1])

        # 2. Check if that subtree exists (i.e in the game tree)
        if subtree is None:
            # Subtree is not in the game tree

            if i == len(move_list) - 1:
                # Expecting this to be the last item in move_list.
                new_tree = CheckersGameTree(not move_list[i][0],  # Next player
                                            move_list[i][1])  # previous player's move
            else:
                new_tree = CheckersGameTree(move_list[i + 1][0],    # Next player
                                            move_list[i][1])        # previous player's move

            assert move_list[i][0] == self.is_white     # Make sure we have the same player.

            # Add the rest of the move_list as subtrees to the new subtree we just made
            new_tree.insert_move_sequence(move_list, i + 1)

            # Add the new tree as a subtree.
            self.add_subtree(new_tree)

        else:
            # Subtree is in the game tree. We need to continue recursing through the game
            # tree without making any changes.
            subtree.insert_move_sequence(move_list, i + 1)

    def find_subtree_by_move(self, move: tuple[str, str, str]) -> Optional[CheckersGameTree]:
        """Finds the subtree corresponding to the input move.

        Return None if there is no such subtree.
        """

        for subtree in self.subtrees:
            if subtree.prev_move == move:
                return subtree

        return None

    def __str__(self) -> str:
        """Return a string representation of this tree.
        """
        return self._str_indented(0)

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_white:
            turn_desc = "White's move"
        else:
            turn_desc = "Black's move"

        move_desc = f'{self.prev_move}, B: {self.lost_black_pcs}, W: {self.lost_white_pcs} ' \
                    f'-> {turn_desc}\n'
        s = '  ' * depth + move_desc
        if self.subtrees == []:
            return s
        else:
            for subtree in self.subtrees:
                s += subtree._str_indented(depth + 1)
            return s


if __name__ == '__main__':
    # Draw
    moves = [(True, ('d5', '', 'c4')), (False, ('c2', '', 'd3')), (True, ('e6', '', 'd5')),
             (False, ('e2', '', 'f3')), (True, ('c4', 'd3', 'e2')), (False, ('f1', 'e2', 'd3')),
             (True, ('f5', '', 'e4')), (False, ('d3', 'e4', 'f5')), (True, ('d5', '', 'e4')),
             (False, ('f3', 'e4', 'd5')), (True, ('c6', 'd5', 'e4')), (False, ('a2', '', 'b3')),
             (True, ('b5', '', 'a4')), (False, ('d1', '', 'e2')), (True, ('a4', 'b3', 'c2')),
             (False, ('b1', 'c2', 'd3')), (True, ('e4', 'd3', 'c2')), (False, ('f5', '', 'e6')),
             (True, ('c2', '', 'd1')), (False, ('e2', '', 'd3')), (True, ('d1', '', 'e2')),
             (False, ('d3', '', 'e4')), (True, ('e2', '', 'd3')), (False, ('e6', '', 'f5')),
             (True, ('a6', '', 'b5')), (False, ('f5', '', 'e6')), (True, ('d3', 'e4', 'f5')),
             (False, ('e6', '', 'd5')), (True, ('b5', '', 'c4')), (False, ('d5', 'c4', 'b3')),
             (True, ('f5', '', 'e6')), (False, ('b3', '', 'c2')), (True, ('e6', '', 'f5')),
             (False, ('c2', '', 'b1')), (True, ('f5', '', 'e4'))]

    # White Wins
    moves_2 = [(True, ('f5', '', 'e4')), (False, ('e2', '', 'd3')), (True, ('b5', '', 'c4')),
               (False, ('d3', 'c4', 'b5')), (True, ('c6', 'b5', 'a4')), (False, ('c2', '', 'd3')),
               (True, ('e4', 'd3', 'c2')), (False, ('b1', 'c2', 'd3')), (True, ('a6', '', 'b5')),
               (False, ('d3', '', 'c4')), (True, ('b5', 'c4', 'd3')), (False, ('f1', '', 'e2')),
               (True, ('d3', 'e2', 'f1')), (False, ('d1', '', 'c2')), (True, ('e6', '', 'f5')),
               (False, ('c2', '', 'd3')), (True, ('d5', '', 'c4')), (False, ('d3', 'c4', 'b5')),
               (True, ('f5', '', 'e4')), (False, ('a2', '', 'b3')), (True, ('a4', 'b3', 'c2')),
               (False, ('b5', '', 'c6')), (True, ('e4', '', 'f3')), (False, ('c6', '', 'b5')),
               (True, ('f3', '', 'e2')), (False, ('b5', '', 'c4')), (True, ('e2', '', 'd1')),
               (False, ('c4', '', 'd5')), (True, ('d1', '', 'e2')), (False, ('d5', '', 'c4')),
               (True, ('e2', '', 'd3')), (False, ('c4', 'd3', 'e2')), (True, ('f1', 'e2', 'd3'))]

    # Black Wins
    moves_3 = [(True, ('d5', '', 'c4')), (False, ('c2', '', 'd3')), (True, ('c4', '', 'b3')),
               (False, ('a2', 'b3', 'c4')), (True, ('b5', '', 'a4')), (False, ('c4', '', 'b5')),
               (True, ('a6', 'b5', 'c4')), (False, ('d3', 'c4', 'b5')), (True, ('a4', '', 'b3')),
               (False, ('e2', '', 'd3')), (True, ('c6', 'b5', 'a4')), (False, ('f1', '', 'e2')),
               (True, ('e6', '', 'd5')), (False, ('d3', '', 'c4')), (True, ('d5', '', 'e4')),
               (False, ('e2', '', 'd3')), (True, ('e4', 'd3', 'c2')), (False, ('b1', 'c2', 'd3')),
               (True, ('f5', '', 'e4')), (False, ('d3', 'e4', 'f5')), (True, ('b3', '', 'c2')),
               (False, ('d1', 'c2', 'b3')), (True, ('a4', 'b3', 'c2')), (False, ('c4', '', 'd5')),
               (True, ('c2', '', 'b1')), (False, ('d5', '', 'e6')), (True, ('b1', '', 'a2')),
               (False, ('e6', '', 'd5')), (True, ('a2', '', 'b3')), (False, ('f5', '', 'e6')),
               (True, ('b3', '', 'a4')), (False, ('d5', '', 'c4')), (True, ('a4', '', 'b3')),
               (False, ('c4', 'b3', 'a2'))]

    test_tree = CheckersGameTree(STARTING_PLAYER, START_MOVE)
    test_tree.insert_move_sequence(moves, 0)
    test_tree.insert_move_sequence(moves_2, 0)
    test_tree.insert_move_sequence(moves_3, 0)
    print(test_tree)
