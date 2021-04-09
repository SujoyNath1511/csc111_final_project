"""
Helper functions
"""
from __future__ import annotations
from typing import Optional
import checkers_game
import checkers_game_tree_v2
import random


class Player:
    """
    An abstract class representing a checkers player.
    This class will be used to create subclasses of different players
    """
    def make_move(self, game: checkers_game.Checkers, previous_move: tuple[str, str, str],
                  continuing_from_previous_move: bool) -> tuple[str, str, str]:
        """
        Make a move based on the given checkers game
        Preconditions:
            - There should at least be one valid moves.
        """
        raise NotImplementedError


class AggressivePlayer(Player):
    """
    A checkers AI player that is greedy and prioritizing the number of pieces its opponent loses
    """
    # Private Instance Attributes:
    #   - _game_tree:
    #       The GameTree that this player uses to make its moves. If None, then this
    #       player just makes random moves.
    _game_tree: Optional[checkers_game_tree_v2.CheckersGameTree]

    def __init__(self, game_tree: Optional[checkers_game_tree_v2.CheckersGameTree]) -> None:
        """
        Assigns the game tree to this player's game tree and if its none, the game tree will be assigned to none
        """
        self._game_tree = game_tree

    def make_move(self, game: checkers_game.Checkers, previous_move: tuple[str, str, str],
                  continuing_from_previous_move: bool) -> tuple[str, str, str]:
        """
        Makes a move based on the game given, previous_move the opponent has made and/or
        if its continuing from previous move
        """
        # Check if the game tree is empty, if it is, pick a random move from get_valid_moves
        if self._game_tree is None:
            lst_of_moves = game.get_valid_moves()
            move = random.choice(lst_of_moves)
            return move
        # Check if there is a previous move, if there is not, then pick a move from the subtrees
        # because it would be the root of the tree
        elif previous_move == checkers_game_tree_v2.START_MOVE:
            move = self._game_tree.subtrees[0]
            for subtree in self._game_tree.subtrees:
                if subtree.lost_black_pcs >= move.lost_black_pcs:
                    move = subtree
            return move.move

        else:
            # find the subtree with the previous move
            subtree = self._game_tree.find_subtree_by_move(previous_move)
            #   if there is such a subtree and its subtrees are not empty
            if subtree is not None and subtree.subtrees != []:
                self._game_tree = subtree
                #   if it is white's turn
                if game.is_white_move:
                    move = self._game_tree.subtrees[0]
                    for subtree in self._game_tree.subtrees:
                        if subtree.lost_black_pcs >= move.lost_black_pcs:
                            move = subtree
                    return move.move
                else:   # if its black's turn
                    move = self._game_tree.subtrees[0]
                    for subtree in self._game_tree.subtrees:
                        if subtree.lost_white_pcs >= move.lost_white_pcs:
                            move = subtree
                    return move.move
            else:   # there is no subtree that has previous_move
                self._game_tree = None
                move = random.choice(game.get_valid_moves())
                return move


class DefensivePlayer(Player):
    """
    An AI player that is defensive. This player tries to preserve as many pieces as possible and make
    its moves based on the number of pieces it will lose
    """
    # Private Instance Attribute
    #   - _game_tree:
    #       The GameTree that this player uses to make its moves. If None, then this
    #       player just makes random moves.
    _game_tree = Optional[checkers_game_tree_v2.CheckersGameTree]

    def __init__(self, game_tree: Optional[checkers_game_tree_v2.CheckersGameTree]):
        """
        Assign the given game tree to the player's game tree
        """
        self._game_tree = game_tree

    def make_move(self, game: checkers_game.Checkers, previous_move: tuple[str, str, str],
                  continuing_from_previous_move: bool) -> tuple[str, str, str]:
        """
        This AI player makes its move defensively.

        The AI picks the subtree where it will lose the lowest number of pieces
        """
        # Check if the game tree is empty, if it is, pick a random move from get_valid_moves
        if self._game_tree is None:
            lst_of_moves = game.get_valid_moves()
            move = random.choice(lst_of_moves)
            return move
        # Check if there is a previous move, if there is not, then pick a move from the subtrees
        # because it would be the root of the tree
        elif previous_move == ():
            move = self._game_tree.subtrees[0]
            for subtree in self._game_tree.subtrees:
                if subtree.lost_white_pcs <= move.lost_white_pcs:
                    move = subtree
            return move.move
        else:
            # find the subtree with the previous move
            subtree = self._game_tree.find_subtree_by_move(previous_move)
            #   if there is such a subtree and its subtrees are not empty
            if subtree is not None and subtree.subtrees != []:
                self._game_tree = subtree
                #   if it is white's turn
                if game.is_white_move:
                    move = self._game_tree.subtrees[0]
                    for subtree in self._game_tree.subtrees:
                        if subtree.lost_white_pcs <= move.lost_white_pcs:
                            move = subtree
                    return move.move
                else:  # if its black's turn
                    smallest_pcs_lost = min(black.lost_black_pcs for black in self._game_tree.subtrees)
                    #   Find the subtree with the given smallest_pcs_lost
                    move = self._game_tree.subtrees[0]
                    for subtree in self._game_tree.subtrees:
                        if subtree.lost_black_pcs <= move.lost_black_pcs:
                            move = subtree
                    return move.move
            else:  # there is no subtree that has previous_move
                self._game_tree = None
                move = random.choice(game.get_valid_moves())
                return move


class RandomPlayer(Player):
    """
    A random player
    """
    def make_move(self, game: checkers_game.Checkers, previous_move: tuple[str, str, str],
                  continuing_from_previous_move: bool) -> tuple[str, str, str]:
        """
        Makes move
        """
        moves = game.get_valid_moves()
        move = random.choice(moves)
        return move


if __name__ == '__main__':
    import doctest
    doctest.testmod()
