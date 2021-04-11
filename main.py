"""CSC111 Winter 2021 Final Project: Building A Checkers AI Player

This is the main file of the project. It is meant to run the pygame interface and print the
statistics for the AI players onto the Python Console.

Copyright and Usage Information:
======================================
This file is provided solely for the use of the CSC111 Teaching team and for the
use of people who made this file, Mohamed Abdullahi, Benjamin Lee, Eren Findik and Sujoy
Deb Nath. Any other forms of distribution of this code is strictly prohibited without express
permission of the aforementioned group.
This file is Copyright (c) 2021 Sujoy Deb Nath, Benjamin Lee, Mohamed Abdullahi and Eren Findik.
"""
import checkers_game_with_pygame_v5 as c_game
import ai_players_final as ai
import pygame_interface


if __name__ == '__main__':

    # Run the pygame interface.
    player1, player2 = pygame_interface.choose_players()
    game = c_game.run_game_pygame(player1, player2)
    print('The winner:' + game[0])

    # Print AI statistics. This part may take a while, so if you want to see
    # the statistics specifically, comment out the previous lines.
    ai.print_ai_statistics()
