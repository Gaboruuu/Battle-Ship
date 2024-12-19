def get_ui():
    with open('settings.properties', 'r') as f:
        line = f.read()
        if line == 'ui = console':
            from ui.console_ui import ConsoleUI
            return ConsoleUI()
        elif line == 'ui=gui':
            from ui.pygame_ui import PygameUI
            return PygameUI()
        else:
            raise ValueError('Invalid UI setting')


if __name__ == '__main__':
    Ui = get_ui()
    Ui.run()