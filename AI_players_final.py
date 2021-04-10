"""
CSC111 Winter 2021 Final Project: Building A Checkers AI Player
This Python module contains the subclasses for the AI players and the random player.
======================================
This file is provided solely for the use of the CSC111 Teaching team and for the
use of people who made this file, Mohamed Abdullahi, Benjamin Lee, Eren Findik and Sujoy
Deb Nath. Any other forms of distribution of this code is strictly prohibited without express
permission of the aforementioned group.
This file is Copyright (c) 2021 Sujoy Deb Nath, Benjamin Lee, Mohamed Abdullahi and Eren Findik.
"""
from __future__ import annotations
import random
from typing import Optional
import checkers_game_tree_v2 as gametree
import checkers_game_with_pygame_v3 as checkers_game


class AggressivePlayer(checkers_game.Player):
    """
    A checkers AI player that is greedy and prioritizing the number of pieces its opponent loses
    """
    # Private Instance Attributes:
    #   - _game_tree:
    #       The GameTree that this player uses to make its moves. If None, then this
    #       player just makes random moves.
    _game_tree: Optional[gametree.CheckersGameTree]

    def __init__(self, game_tree: Optional[gametree.CheckersGameTree]) -> None:
        """
        Assigns the game tree to this player's game tree and if its none,
        the game tree will be assigned to none
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
            return helper_random_player(game, previous_move, continuing_from_previous_move)

        # Check if there is a previous move, if there is not, then pick a move from the subtrees
        # because it would be the root of the tree
        elif previous_move == gametree.START_MOVE:
            assert game.is_white_move == self._game_tree.is_white
            subtree = self._game_tree.subtrees[0]
            for possible_subtree in self._game_tree.subtrees:
                if possible_subtree.lost_black_pcs >= subtree.lost_black_pcs:
                    subtree = possible_subtree
            self._game_tree = subtree
            return subtree.move

        else:
            # find the subtree with the previous move
            subtree = self._game_tree.find_subtree_by_move(previous_move)
            #   if there is such a subtree and its subtrees are not empty
            if subtree is not None and subtree.subtrees != []:
                self._game_tree = subtree
                assert game.is_white_move == self._game_tree.is_white
                # Find the best subtree for the AI
                subtree = self.helper_find_best_subtree(game.is_white_move)
                self._game_tree = subtree
                return subtree.move
            else:   # there is no subtree that has previous_move
                self._game_tree = None
                return helper_random_player(game, previous_move, continuing_from_previous_move)

    def helper_find_best_subtree(self, is_white_move: bool) -> gametree.CheckersGameTree:
        """
        A helper function that finds the best subtree to pick for the AI player
        """
        subtree = self._game_tree.subtrees[0]
        if is_white_move:
            for possible_subtree in self._game_tree.subtrees:
                if possible_subtree.lost_black_pcs >= subtree.lost_black_pcs:
                    subtree = possible_subtree
        else:  # if its black's turn
            for possible_subtree in self._game_tree.subtrees:
                if possible_subtree.lost_white_pcs >= subtree.lost_white_pcs:
                    subtree = possible_subtree
        return subtree


class DefensivePlayer(checkers_game.Player):
    """
    An AI player that is defensive. This player tries to preserve as many
    pieces as possible and make its moves based on the number of pieces it will lose


    """
    # Private Instance Attribute
    #   - _game_tree:
    #       The GameTree that this player uses to make its moves. If None, then this
    #       player just makes random moves.
    _game_tree: Optional[gametree.CheckersGameTree]

    def __init__(self, game_tree: Optional[gametree.CheckersGameTree]) -> None:
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
            return helper_random_player(game, previous_move, continuing_from_previous_move)

        # Check if there is a previous move, if there is not, then pick a move from the subtrees
        # because it would be the root of the tree
        elif previous_move == gametree.START_MOVE:
            assert game.is_white_move == self._game_tree.is_white
            subtree = self._game_tree.subtrees[0]
            for possible_subtree in self._game_tree.subtrees:
                if possible_subtree.lost_white_pcs <= subtree.lost_white_pcs:
                    subtree = possible_subtree
            return subtree.move
        else:
            # find the subtree with the previous move
            subtree = self._game_tree.find_subtree_by_move(previous_move)
            #   if there is such a subtree and its subtrees are not empty
            if subtree is not None and subtree.subtrees != []:
                self._game_tree = subtree
                assert game.is_white_move == self._game_tree.is_white
                #   Find the best subtree for the AI player
                subtree = self.helper_find_best_subtree(game.is_white_move)
                self._game_tree = subtree
                return subtree.move
            else:  # there is no subtree that has previous_move
                self._game_tree = None
                return helper_random_player(game, previous_move, continuing_from_previous_move)

    def helper_find_best_subtree(self, is_white_move: bool) -> gametree.CheckersGameTree:
        """
        A helper function that finds the best subtree to pick for the AI player
        """
        subtree = self._game_tree.subtrees[0]
        #   if it is white's turn
        if is_white_move:
            for possible_subtree in self._game_tree.subtrees:
                if possible_subtree.lost_white_pcs <= subtree.lost_white_pcs:
                    subtree = possible_subtree
        else:  # if its black's turn
            subtree = self._game_tree.subtrees[0]
            for possible_subtree in self._game_tree.subtrees:
                if possible_subtree.lost_black_pcs <= subtree.lost_black_pcs:
                    subtree = possible_subtree
        return subtree


class RandomPlayer(checkers_game.Player):
    """
    A random player
    """
    def make_move(self, game: checkers_game.Checkers, previous_move: tuple[str, str, str],
                  continuing_from_previous_move: bool) -> tuple[str, str, str]:
        """
        Makes move
        """
        #   Check whether if the player can can capture again
        if continuing_from_previous_move:
            if game.is_white_move:  # If it is the white's turn
                #   Find the piece that captured
                piece = game.white_pieces[previous_move[2]]

            else:  # It is black's turn
                #   Find the piece that captured
                piece = game.black_pieces[previous_move[2]]
            #   Find possible moves that the piece can make
            moves = game.get_valid_move_piece(piece)
            #   Pick a random move from the valid moves
            move = random.choice(moves[0])
        else:  # Not making double captures
            possible_moves = game.get_valid_moves()
            move = random.choice(possible_moves)
        return move


def helper_random_player(game: checkers_game.Checkers,
                         previous_move: tuple[str, str, str],
                         continuing_from_previous_move: bool) -> tuple[str, str, str]:
    """
    Helper function that makes a random move
    """
    if continuing_from_previous_move:
        if game.is_white_move:  # If it is the white's turn
            #   Find the piece that captured
            piece = game.white_pieces[previous_move[2]]

        else:  # It is black's turn
            #   Find the piece that captured
            piece = game.black_pieces[previous_move[2]]
        #   Find possible moves that the piece can make
        moves = game.get_valid_move_piece(piece)
        #   Pick a random move from the valid moves
        move = random.choice(moves[0])
    else:  # Not making double captures
        possible_moves = game.get_valid_moves()
        move = random.choice(possible_moves)
    return move


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ["__future__", "typing", "random",
                          "checkers_game_with_pygame_v3", "checkers_game_tree_v2"],
        'allowed-io': [],
        'max-nested-blocks': 5,
        'max-line-length': 100,
        'disable': ['E1136']
    })
