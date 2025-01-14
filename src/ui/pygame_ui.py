import pygame
from abc import ABC
from src.Service.game import get_board_size
from src.board.board import Board
from src.ui.ui_interface import UiInterface


class PygameUI(UiInterface, ABC):
    def __init__(self):
        """
        Initialize the PygameUI class.
        """
        super().__init__()
        self.__game = None
        self.__board_size = get_board_size()
        self.__panel_size = 400  # Fixed panel size
        self.__cell_size = self.__panel_size // self.__board_size  # Calculate cell size based on board size
        self.__margin = 10
        self.__panel_offset = 100  # Space for titles above boards
        self.__screen_width = 1200  # Two panels and margins
        self.__screen_height = 600
        self.__log_panel_width = 200
        self.__log_panel_height = self.__screen_height - 2 * self.__margin
        self.__log_panel = pygame.Surface((self.__log_panel_width, self.__log_panel_height))
        self.__log_panel_rect = self.__log_panel.get_rect(topleft=(self.__screen_width - self.__log_panel_width - self.__margin, self.__margin))
        self.__logs = []
        self.__log_scroll_offset = 0

        pygame.init()
        self.__screen = pygame.display.set_mode((self.__screen_width, self.__screen_height))
        pygame.display.set_caption("Battleship")
        self.__font = pygame.font.Font(None, 36)
        self.__log_font = pygame.font.Font(None, 24)

        self.running = True
        self.placing_ships = True

    def print_board(self, board: Board):
        """
        Print a single board.

        :param board: Board - The board to be printed.
        """
        self.__display_boards()

    def print_boards(self, player_board: Board, computer_board: Board):
        """
        Print both player and computer boards.

        :param player_board: Board - The player's board.
        :param computer_board: Board - The computer's board.
        """
        self.__display_boards()

    def run(self, game):
        """
        Run the game loop.

        :param game: Game - The game instance.
        :return: PygameUI - The PygameUI instance.
        """
        self.__game = game
        self.__handle_events()
        self.__display_boards()
        pygame.display.flip()
        return self

    def __handle_events(self):
        """
        Handle Pygame events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    self.__log_scroll_offset = min(self.__log_scroll_offset + 20, 0)
                elif event.button == 5:  # Scroll down
                    max_offset = -(len(self.__logs) * (self.__log_font.get_height() + 5) - self.__log_panel_height)
                    self.__log_scroll_offset = max(self.__log_scroll_offset - 20, max_offset)

    def __display_boards(self):
        """
        Display both player and computer boards on the screen.
        """
        self.__screen.fill((0, 0, 0))
        # Draw computer's board
        self.__draw_board(self.__game.computer_board, 50, "Computer")

        # Draw player's board
        player_board_x_offset = self.__board_size * self.__cell_size + self.__margin + 100
        self.__draw_board(self.__game.player_board, player_board_x_offset, "Player")

        self.__draw_log_panel()

        pygame.display.flip()

    def __draw_log_panel(self):
        """
        Draw the log panel on the screen.
        """
        self.__log_panel.fill((50, 50, 50))  # Background color for log panel
        y_offset = self.__log_scroll_offset
        log_line_height = self.__log_font.get_height() + 5

        for log in self.__logs:
            log_surface = self.__log_font.render(log, True, (255, 255, 255))
            if 0 <= y_offset < self.__log_panel_height:  # Only draw visible logs
                self.__log_panel.blit(log_surface, (5, y_offset))
            y_offset += log_line_height

        self.__screen.blit(self.__log_panel, self.__log_panel_rect)

    def __draw_board(self, board: Board, x_offset: int, title: str):
        """
        Draw a single board on the screen.

        :param board: Board - The board to be drawn.
        :param x_offset: int - The x offset for the board.
        :param title: str - The title of the board.
        """
        for row in range(self.__board_size):
            for col in range(self.__board_size):
                cell_value = board.get_cell(row, col)
                color = (255, 255, 255)  # Default white
                if cell_value == Board.HIT:
                    color = (255, 0, 0)  # Red for hit
                elif cell_value == Board.MISS:
                    color = (0, 0, 255)  # Blue for miss
                elif cell_value > 0 and board == self.__game.player_board:
                    color = (0, 255, 0)  # Green for ship (player's board only)

                rect = pygame.Rect(
                    x_offset + col * self.__cell_size,
                    self.__margin + self.__panel_offset + row * self.__cell_size,
                    self.__cell_size - 1,
                    self.__cell_size - 1,
                )
                pygame.draw.rect(self.__screen, color, rect)

        # Draw title
        text_surface = self.__font.render(title, True, (255, 255, 255))
        self.__screen.blit(text_surface, (x_offset + self.__margin, self.__panel_offset // 2))

    def __add_log(self, message: str):
        """
        Add a log message to the log panel.

        :param message: str - The log message to be added.
        """
        self.__logs.append(message)
        if len(self.__logs) * (self.__log_font.get_height() + 5) > self.__log_panel_height:
            self.__log_scroll_offset -= self.__log_font.get_height() + 5

    def get_placement(self, battleship_lengths: list[int]) -> tuple[int, int, str, int] or None:
        """
        Get the placement of a battleship from the user.

        :param battleship_lengths: list[int] - The lengths of the battleships.
        :return: tuple[int, int, str, int] - The column, row, direction, and length of the battleship.
        :return: None - If the user closes the window.
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    return None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    board_width = self.__board_size * self.__cell_size + self.__margin + self.__panel_offset
                    if  board_width < x < board_width + 400:  # Right panel: player's board
                        col = (x - board_width) // self.__cell_size
                        row = (y - self.__panel_offset - self.__margin) // self.__cell_size
                        self.__clear_prompt_area()
                        direction = self.__prompt_direction()
                        length = self.__prompt_length(battleship_lengths)
                        return col, row, direction, length

    def __prompt_length(self, battleship_lengths: list[int]) -> int or None:
        """
        Prompt the user to select the length of the battleship.

        :param battleship_lengths: list[int] - The lengths of the battleships.
        :return: int - The selected length.
        :return: None - If the user closes the window.
        """
        button_width = 100
        button_height = 50
        buttons = []
        y = self.__screen_height - button_height - self.__margin  # Position buttons at the bottom of the screen

        # Draw the prompt text
        prompt_text = self.__font.render("Select the length", True, (255, 255, 255))
        text_x = self.__margin
        text_y = y + button_height // 2 - prompt_text.get_height() // 2
        self.__screen.blit(prompt_text, (text_x, text_y))

        for i, length in enumerate(battleship_lengths):
            x = text_x + prompt_text.get_width() + self.__margin + i * (button_width + self.__margin)
            rect = pygame.Rect(x, y, button_width, button_height)
            buttons.append((rect, length))
            pygame.draw.rect(self.__screen, (255, 255, 255), rect)
            text_surface = self.__font.render(str(length), True, (0, 0, 0))
            self.__screen.blit(text_surface, (x + button_width // 2 - text_surface.get_width() // 2,
                                              y + button_height // 2 - text_surface.get_height() // 2))

        pygame.display.flip()

        selected = None
        while selected is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    return None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for rect, length in buttons:
                        if rect.collidepoint(event.pos):
                            selected = length
                            self.__clear_prompt_area()  # Clear the prompt area after selection
                            return selected

    def __prompt_direction(self) -> str or None:
        """
        Prompt the user to select the direction of the battleship.

        :return: str - The selected direction.
        :return: None - If the user closes the window.
        """
        button_width = 150
        button_height = 50
        directions = ["Horizontal", "Vertical"]
        buttons = []
        y = self.__screen_height - button_height - self.__margin  # Position buttons at the bottom of the screen

        # Draw the prompt text
        prompt_text = self.__font.render("Select the direction", True, (255, 255, 255))
        text_x = self.__margin
        text_y = y + button_height // 2 - prompt_text.get_height() // 2
        self.__screen.blit(prompt_text, (text_x, text_y))

        for i, direction in enumerate(directions):
            x = text_x + prompt_text.get_width() + self.__margin + i * (button_width + self.__margin)
            rect = pygame.Rect(x, y, button_width, button_height)
            buttons.append((rect, direction))
            pygame.draw.rect(self.__screen, (255, 255, 255), rect)
            text_surface = self.__font.render(direction, True, (0, 0, 0))
            self.__screen.blit(text_surface, (x + button_width // 2 - text_surface.get_width() // 2,
                                              y + button_height // 2 - text_surface.get_height() // 2))

        pygame.display.flip()

        selected = None
        while selected is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    return None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for rect, direction in buttons:
                        if rect.collidepoint(event.pos):
                            selected = direction
                            self.__clear_prompt_area()  # Clear the prompt area after selection
                            return selected

    def __clear_prompt_area(self):
        """
        Clear the area where prompts are displayed.
        """
        rect = pygame.Rect(0, self.__screen_height - self.__margin * 6, self.__screen_width, self.__margin * 6)
        pygame.draw.rect(self.__screen, (0, 0, 0), rect)
        pygame.display.flip()

    def __show_prompt(self, text: str):
        """
        Show a prompt message on the screen.

        :param text: str - The prompt message to be displayed.
        """
        prompt_surface = self.__font.render(text, True, (255, 255, 255))
        self.__screen.blit(prompt_surface, (self.__margin, self.__screen_height - self.__margin * 3))

    def get_play_coordinates(self) -> tuple[int, int] or None:
        """
        Get the play coordinates from the user.

        :return: tuple[int, int] - The column and row of the play coordinates.
        :return: None - If the user closes the window.
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    return None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if self.__margin + 50 < x < 50 + self.__board_size * self.__cell_size + self.__margin and self.__panel_offset < y < self.__board_size * self.__cell_size + self.__panel_offset:
                        col = (x - 50) // self.__cell_size
                        row = (y - self.__margin - self.__panel_offset) // self.__cell_size
                        return col, row

    def print_game_over(self, winner: str, player_hits: int, player_misses: int, computer_hits: int, computer_misses: int):
        """
        Print the game over message.

        :param winner: str - The winner of the game.
        :param player_hits: int - The number of hits by the player.
        :param player_misses: int - The number of misses by the player.
        :param computer_hits: int - The number of hits by the computer.
        :param computer_misses: int - The number of misses by the computer.
        """
        message = f"Game Over! Winner: {winner}"
        hits = f"Hits: {player_hits}" if winner == "Player" else f"Hits: {computer_hits}"
        misses = f"Misses: {player_misses}" if winner == "Player" else f"Misses: {computer_misses}"

        self.__screen.fill((0, 0, 0))
        message_surface = self.__font.render(message, True, (255, 255, 255))
        hits_surface = self.__font.render(hits, True, (255, 255, 255))
        misses_surface = self.__font.render(misses, True, (255, 255, 255))

        self.__screen.blit(message_surface, (self.__margin, self.__screen_height // 4))
        self.__screen.blit(hits_surface, (self.__margin, self.__screen_height // 2))
        self.__screen.blit(misses_surface, (self.__margin, self.__screen_height // 2 + 40))

        pygame.display.flip()
        pygame.time.wait(5000)
        self.running = False

    def print_result(self, result: bool, player: str):
        """
        Print the result of a play.

        :param result: bool - The result of the play (hit or miss).
        :param player: str - The player who made the play.
        """
        self.__add_log(f"{player} hit!") if result else self.__add_log(f"{player} missed!")

    def print_sunk(self, player: str):
        """
        Print a message indicating a ship has been sunk.

        :param player: str - The player who sunk the ship.
        """
        self.__add_log(f"{player} has sunk a ship!")

    def print_exception(self, e: Exception):
        """
        Print an exception message.

        :param e: Exception - The exception to be printed.
        """
        self.__add_log(f"Error: {e}")
        self.__draw_log_panel()
        pygame.display.flip()