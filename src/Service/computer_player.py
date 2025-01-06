import random
from src.board.board import ShipDirection, ComputerBoard


class ComputerPlayer:
    def __init__(self, board: ComputerBoard):
        self.__board = board
        self.__board_size = board.get_size

    def place_battleships(self, _computer_battleships, _computer_battleships_length):
        for index in range(1, _computer_battleships + 1):
            placed = False
            while not placed:
                x = random.randint(0, self.__board_size - 1)
                y = random.randint(0, self.__board_size - 1)
                direction = random.choice(list(ShipDirection))
                length = random.choice(_computer_battleships_length)
                try:
                    self.__board.place_battleships(length, x, y, direction, index)
                    placed = True
                    _computer_battleships_length.remove(length)
                except ValueError:
                    continue

    def play(self, player_board):
        x = random.randint(0, self.__board_size - 1)
        y = random.randint(0, self.__board_size - 1)
        try:
            hit, boat = player_board.check_hit(x, y)
            if hit:
                print("Computer hit")
            else:
                print("Computer missed")
        except ValueError:
            self.play(player_board)
        return x, y