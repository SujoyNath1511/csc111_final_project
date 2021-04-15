"""
CSC111 Winter 2021 Final Project: Building A Checkers AI Player

This Python module contains the game tree class that the Aggressive AI and Defensive AI will
use. It also contains the functions that allow for reading and writing to a CSV file (game tree
building purposes) and an Exploring Player AI that also builds the game tree.

Copyright and Usage Information:
======================================
This file is provided solely for the use of the CSC111 Teaching team and for the
use of people who made this file, Mohamed Abdullahi, Benjamin Lee, Eren Findik and Sujoy
Deb Nath. Any other forms of distribution of this code is strictly prohibited without express
permission of the aforementioned group.
This file is Copyright (c) 2021 Sujoy Deb Nath, Benjamin Lee, Mohamed Abdullahi and Eren Findik.
"""
from __future__ import annotations
from typing import Optional
import random
import csv
# May be subject to change later
from checkers_game_with_pygame_final import Player, Checkers, run_game

START_MOVE = ('', '', '')
STARTING_PLAYER = True


class CheckersGameTree:
    """A tree object that stores the possible moves and move sequences within a simplified
    checkers game.
    Instance Attributes:
        - is_white: Whether white will make the next move
        - move: The move made this turn.
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
    move: tuple[str, str, str]
    lost_white_pcs: float
    lost_black_pcs: float
    subtrees: list[CheckersGameTree]

    def __init__(self, curr_player: bool,
                 move: Optional[tuple[str, str, str]]) -> None:

        self.is_white = curr_player

        if move is None:
            self.move = START_MOVE
        else:
            self.move = move

        self.lost_black_pcs = 0
        self.lost_white_pcs = 0
        self.subtrees = []

    def is_empty(self) -> bool:
        """Returns whether this tree is empty or not.

        A tree is considered empty if the root move is empty (all positions are empty.)
        """
        if self.move == START_MOVE:
            return True
        return False

    def add_subtree(self, subtree: CheckersGameTree) -> None:
        """Adds a subtree to the current tree."""
        self.subtrees.append(subtree)
        self.update_lost_pcs()  # Update all the values of the tree.

    def update_lost_pcs(self) -> None:
        """Updates the self.lost_black_pcs and self.lost_white_pcs.

        Preconditions:
            - self.subtrees != []
        """
        if self.is_white is True:
            # White is the current player

            # Get the average for all the subtrees
            lst_of_lost_white = [tree.lost_white_pcs for tree in self.subtrees]
            self.lost_white_pcs = sum(lst_of_lost_white) / len(lst_of_lost_white)

            # Get the average for all the subtrees, plus one for each subtree that as a capture.
            lost_black_pcs_so_far = []
            for subtree in self.subtrees:
                lost_pcs = subtree.lost_black_pcs
                if subtree.move[1] != '':
                    lost_black_pcs_so_far.append(lost_pcs + 1)
                else:
                    lost_black_pcs_so_far.append(lost_pcs)

            self.lost_black_pcs = sum(lost_black_pcs_so_far) / len(lost_black_pcs_so_far)
        else:
            # Black is the current player
            lst_of_lost_black = [tree.lost_black_pcs for tree in self.subtrees]
            self.lost_black_pcs = sum(lst_of_lost_black) / len(lst_of_lost_black)

            lost_white_pcs_so_far = []
            for subtree in self.subtrees:
                lost_pcs = subtree.lost_white_pcs

                if subtree.move[1] != '':
                    lost_white_pcs_so_far.append(lost_pcs + 1)
                else:
                    lost_white_pcs_so_far.append(lost_pcs)

            self.lost_white_pcs = sum(lost_white_pcs_so_far) / len(lost_white_pcs_so_far)

    def insert_move_sequence(self, move_list: list[tuple[bool, tuple[str, str, str]]],
                             i: int) -> None:
        """Inserts a move sequence into the game tree. Each consecutive element is a
        child of the previous element. The variable i refers to the index position of
        the current move being inserted (the root move of the tree).

        Preconditions:
            - 0 <= i <= len(move_list)
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
                new_tree = CheckersGameTree(move_list[i + 1][0],  # Next player
                                            move_list[i][1])  # previous player's move

            assert move_list[i][0] == self.is_white  # Make sure we have the same player.

            # Add the rest of the move_list as subtrees to the new subtree we just made
            new_tree.insert_move_sequence(move_list, i + 1)

            # Add the new tree as a subtree.
            self.add_subtree(new_tree)

        else:
            # Subtree is in the game tree. We need to continue recursing through the game
            # tree without making any changes.
            subtree.insert_move_sequence(move_list, i + 1)

        return None

    def find_subtree_by_move(self, move: tuple[str, str, str]) -> Optional[CheckersGameTree]:
        """Finds the subtree corresponding to the input move.
        Return None if there is no such subtree.
        """
        for subtree in self.subtrees:
            if subtree.move == move:
                return subtree

        return None

    def __str__(self) -> str:
        """Return a string representation of this tree.
        
        This code is borrowed from A2.
        """
        return self._str_indented(0)

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this tree.
        The indentation level is specified by the <depth> parameter.
        
        This code is borrowed and modified from A2.
        """
        if self.is_white:
            turn_desc = "White's move"
        else:
            turn_desc = "Black's move"

        move_desc = f'{self.move}, B: {self.lost_black_pcs}, W: {self.lost_white_pcs} ' \
                    f'-> {turn_desc}\n'
        s = '  ' * depth + move_desc
        if self.subtrees == []:
            return s
        else:
            for subtree in self.subtrees:
                s += subtree._str_indented(depth + 1)
            return s


class ExploringPlayer(Player):
    """
    A player that makes moves that have not been made before using a GameTree.
    Instance Attribute:
        - _game_tree: The game tree that ExploringPlayer uses to make moves
    """
    game_tree: Optional[CheckersGameTree] = None

    def __init__(self, game_tree: CheckersGameTree) -> None:
        self.game_tree = game_tree

    def make_move(self, game: Checkers, previous_move: tuple[str, str, str],
                  continuing_from_previous_move: bool) -> tuple[str, str, str]:
        """Makes a move that is not in the game_tree. If all valid moves are in the game tree,
        it makes a random move."""
        # If previous_move is None, then no move has been made in the game
        if self.game_tree is not None and previous_move != ('', '', ''):
            self.game_tree = self.game_tree.find_subtree_by_move(previous_move)
        # If it is continuing from a previous move for white, get the valid moves for the piece
        if continuing_from_previous_move and game.is_white_move:
            valid_moves = game.get_valid_move_piece(game.white_pieces[previous_move[2]])[0]
        elif continuing_from_previous_move:
            valid_moves = game.get_valid_move_piece(game.black_pieces[previous_move[2]])[0]
        else:
            valid_moves = game.get_valid_moves()
        # No moves are in the game tree, so any move can be picked
        if self.game_tree is None:
            return random.choice(valid_moves)
        else:
            # Find the moves not in the game tree
            moves_not_in_game_tree = []
            for move in valid_moves:
                for subtree in self.game_tree.subtrees:
                    if subtree.move == move:
                        move = None
                        break
                if move is not None:
                    moves_not_in_game_tree.append(move)
            if moves_not_in_game_tree == []:
                return random.choice(valid_moves)
            else:
                return random.choice(moves_not_in_game_tree)


def exploring_player_runner(n: int) -> tuple[CheckersGameTree,
                                             list[list[tuple[bool, tuple[str, str, str]]]]]:
    """Runs run_games n times to build up the game tree using ExploringPlayers and a blank
    game tree.
    Returns two items, the built up game tree and a list of lists. Each sublist within the
    list represents all the moves played in one game and who made each move. The format of the
    sublist is the same format as the list returned in run_game() from
    checkers_game_with_pygame_final.py.
    """
    all_move_sequences = []
    game_tree = CheckersGameTree(True, None)
    white_player = ExploringPlayer(game_tree)
    black_player = ExploringPlayer(game_tree)
    for _ in range(0, n):
        move_sequence = run_game(white_player, black_player)[1]
        game_tree.insert_move_sequence(move_sequence, 0)
        all_move_sequences.append(move_sequence)
        white_player.game_tree = game_tree
        black_player.game_tree = game_tree
    return (game_tree, all_move_sequences)


def write_moves_to_csv(filename: str,
                       list_of_games: list[list[tuple[bool, tuple[str, str, str]]]]) -> None:
    """This function takes in a csv file and list of lists, where each sublist represents
    the moves made in a single game, and writes this list of lists into the csv file.

    Preconditions:
        - filename is a valid file path to a file that exists
        - list_of_games != []
        - all(moves != [] for moves in list_of_games)
        - The move sequences in list_of_games are all the moves in a single game, from start to
        finish.
        - Every move in move in the sublists of list_of_games are valid moves.
    """
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        for move_seq in list_of_games:
            move_list = [str((int(move[0]), move_to_str(move[1])))
                         for move in move_seq]
            writer.writerow(move_list)


def read_moves_from_csv(filename: str) -> list[list[tuple[bool, tuple[str, str, str]]]]:
    """Returns a list of lists, where each sublist represents the moves made
    in a single game, read from a csv file with the path filename.

    Preconditions:
        - filename is a valid file path
    """

    list_of_games = []

    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            # Here is what row may look like:
            # ["(1, 'a4  b3')","(0, 'a2b3c4')", ...]
            # Thus each element is the string: "(1, 'a4  b3')"
            # Need to convert from "(1, 'a4  b3')" to (True, ('a4', '', 'b3'))
            move_sequence = [(bool(int(move[1])), str_to_move(move[5: 11])) for move in row]
            list_of_games.append(move_sequence)

    return list_of_games


def move_to_str(move: tuple[str, str, str]) -> str:
    """Takes in a move and converts it to a string.

    >>> move_to_str(('a4', '', 'b3'))
    'a4  b3'

    >>> move_to_str(('a4', 'b5', 'c6'))
    'a4b5c6'
    """
    if move[1] == '':
        capture = '  '
    else:
        capture = move[1]

    return move[0] + capture + move[2]


def str_to_move(str_move: str) -> tuple[str, str, str]:
    """Takes in a string and converts into a move. The move format
    is based on how move was defined in the Checkers class and
    CheckersGameTree class.

    Precondtions:
        - str_move is properly formatted.
        - len(str_move) == 6

    >>> str_to_move('a4  b3')
    ('a4', '', 'b3')

    >>> str_to_move('a4b5c6')
    ('a4', 'b5', 'c6')
    """
    if str_move[2: 4] == '  ':
        capture = ''
    else:
        capture = str_move[2: 4]

    return (str_move[0: 2], capture, str_move[4:])


def build_game_tree_from_list(list_of_games: list[list[tuple[bool, tuple[str, str, str]]]]) -> \
        CheckersGameTree:
    """Returns a built up game tree using the move sequences in list_of_games. list_of_games
    is a list of lists, where each sublist is the move sequence from a single game.

    Preconditions:
        - list_of_games != []
        - all(moves != [] for moves in list_of_games)
        - The move sequences in list_of_games are all the moves in a single game, from start to
        finish.
        - Every move in move in the sublists of list_of_games are valid moves.
    """
    game_tree = CheckersGameTree(STARTING_PLAYER, None)

    for move_seq in list_of_games:
        game_tree.insert_move_sequence(move_seq, 0)

    return game_tree


def compare_move_sequence_game_tree(game_tree: CheckersGameTree,
                                    move_sequence: list[tuple[bool, tuple[str, str, str]]],
                                    i: int) -> bool:
    """Makes a list of move sequences based on the game tree. Move sequences are a lists of valid
     moves played in a game. Used to test whether moves are valid.

     Preconditions:
        - 0 <= i < len(move_sequence)
        - move_sequence != []
     """

    if i == len(move_sequence) - 1:
        # Since move_sequence from exploring_player_runner also returns a bool in the list, we need
        # to exclude that
        return game_tree.move == move_sequence[i][1]
    elif game_tree.move == ('', '', ''):
        for subtree in game_tree.subtrees:
            if compare_move_sequence_game_tree(subtree, move_sequence, i):
                return True
        return False
    elif game_tree.move != move_sequence[i][1]:
        return False
    else:
        for subtree in game_tree.subtrees:
            if compare_move_sequence_game_tree(subtree, move_sequence, i + 1):
                return True
        return False


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ["__future__", "typing", "random",
                          "csv", "checkers_game_with_pygame_final"],
        'allowed-io': ['read_moves_from_csv', 'write_moves_to_csv'],
        'max-nested-blocks': 5,
        'max-line-length': 100,
        'disable': ['E1136']
    })
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()
