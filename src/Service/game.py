from src.board import PlayerBoard, ComputerBoard

class Game:
    def __init__(self, player_board: PlayerBoard, computer_board: ComputerBoard, battleships: int, battle_ship_length: list):
        self._player_board = player_board
        self._computer_board = computer_board
        self._battleships = battleships
        self._battle_ship_length = battle_ship_length
        self._player_turn = True
        self._game_over = False
        self._winner = None
        self._player_hits = 0
        self._computer_hits = 0
        self._player_misses = 0
        self._computer_misses = 0
        self._player_battleships = battleships
        self._computer_battleships = battleships

    def start(self):
        while not self._game_over:
            self._player_turn = True
            self._player_turn()
            self._player_turn = False
            self._computer_turn()
            self._check_game_over()
        self._display_winner()

    def _place_battleships(self):

