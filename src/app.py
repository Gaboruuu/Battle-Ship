from src.ui.console_ui import ConsoleUI
from src.Service.game import Game

if __name__ == '__main__':
    Game = Game(ConsoleUI())
    Game.start()