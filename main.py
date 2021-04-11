

import checkers_game_with_pygame_v5 as c_game
import checkers_game_tree_v5 as checkers_game_tree
import AI_players_v2 as ai
import pygame_interface




if __name__ == '__main__':

    # list_of_games = checkers_game_tree.read_moves_from_csv('game_tree_data.csv')
    # game_tree = checkers_game_tree.build_game_tree_from_list(list_of_games)



    player1, player2 = pygame_interface.choose_players()
    game = c_game.run_game_pygame(player1, player2)
    print('The winner:' + game[0])
    print(game[1])
    print(player1)
    print(player2)

