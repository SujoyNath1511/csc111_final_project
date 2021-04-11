"""The main file."""
import checkers_game_with_pygame_v5 as c_game
import ai_players_final as ai
import pygame_interface


if __name__ == '__main__':

    player1, player2 = pygame_interface.choose_players()
    game = c_game.run_game_pygame(player1, player2)
    print('The winner:' + game[0])

    ai.print_ai_statistics()
