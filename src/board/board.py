from enum import Enum

class ShipDirection(Enum):
    HORIZONTAL = 1
    VERTICAL = 2

class Board:
    HIT =  -1
    MISS = -2
    SHIP = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def __init__(self, board_size: int):
        self._board_size = board_size
        self._board = [[0 for _ in range(board_size)] for _ in range(board_size)]
        self.__battleships = []
        self._battleships_remaining = 0

    def place_battleships(self, battle_ship_length: int, x: int, y: int, direction: ShipDirection, ship_number: int):
        """
        Place a battleship on the board
        :param battle_ship_length: Indicates the length of the ship
        :type battle_ship_length: int
        :param x: Indicates the x coordinate of the ship
        :type x: int
        :param y: Indicates the y coordinate of the ship
        :type y: int
        :param direction: Indicates the direction of the ship
        :type direction: ShipDirection
        :param ship_number: The number of the ship
        :type ship_number: int
        :return: None
        """
        self.__validate_placement(battle_ship_length, direction, x, y)

        # Place the ship
        if direction == ShipDirection.HORIZONTAL:
            for i in range(battle_ship_length):
                self._board[y][x + i] = ship_number
        else:
            for i in range(battle_ship_length):
                self._board[y + i][x] = ship_number
        self.__battleships.append((x, y, direction, battle_ship_length, ship_number))
        self._battleships_remaining += 1

    def __validate_placement(self, battle_ship_length, direction, x, y):
        """
        Validate if the ship can be placed on the board
        :param battle_ship_length: Indicates the length of the ship
        :type battle_ship_length: int
        :param direction: Indicates the direction of the ship
        :type direction: ShipDirection
        :param x: Indicates the x coordinate of the ship
        :type x: int
        :param y: Indicates the y coordinate of the ship
        :type y: int
        :return: None
        """
        # Check if the coordinates are valid
        if direction == ShipDirection.HORIZONTAL and x + battle_ship_length > self._board_size:
            raise ValueError("Ship cannot be placed")
        if direction == ShipDirection.VERTICAL and y + battle_ship_length > self._board_size:
            raise ValueError("Ship cannot be placed")
        # Check if the ship overlaps with another ship
        if direction == ShipDirection.HORIZONTAL:
            for i in range(battle_ship_length):
                if self._board[y][x + i] != 0:
                    raise ValueError("Ship overlaps with another ship")
        else:
            for i in range(battle_ship_length):
                if self._board[y + i][x] != 0:
                    raise ValueError("Ship overlaps with another ship")

    def check_hit(self, x: int, y: int) -> (bool, int):
        """
        Check if a hit is a hit or a miss
        :param x: Indicates the x coordinate of the hit
        :type x: int
        :param y: Indicates the y coordinate of the hit
        :type y: int
        :return: Returns a tuple with a boolean indicating if the hit is a hit or a miss and the ship number if it is a hit
        :rtype: tuple
        """
        # Check if the coordinates are valid
        if y < 0 or y >= self._board_size or x < 0 or x >= self._board_size:
            raise ValueError("Invalid coordinates")
        if self._board[y][x] == -1 or self._board[y][x] == -2:
            raise ValueError("Already hit")

        # Check if the hit is a miss or a hit
        if self._board[y][x] == 0:
            self._board[y][x] = -2
            return False, None

        boat = self._board[y][x]
        self._board[y][x] = -1
        return True, boat

    def check_ship_sunk(self, ship_number: int) -> bool:
        """
        Check if a ship is sunk
        :param ship_number: Indicates the ship number
        :type ship_number: int
        :return: Returns a boolean indicating if the ship is sunk
        :rtype: bool
        """
        for x, y, direction, length, ship in self.__battleships:
            if ship_number == ship:
                if direction == ShipDirection.HORIZONTAL:
                    for i in range(length):
                        if self._board[y][x + i] != -1:
                            return False
                else:
                    for i in range(length):
                        if self._board[y + i][x] != -1:
                            return False
                return True
        return False

    def check_game_over(self) -> bool:
        """
        Check if the game is over
        :return: True if the game is over, False otherwise
        :rtype: bool
        """
        return self._battleships_remaining == 0

    def get_cell(self, x, y):
        return self._board[x][y]

    @property
    def get_size(self) -> int:
        return self._board_size

class PlayerBoard(Board):
    def __init__(self, board_size: int):
        super().__init__(board_size)
        self._battleships_remaining = 0

    def place_battleships(self, battle_ship_length: int, x: int, y: int, direction: str, ship_number: int):
        direction = direction.lower()
        direction = ShipDirection.HORIZONTAL if (direction == "h" or direction == "horizontal") else ShipDirection.VERTICAL if (direction == "v" or direction == "vertical") else None
        super().place_battleships(battle_ship_length, x, y, direction, ship_number)

    def check_hit(self, x, y) -> (bool, int):
        hit, boat = super().check_hit(x, y)
        if hit:
            if super().check_ship_sunk(boat):
                self._battleships_remaining -= 1
        return hit, boat

    def __str__(self):
        # Create the top margin line
        board_str = "    " + "  ".join([str(i + 1).rjust(2) for i in range(self._board_size)]) + "\n"
        board_str += "   +" + "---+" * self._board_size + "\n"

        for y in range(self._board_size):
            # Create each row with a left margin line
            row_str = str(y + 1).rjust(2) + " |"
            for cell in self._board[y]:
                if cell == -1:
                    row_str += " . |"
                elif cell == -2:
                    row_str += " X |"
                elif cell == 0:
                    row_str += "   |"
                else:
                    row_str += f" {cell} |"
            row_str += "\n"
            board_str += row_str
            # Add a line between rows
            board_str += "   +" + "---+" * self._board_size + "\n"
        return board_str



class ComputerBoard(Board):
    def __init__(self, board_size: int):
        super().__init__(board_size)
        self._battleships_remaining = 0

    def place_battleships(self, battle_ship_length: int, x: int, y: int, direction: ShipDirection, ship_number: int):
        super().place_battleships(battle_ship_length, x, y, direction, ship_number)

    def check_hit(self, x, y) -> (bool, int):
       # print(self._battleships_remaining)
        hit, boat = super().check_hit(x, y)
        if hit:
            if super().check_ship_sunk(boat):
                self._battleships_remaining -= 1
        return hit, boat

    def __str__(self):
        # Create the top margin line
        board_str = "    " + "  ".join([str(i + 1).rjust(2) for i in range(self._board_size)]) + "\n"
        board_str += "   +" + "---+" * self._board_size + "\n"

        for y in range(self._board_size):
            # Create each row with a left margin line
            row_str = str(y + 1).rjust(2) + " |"
            for cell in self._board[y]:
                if cell == -1:
                    row_str += " . |"
                elif cell == -2:
                    row_str += " X |"
                else:
                    row_str += "   |"
            row_str += "\n"
            board_str += row_str
            # Add a line between rows
            board_str += "   +" + "---+" * self._board_size + "\n"
        return board_str