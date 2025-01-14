import os
import sys
from abc import ABC

from src.ui.ui_interface import UiInterface


class ConsoleUI(UiInterface, ABC):
    def __init__(self):
        super().__init__()

    def run(self, game):
        print("Welcome to Battleships!")
        print("You have to place your battleships on the board")
        print("After that, you will be prompted to enter the coordinates for your hits")

    def get_placement(self, battleships):
        print("Lets place the battleships")
        print(f"You have to place the battleships with the lengths: {battleships}")
        x, y, direction, length = input("Enter the x coordinate, y coordinate, direction (HORIZONTAL/VERTICAL or h/v), and length of the ship separated by spaces: ").split()
        x = int(x) - 1
        y = int(y) - 1
        length = int(length)
        return x, y, direction, length

    def print_board(self, board):
        print(board)

    def print_boards(self, _player_board, _computer_board):
        #os.system('cls')
        print("Player board:")
        print(_player_board)
        print("Computer board:")
        print(_computer_board)

    def print_game_over(self, winner, player_hits, player_misses, computer_hits, computer_misses):
        print(f"The winner is {winner}")
        print(f"Player hits: {player_hits}")
        print(f"Player misses: {player_misses}")
        print(f"Computer hits: {computer_hits}")
        print(f"Computer misses: {computer_misses}")

    def get_play_coordinates(self):
        print("Enter the coordinates for the hit")
        x = int(input("Enter the x coordinate: ")) - 1
        y = int(input("Enter the y coordinate: ")) - 1
        return x, y

    def print_result(self, result, player):
        print(f"{player} has {'hit' if result else 'missed'}")

    def print_sunk(self, player):
        print(f"{player} has sunk a ship")

    def print_exception(self, e):
        print(e)
