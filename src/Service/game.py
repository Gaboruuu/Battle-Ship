from src.Service.computer_player import ComputerPlayer
from src.board.board import PlayerBoard, ComputerBoard
from src.ui.ui_interface import UiInterface


def get_board_size():
    with open('settings.properties', 'r') as f:
        for line in f:
            if 'board_size' in line:
                return int(line.split('=')[1].strip())
        raise ValueError('Invalid board size setting')

def get_battleships():
    with open('settings.properties', 'r') as f:
        for line in f:
            if 'battleships' in line:
                return int(line.split('=')[1].strip())
        raise ValueError('Invalid battleships setting')

def get_battle_ship_length() -> list:
    with open('settings.properties', 'r') as f:
        for line in f:
            if 'battle_ship_length' in line:
                return list(map(int, line.split('=')[1].strip().split(',')))
        raise ValueError('Invalid battle ship length setting')


class Game:
    def __init__(self, ui: UiInterface):
        self._ui = ui
        self._player_board = PlayerBoard(get_board_size())
        self._computer_board = ComputerBoard(get_board_size())
        #self._battleships = get_battleships()
        #self._battle_ship_length = get_battle_ship_length()
        self._player_turn = True
        self._game_over = False
        self._winner = None
        self._player_hits = 0
        self._computer_hits = 0
        self._player_misses = 0
        self._computer_misses = 0
        self._player_battleships = get_battleships()
        self._player_battleships_length = get_battle_ship_length()
        self._computer_battleships = get_battleships()
        self._computer_battleships_length = get_battle_ship_length()
        self._computer = ComputerPlayer(self._computer_board)

    def start(self):
        self._place_player_battleships()
        self._place_computer_battleships()
        self._game_loop()

    def _place_player_battleships(self):
        for index in range(1, self._player_battleships + 1):
            self._ui.print_board(self._player_board)
            x, y, direction, length = self._ui.get_placement(self._player_battleships_length)
            self._player_board.place_battleships(length, x, y, direction, index)
            self._player_battleships_length.remove(length)

        self._ui.print_board(self._player_board)

    def _place_computer_battleships(self):
        self._computer.place_battleships(self._computer_battleships, self._computer_battleships_length)

    def _game_loop(self):
        while not self._game_over:
            if self._player_turn:
                self._player_play()
                self._ui.print_boards(self._player_board, self._computer_board)
            else:
                self._computer_play()
            self._player_turn = not self._player_turn
            self._game_over = self._player_board.check_game_over() or self._computer_board.check_game_over()
        self._winner = "Player" if self._computer_board.check_game_over() else "Computer"
        self._ui.print_game_over(self._winner, self._player_hits, self._player_misses, self._computer_hits, self._computer_misses)
        self._ui.print_boards(self._player_board, self._computer_board)

    def _player_play(self):
        x, y = self._ui.get_play_coordinates()
        hit, boat = self._computer_board.check_hit(x, y)
        if hit:
            print("Hit!")
            if self._computer_board.check_ship_sunk(boat):
                print("You sunk a battleship!")
                self._player_hits += 1
        else:
            print("Miss!")
            self._player_misses += 1

    def _computer_play(self):
        self._computer.play(self._player_board)
