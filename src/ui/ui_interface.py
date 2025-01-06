from abc import abstractmethod, ABC


class UiInterface(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_placement(self, battleships):
        pass

    @abstractmethod
    def print_boards(self, _player_board, _computer_board):
        pass

    @abstractmethod
    def print_game_over(self, winner, player_hits, player_misses, computer_hits, computer_misses):
        pass

    @abstractmethod
    def get_play_coordinates(self):
        pass

    @abstractmethod
    def print_board(self, board):
        pass
