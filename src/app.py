from src.ui.console_ui import ConsoleUI
from src.Service.game import Game
from src.ui.pygame_ui import PygameUI

def get_ui():
    ui = None
    with open('settings.properties', 'r') as f:
        for line in f:
            if 'ui' in line:
                ui = line.split('=')[1].strip()
    if ui == 'pygame':
        return PygameUI()
    elif ui == 'console':
        return ConsoleUI()

    raise ValueError('Invalid ui setting')

if __name__ == '__main__':
    Game = Game(get_ui())
    Game.start()