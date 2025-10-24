# 🚢 Battleship Game

A Python implementation of the classic Battleship game with both console and graphical (Pygame) interfaces. Play against an intelligent computer opponent that uses strategic targeting algorithms.

## 📋 Features

- **Dual UI Support**: Choose between console-based or Pygame graphical interface
- **Configurable Game Settings**: Customize board size, number of ships, and ship lengths
- **Smart AI Opponent**: Computer player uses intelligent targeting strategies
- **Ship Placement**: Place your battleships horizontally or vertically on the board
- **Real-time Feedback**: Track hits, misses, and remaining ships
- **Game Statistics**: View final game statistics including hit/miss ratios

## 🎮 Game Modes

### Console UI

A text-based interface for quick gameplay in the terminal.

### Pygame UI

A graphical interface with visual board representation and mouse controls.

## 🛠️ Installation

### Prerequisites

- Python 3.x
- Pygame (for graphical UI)

### Setup

1. Clone the repository:

```bash
git clone https://github.com/Gaboruuu/Battle-Ship.git
cd a10-Gabor-Gabriel
```

2. Install dependencies:

```bash
pip install pygame
```

## ⚙️ Configuration

Edit the `src/settings.properties` file to customize your game:

```properties
ui=pygame                    # Options: pygame, console
board_size=6                 # Size of the game board (6x6)
battleships=4                # Number of battleships
battle_ship_length=2,3,4     # Lengths of individual battleships
```

### Configuration Options:

- **ui**: Choose between `pygame` (graphical) or `console` (text-based)
- **board_size**: Size of the square game board (e.g., 6 creates a 6x6 grid)
- **battleships**: Number of ships to place on the board
- **battle_ship_length**: Comma-separated list of ship lengths

## 🚀 How to Run

Navigate to the project directory and run:

```bash
python src/app.py
```

Or from the src directory:

```bash
cd src
python app.py
```

## 🎯 How to Play

### Ship Placement Phase

1. When the game starts, you'll be prompted to place your battleships
2. For **Console UI**: Enter coordinates, direction (HORIZONTAL/VERTICAL or h/v), and ship length
3. For **Pygame UI**: Click on the board to place ships

### Attack Phase

1. Take turns with the computer to attack coordinates on the opponent's board
2. For **Console UI**: Enter x and y coordinates
3. For **Pygame UI**: Click on the opponent's board to attack
4. Track hits (successful attacks) and misses
5. First player to sink all opponent's ships wins!

### Board Symbols (Console UI)

- `0`: Empty water
- `1-10`: Your ships
- `-1`: Hit
- `-2`: Miss

## 📁 Project Structure

```
a10-Gabor-Gabriel/
├── src/
│   ├── app.py                    # Main entry point
│   ├── settings.properties       # Game configuration
│   ├── game_test.py             # Unit tests
│   ├── board/
│   │   ├── __init__.py
│   │   └── board.py             # Board logic (PlayerBoard, ComputerBoard)
│   ├── Service/
│   │   ├── __init__.py
│   │   ├── game.py              # Game logic and flow
│   │   └── computer_player.py   # AI player implementation
│   └── ui/
│       ├── __init__.py
│       ├── ui_interface.py      # UI abstract interface
│       ├── console_ui.py        # Console-based UI
│       └── pygame_ui.py         # Pygame graphical UI
└── README.md
```

## 🧠 AI Strategy

The computer player implements an intelligent targeting system:

- **Random Search**: Initially attacks random coordinates
- **Hunt Mode**: When a ship is hit, targets adjacent cells
- **Target Queue**: Maintains a list of potential ship locations
- **Proximity Targeting**: Prioritizes coordinates near previous hits

## 🧪 Testing

Run the test suite:

```bash
python src/game_test.py
```

## 🎓 Academic Project

This project was developed as an assignment (a10) for an Informatics course, demonstrating:

- Object-oriented programming principles
- Separation of concerns (UI, logic, data)
- Strategy pattern for AI implementation
- Multiple interface implementations
- Configuration-driven application design

## 📝 License

This is an academic project for educational purposes.

## 👨‍💻 Author

**Gabor Gabriel**

- GitHub: [@Gaboruuu](https://github.com/Gaboruuu)

## 🤝 Contributing

This is an academic assignment, but suggestions and feedback are welcome!

---

**Enjoy the game and happy sailing! ⚓**
