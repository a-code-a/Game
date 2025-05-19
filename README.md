# Minion Tower Defense

A tower defense game inspired by Bloons Tower Defense 6, featuring minions as attackers and Gru as the defender.

## Features

- Multiple tower types with different abilities
- Upgrade trees with 2 paths per tower
- Various enemy types with different properties
- Wave-based gameplay with increasing difficulty
- Economy system with coins for killing enemies
- Multiple maps
- Extensible architecture for easy additions and modifications

## How to Play

1. Run the game:
   ```
   python src/main.py
   ```

2. Place towers on the map to defend against waves of minions
3. Upgrade your towers to make them more powerful
4. Start waves when you're ready
5. Survive as long as possible!

## Tower Types

- **Basic Tower**: Balanced tower with moderate damage and range
- **Sniper Tower**: Long range with high damage but slow firing rate
- **Area Tower**: Deals splash damage to multiple enemies
- **Support Tower**: Buffs nearby towers

## Upgrade Paths

Each tower has two upgrade paths:

- **Path 1**: Usually focuses on attack speed or range
- **Path 2**: Usually focuses on damage or special abilities

You can upgrade a tower up to 2 times on each path, but if you reach level 2 on one path, the other path becomes locked.

## Enemy Types

- **Basic Minion**: Standard enemy with balanced stats
- **Fast Minion**: Moves quickly but has less health
- **Tank Minion**: Slow but has high health
- **Boss Minion**: Very high health and deals more damage

## Requirements

- Python 3.6+
- Pygame

## Installation

1. Clone the repository
2. Install the required packages:
   ```
   pip install pygame
   ```
3. Run the game:
   ```
   python src/main.py
   ```

## Extending the Game

### Adding New Towers

1. Create a new tower class in `src/towers/`
2. Add the tower configuration to `TOWER_TYPES` in `src/constants.py`
3. Add the tower image to `assets/images/towers/`

### Adding New Enemies

1. Create a new enemy class in `src/enemies/`
2. Add the enemy configuration to `ENEMY_TYPES` in `src/constants.py`
3. Add the enemy image to `assets/images/enemies/`

### Adding New Maps

1. Create a new map class in `src/maps/`
2. Add the map image to `assets/images/maps/`

## Credits

- Game developed by [Your Name]
- Inspired by Bloons Tower Defense 6
- Minions and Gru are characters from the Despicable Me franchise
