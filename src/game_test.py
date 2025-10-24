import unittest
from unittest.mock import Mock, patch
from src.Service.game import Game, get_board_size, get_battleships, get_battle_ship_length
from src.board.board import PlayerBoard, ComputerBoard
from src.ui.ui_interface import UiInterface

class TestGame(unittest.TestCase):

    def setUp(self):
        self.ui = Mock(spec=UiInterface)
        with patch('src.Service.game.get_board_size', return_value=10), \
            patch('src.Service.game.get_battleships', return_value=5), \
            patch('src.Service.game.get_battle_ship_length', return_value=[2, 3, 3, 4, 5]):
            self.game = Game(self.ui)

    def test_get_board_size(self):
        self.assertEqual(get_board_size(), 10)  # Assuming the board size is 10 in settings.properties

    def test_get_battleships(self):
        self.assertEqual(get_battleships(), 5)  # Assuming the number of battleships is 5 in settings.properties

    def test_get_battle_ship_length(self):
        self.assertEqual(get_battle_ship_length(), [2, 3, 3, 4, 5])  # Assuming these lengths in settings.properties

    def test_place_player_ship(self):
        self.ui.get_placement.return_value = (0, 0, 'Horizontal', 3)
        self.game.place_player_ship(1)
        self.assertEqual(self.game.player_board.get_cell(0, 0), 1)
        self.assertEqual(self.game.player_board.get_cell(0, 1), 1)
        self.assertEqual(self.game.player_board.get_cell(0, 2), 1)

    def test_place_computer_battleships(self):
        self.game.place_computer_battleships()
        self.assertEqual(len(self.game.computer_board.ships), 5)  # Assuming 5 ships

    def test_player_play_hit(self):
        self.ui.get_play_coordinates.return_value = (0, 0)
        self.game.computer_board.place_battleships(3, 0, 0, 'Horizontal', 1)
        self.game.player_play()
        self.assertEqual(self.game.computer_board.get_cell(0, 0), ComputerBoard.HIT)

    def test_player_play_miss(self):
        self.ui.get_play_coordinates.return_value = (0, 0)
        self.game.player_play()
        self.assertEqual(self.game.computer_board.get_cell(0, 0), ComputerBoard.MISS)

    def test_game_over(self):
        self.game.computer_board.place_battleships(3, 0, 0, 'Horizontal', 1)
        self.game.computer_board.place_battleships(3, 1, 0, 'Horizontal', 2)
        self.game.computer_board.place_battleships(3, 2, 0, 'Horizontal', 3)
        self.game.computer_board.place_battleships(3, 3, 0, 'Horizontal', 4)
        self.game.computer_board.place_battleships(3, 4, 0, 'Horizontal', 5)
        for i in range(5):
            for j in range(3):
                self.game.computer_board.hit(i, j)
        self.assertTrue(self.game.computer_board.check_game_over())

if __name__ == '__main__':
    unittest.main()