import random

from src.board.board import ShipDirection, ComputerBoard, PlayerBoard


class ComputerPlayer:
    def __init__(self, board: ComputerBoard):
        self.__board = board
        self.__board_size = board.get_size
        self.__hits = set()
        self.__potential_targets = []

    def place_battleships(self, computer_battleships : int, computer_battleships_length: list) -> None:
        """
        Place battleships on the computer board
        :param computer_battleships:  Number of battleships to place
        :type computer_battleships: int
        :param computer_battleships_length: List of battleship lengths
        :type computer_battleships_length: list
        :return: None
        """
        for index in range(1, computer_battleships + 1):
            placed = False
            while not placed:
                x = random.randint(0, self.__board_size - 1)
                y = random.randint(0, self.__board_size - 1)
                direction = random.choice(list(ShipDirection))
                #print(_computer_battleships_length)
                length = random.choice(computer_battleships_length)
                try:
                    self.__board.place_battleships(length, x, y, direction, index)
                    placed = True
                    computer_battleships_length.remove(length)
                except ValueError:
                    continue

    def play(self, player_board : PlayerBoard, game) -> tuple:
        """
        Play a turn for the computer
        :param player_board: Player board to attack
        :type player_board: PlayerBoard
        :param game: The game object
        :type game: Game
        :return: Tuple of coordinates for the computer's move
        :rtype: tuple
        """
        if self.__potential_targets:
            # Sort potential targets by proximity to other known hits
            self.__potential_targets.sort(key=lambda coord: self.__count_adjacent_hits(coord), reverse=True)
            x, y = self.__potential_targets.pop(0)
        else:
            x, y = self.__get_weighted_random_hit()

        try:
            hit, boat = player_board.check_hit(x, y)
            if hit:
                game.ui.print_result(hit, "Computer")
                game.computer_hits += 1
                if player_board.check_ship_sunk(boat):
                    game.ui.print_sunk("Computer")
                    self.__potential_targets.clear()  # Clear potential targets if a ship is sunk
                else:
                    self.__add_potential_targets(x, y)
            else:
                game.ui.print_result(hit, "Computer")
                game.computer_misses += 1
        except ValueError:
            self.play(player_board, game)  # Retry if the move was invalid
        return x, y

    def __get_weighted_random_hit(self) -> tuple:
        """
        Get a random hit weighted towards the center and corners of the board
        :return: Tuple of coordinates for the computer's move
        :rtype: tuple
        """
        # Weight cells towards the center and corners of the board for initial random hits
        while True:
            x = random.choices(range(self.__board_size), weights=self.__combined_weights())[0]
            y = random.choices(range(self.__board_size), weights=self.__combined_weights())[0]
            if (x, y) not in self.__hits:
                self.__hits.add((x, y))
                return x, y

    def __add_potential_targets(self, x: int, y: int) -> None:
        """
        Add potential targets around a hit to prioritize targeting nearby cells
        :param x:  x-coordinate of the hit
        :type x:  int
        :param y:  y-coordinate of the hit
        :type y:  int
        :return: None
        """
        # Add adjacent cells along the axis of the hit to prioritize likely ship placements
        potential_moves = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        for move in potential_moves:
            if 0 <= move[0] < self.__board_size and 0 <= move[1] < self.__board_size and move not in self.__hits:
                self.__potential_targets.append(move)

    def __count_adjacent_hits(self, coord: tuple) -> int:
        """
        Count the number of adjacent hits to a coordinate
        :param coord:  Coordinates to check
        :type coord:  tuple
        :return:  Number of adjacent hits
        :rtype:  int
        """
        # Count the number of adjacent hits to prioritize targeting cells near clusters of hits
        x, y = coord
        adjacent_hits = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        return sum(1 for adj in adjacent_hits if adj in self.__hits)

    def __center_weights(self) -> list:
        """
        Generate weights for prioritizing the center of the board
        :return: List of weights for each cell
        :rtype: list
        """
        # Generate weights for prioritizing the center of the board
        center = self.__board_size // 2
        return [center - abs(center - i) for i in range(self.__board_size)]

    def __corner_weights(self) -> list:
        """
        Generate weights for prioritizing the corners of the board
        :return: Returns a list of weights for each cell
        :rtype: list
        """
        # Generate weights for prioritizing corners of the board
        weights = [1] * self.__board_size
        weights[0] += 3  # Top-left corner
        weights[-1] += 3  # Top-right corner
        weights[self.__board_size // 2] += 2  # Middle rows
        return weights

    def __combined_weights(self) -> list:
        """
        Combine center and corner weights for better random selection
        :return: Returns a list of weights for each cell
        :rtype: list
        """
        # Combine center and corner weights for better random selection
        center_weights = self.__center_weights()
        corner_weights = self.__corner_weights()
        return [cw + cc for cw, cc in zip(center_weights, corner_weights)]
