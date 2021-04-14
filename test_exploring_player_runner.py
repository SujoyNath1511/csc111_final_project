"""CSC111 Winter 2021 Final Project: Building A Checkers AI Player

This is a unit test file used to test checkers_game_tree_final.exploring_player_runner().

Copyright and Usage Information:
======================================
This file is provided solely for the use of the CSC111 Teaching team and for the
use of people who made this file, Mohamed Abdullahi, Benjamin Lee, Eren Findik and Sujoy
Deb Nath. Any other forms of distribution of this code is strictly prohibited without express
permission of the aforementioned group.
This file is Copyright (c) 2021 Sujoy Deb Nath, Benjamin Lee, Mohamed Abdullahi and Eren Findik.
"""

from checkers_game_tree_final import exploring_player_runner, compare_move_sequence_game_tree


def test_exploring_player_runner() -> None:
    """Tests exploring_player_runner to ensure that it each move sequence is unique. Note that
    this may be true for a limited number of move sequences because once a certain number of
    games have been played, there may be repeats."""
    move_sets = exploring_player_runner(50)[1]
    assert all(move_sets.count(moves) == 1 for moves in move_sets)


def test_exploring_runner_tree() -> None:
    """Asserts that the game tree returned has all the moves from the list of move sequences"""
    test = exploring_player_runner(50)
    game_tree = test[0]
    move_sets = test[1]
    assert all(compare_move_sequence_game_tree(game_tree, move_sequence, 0)
               for move_sequence in move_sets)


if __name__ == '__main__':
    import pytest
    pytest.main(['test_exploring_player_runner.py'])
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ["checkers_game_tree_final"],
        'allowed-io': [],
        'max-nested-blocks': 5,
        'max-line-length': 100,
        'disable': ['E1136']
    })
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()
