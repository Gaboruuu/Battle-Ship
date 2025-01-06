from enum import Enum
import random

class ShipDirection(Enum):
    HORIZONTAL = 1
    VERTICAL = 2

class Board:
    def __init__(self, board_size: int):
        self._board_size = board_size
        self._board = [[0 for _ in range(board_size)] for _ in range(board_size)]
        self._battleships = []
        self._hits = 0
        self._misses = 0
        self._battleships_remaining = 0

    def place_battleships(self, battle_ship_length: int, x: int, y: int, direction: ShipDirection, ship_number: int):
        # Check if the ship can be placed
        self.validate_placement(battle_ship_length, direction, x, y)

        # Place the ship
        if direction == ShipDirection.HORIZONTAL:
            for i in range(battle_ship_length):
                self._board[y][x + i] = ship_number
        else:
            for i in range(battle_ship_length):
                self._board[y + i][x] = ship_number
        self._battleships.append((x, y, direction, battle_ship_length, ship_number))
        self._battleships_remaining += 1

    def validate_placement(self, battle_ship_length, direction, x, y):
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

    def check_hit(self, x, y) -> (bool, int):
        # Check if the coordinates are valid
        if y < 0 or y >= self._board_size or x < 0 or x >= self._board_size:
            raise ValueError("Invalid coordinates")
        if self._board[y][x] == -1:
            raise ValueError("Already hit")

        # Check if the hit is a miss or a hit
        if self._board[y][x] == 0:
            self._misses += 1
            self._board[y][x] = -1
            return False, None

        self._hits += 1
        boat = self._board[y][x]
        self._board[y][x] = -1
        return True, boat

    def check_ship_sunk(self, ship_number: int):
        for x, y, direction, length, ship in self._battleships:
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
        return self._battleships_remaining == 0

    def __str__(self):
        # Create the top margin line
        board_str = "    " + "  ".join([str(i + 1).rjust(2) for i in range(self._board_size)]) + "\n"
        board_str += "   +" + "---+" * self._board_size + "\n"

        for y in range(self._board_size):
            # Create each row with a left margin line
            row_str = str(y + 1).rjust(2) + " |" + " |".join([str(cell).rjust(2) for cell in self._board[y]]) + " |\n"
            board_str += row_str
            # Add a line between rows
            board_str += "   +" + "---+" * self._board_size + "\n"
        return board_str

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



class ComputerBoard(Board):
    def __init__(self, board_size: int):
        super().__init__(board_size)
        self._battleships_remaining = 0

    def place_battleships(self, battle_ship_length: int, x: int, y: int, direction: ShipDirection, ship_number: int):
        super().place_battleships(battle_ship_length, x, y, direction, ship_number)

    def check_hit(self, x, y) -> (bool, int):
        print(self._battleships_remaining)
        hit, boat = super().check_hit(x, y)
        if hit:
            if super().check_ship_sunk(boat):
                self._battleships_remaining -= 1
        return hit, boat