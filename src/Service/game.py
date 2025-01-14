import random

import pygame

from src.Service.computer_player import ComputerPlayer
from src.board.board import PlayerBoard, ComputerBoard
from src.ui.ui_interface import UiInterface


def get_board_size() -> int:
    """
    Get the board size from the settings file.

    :return: int - The board size.
    """
    with open('settings.properties', 'r') as f:
        for line in f:
            if 'board_size' in line:
                return int(line.split('=')[1].strip())
        raise ValueError('Invalid board size setting')

def get_battleships() -> int:
    """
    Get the number of battleships from the settings file.

    :return: int - The number of battleships.
    """
    with open('settings.properties', 'r') as f:
        for line in f:
            if 'battleships' in line:
                return int(line.split('=')[1].strip())
        raise ValueError('Invalid battleships setting')

def get_battle_ship_length() -> list[int]:
    """
    Get the lengths of the battleships from the settings file.

    :return: list[int] - The lengths of the battleships.
    """
    with open('settings.properties', 'r') as f:
        for line in f:
            if 'battle_ship_length' in line:
                return list(map(int, line.split('=')[1].strip().split(',')))
        raise ValueError('Invalid battle ship length setting')


class Game:
    def __init__(self, ui: UiInterface):
        """
        Initialize the Game class.

        :param ui: UiInterface - The UI interface.
        """
        self.ui = ui
        self.player_board = PlayerBoard(get_board_size())
        self.computer_board = ComputerBoard(get_board_size())
        self.__battleships = get_battleships()
        self.__battleships_length = get_battle_ship_length()
        self.__player_turn = True
        self.__game_over = False
        self.__winner = None
        self.__player_hits = 0
        self.computer_hits = 0
        self.__player_misses = 0
        self.computer_misses = 0
        self.__player_battleships = self.__battleships
        self.__ship_length = self.__get_battleship_length()
        self.__player_battleships_length = self.__ship_length.copy()
        self.__computer_battleships = self.__battleships
        self.__computer_battleships_length = self.__ship_length.copy()
        self.__computer = ComputerPlayer(self.computer_board)
        self.__pygame = None

    def __get_battleship_length(self) -> list[int]:
        """
        Get the lengths of the battleships.

        :return: list[int] - The lengths of the battleships.
        """
        result = []

        for length in self.__battleships_length:
            if length >= get_board_size():
                self.__battleships_length.remove(length)

        if len(self.__battleships_length) < self.__battleships:
            result = self.__generate_more_battleships()
        if len(self.__battleships_length) > self.__battleships:
            result = self.__select_battleships()
        if len(self.__battleships_length) == self.__battleships:
            return self.__battleships_length

        return result

    def __generate_more_battleships(self) -> list[int]:
        """
        Generate more battleships if needed.

        :return: list[int] - The lengths of the battleships.
        """
        result = self.__battleships_length.copy()
        remainder = self.__battleships - len(result)

        for _ in range(remainder):
            result.append(random.choice(self.__battleships_length))

        return result

    def __select_battleships(self) -> list[int]:
        """
        Select battleships if there are too many.

        :return: list[int] - The lengths of the battleships.
        """
        result = []
        for _ in range(self.__battleships):
            result.append(random.choice(self.__battleships_length))
        return result

    def start(self):
        """
        Start the game.
        """
        self.__pygame = self.ui.run(self)
        self.place_player_battleships()
        self.place_computer_battleships()
        self.__game_loop()

    def place_player_battleships(self):
        """
        Place the player's battleships on the board.
        """
        for index in range(1, self.__player_battleships + 1):
            self.ui.print_board(self.player_board)
            try:
                self.place_player_ship(index)
            except ValueError as e:
                self.ui.print_exception(e)

        self.ui.print_board(self.player_board)

    def place_player_ship(self, index: int):
        """
        Place a single player's battleship on the board.

        :param index: int - The index of the battleship.
        """
        try:
            x, y, direction, length = self.ui.get_placement(self.__player_battleships_length)
            if length not in self.__player_battleships_length:
                raise ValueError("Invalid ship length")
            self.player_board.place_battleships(length, x, y, direction, index)
            self.__player_battleships_length.remove(length)
        except ValueError as e:
            self.ui.print_exception(e)
            self.place_player_ship(index)

    def place_computer_battleships(self):
        """
        Place the computer's battleships on the board.
        """
        self.__computer.place_battleships(self.__computer_battleships, self.__computer_battleships_length)

    def __game_loop(self):
        """
        Run the main game loop.
        """
        while not self.__game_over:
            if self.__player_turn:
                self.player_play()
            else:
                self.__computer_play()
            self.ui.print_boards(self.player_board, self.computer_board)
            self.__player_turn = not self.__player_turn
            self.__game_over = self.player_board.check_game_over() or self.computer_board.check_game_over()
        self.__winner = "Player" if self.computer_board.check_game_over() else "Computer"
        self.ui.print_game_over(self.__winner, self.__player_hits, self.__player_misses, self.computer_hits, self.computer_misses)
        self.ui.print_boards(self.player_board, self.computer_board)
        if self.__pygame:
            pygame.quit()

    def player_play(self):
        """
        Handle the player's turn.
        """
        try:
            x, y = self.ui.get_play_coordinates()
            hit, boat = self.computer_board.check_hit(x, y)
            self.ui.print_result(hit, "Player")
            if hit:
                self.__player_hits += 1
                if self.computer_board.check_ship_sunk(boat):
                    self.ui.print_sunk("Player")
            else:
                self.__player_misses += 1
        except ValueError as e:
            self.ui.print_exception(e)
            self.ui.print_boards(self.player_board, self.computer_board)
            self.player_play()

    def __computer_play(self):
        """
        Handle the computer's turn.
        """
        self.__computer.play(self.player_board, self)