"""
Constants for the Tower Defense Game
"""

# Screen dimensions
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SIDEBAR_WIDTH = 200

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
TRANSPARENT = (0, 0, 0, 0)

# Game settings
FPS = 60
GRID_SIZE = 64
STARTING_COINS = 500
STARTING_LIVES = 100

# Tower types
TOWER_TYPES = {
    'basic': {
        'cost': 100,
        'damage': 10,
        'range': 150,
        'cooldown': 1.0,
        'upgrade_paths': {
            'path1': [
                {'name': 'Faster Firing', 'cost': 150, 'cooldown_multiplier': 0.8},
                {'name': 'Even Faster Firing', 'cost': 300, 'cooldown_multiplier': 0.6}
            ],
            'path2': [
                {'name': 'Increased Damage', 'cost': 200, 'damage_multiplier': 1.5},
                {'name': 'Heavy Damage', 'cost': 400, 'damage_multiplier': 2.0}
            ]
        }
    },
    'sniper': {
        'cost': 250,
        'damage': 50,
        'range': 500,
        'cooldown': 3.0,
        'upgrade_paths': {
            'path1': [
                {'name': 'Long Range', 'cost': 200, 'range_multiplier': 1.5},
                {'name': 'Global Range', 'cost': 400, 'range_multiplier': 10.0}
            ],
            'path2': [
                {'name': 'Armor Piercing', 'cost': 300, 'damage_multiplier': 2.0},
                {'name': 'One Shot One Kill', 'cost': 600, 'damage_multiplier': 5.0}
            ]
        }
    },
    'area': {
        'cost': 300,
        'damage': 15,
        'range': 120,
        'cooldown': 2.0,
        'splash_radius': 80,
        'upgrade_paths': {
            'path1': [
                {'name': 'Larger Radius', 'cost': 200, 'splash_radius_multiplier': 1.5},
                {'name': 'Massive Explosion', 'cost': 400, 'splash_radius_multiplier': 2.0}
            ],
            'path2': [
                {'name': 'Burning Effect', 'cost': 250, 'adds_burning': True},
                {'name': 'Inferno', 'cost': 500, 'burning_damage_multiplier': 2.0}
            ]
        }
    },
    'support': {
        'cost': 350,
        'damage': 0,
        'range': 200,
        'cooldown': 0,
        'buff_multiplier': 1.2,
        'upgrade_paths': {
            'path1': [
                {'name': 'Increased Range', 'cost': 200, 'range_multiplier': 1.5},
                {'name': 'Global Support', 'cost': 500, 'range_multiplier': 10.0}
            ],
            'path2': [
                {'name': 'Stronger Buff', 'cost': 300, 'buff_multiplier': 1.5},
                {'name': 'Ultimate Buff', 'cost': 600, 'buff_multiplier': 2.0}
            ]
        }
    }
}

# Enemy types
ENEMY_TYPES = {
    'basic_minion': {
        'health': 50,
        'speed': 1.0,
        'reward': 10,
        'damage': 1
    },
    'fast_minion': {
        'health': 30,
        'speed': 2.0,
        'reward': 15,
        'damage': 1
    },
    'tank_minion': {
        'health': 200,
        'speed': 0.5,
        'reward': 30,
        'damage': 2
    },
    'boss_minion': {
        'health': 1000,
        'speed': 0.7,
        'reward': 200,
        'damage': 10
    }
}

# Wave settings
WAVE_COOLDOWN = 10  # seconds between waves
