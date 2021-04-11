"""The main file."""
import checkers_game_with_pygame_v5 as c_game
import checkers_game_tree_final as checkers_game_tree
import AI_players_final as Ai
import pygame_interface


if __name__ == '__main__':

    # list_of_games = checkers_game_tree.read_moves_from_csv('game_tree_data.csv')
    # game_tree = checkers_game_tree.build_game_tree_from_list(list_of_games)

    # player1, player2 = pygame_interface.choose_players()
    # game = c_game.run_game_pygame(player1, player2)
    # print('The winner:' + game[0])
    # print(game[1])
    # print(player1)
    # print(player2)

    list_of_games = checkers_game_tree.read_moves_from_csv('game_tree_data.csv')
    game_tree = checkers_game_tree.build_game_tree_from_list(list_of_games)

    # Statistics for Aggressive AI:
    win_rates_aggro = []
    for i in range(0, 10):
        stats = {'white': 0, 'black': 0, 'draw': 0}
        for j in range(0, 1000):
            white = Ai.AggressivePlayer(game_tree)
            black = Ai.RandomPlayer()
            stats[c_game.run_game(white, black)[0]] += 1
        win_rates_aggro.append(stats['white'] > stats['black'])

    print(win_rates_aggro)

    # Statistics for Defensive AI:
    win_rates_defen = []
    for i in range(0, 10):
        stats = {'white': 0, 'black': 0, 'draw': 0}
        for j in range(0, 1000):
            white = Ai.AggressivePlayer(game_tree)
            black = Ai.RandomPlayer()
            stats[c_game.run_game(white, black)[0]] += 1
        win_rates_defen.append(stats['white'] > stats['black'])

    print(win_rates_defen)
