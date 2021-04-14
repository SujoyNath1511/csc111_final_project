from checkers_game_tree_final import exploring_player_runner, compare_move_sequence_to_game_tree


def test_exploring_player_runner() -> None:
    """Tests exploring_player_runner to ensure that it each move sequence is unique. Note that
    this may be true for a limited number of move sequences because once a certain number of
    games have been played, there may be repeats."""
    move_sets = exploring_player_runner(50)[1]
    assert all(move_sets.count(moves) == 1 for moves in move_sets)


def test_exploring_player_runner_game_tree() -> None:
    """Asserts that the game tree returned has all the moves from the list of move sequences"""
    test = exploring_player_runner(50)
    game_tree = test[0]
    move_sets = test[1]
    assert all(compare_move_sequence_to_game_tree(game_tree, move_sequence, 0)
               for move_sequence in move_sets)


if __name__ == '__main__':
    import pytest
    pytest.main(['test_exploring_player_runner.py'])
