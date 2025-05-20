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

# Comic-style colors
COMIC_BLUE = (41, 128, 185)
COMIC_RED = (231, 76, 60)
COMIC_GREEN = (46, 204, 113)
COMIC_YELLOW = (241, 196, 15)
COMIC_PURPLE = (142, 68, 173)
COMIC_ORANGE = (230, 126, 34)
COMIC_DARK = (44, 62, 80)
COMIC_LIGHT = (236, 240, 241)

# UI Colors
UI_BG = (52, 73, 94)
UI_PANEL = (44, 62, 80)
UI_BUTTON = (41, 128, 185)
UI_BUTTON_HOVER = (52, 152, 219)
UI_BUTTON_DISABLED = (127, 140, 141)
UI_TEXT = (236, 240, 241)
UI_HIGHLIGHT = (241, 196, 15)
UI_DANGER = (231, 76, 60)
UI_SUCCESS = (46, 204, 113)
UI_PATH1 = (52, 152, 219)  # Blue
UI_PATH2 = (230, 126, 34)  # Orange

# Game settings
FPS = 60  # Cap the frame rate to 60 FPS for performance
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
                {'name': 'Faster Firing', 'cost': 150, 'cooldown_multiplier': 0.8, 'description': 'Increases attack speed by 25%'},
                {'name': 'Rapid Fire', 'cost': 300, 'cooldown_multiplier': 0.6, 'description': 'Doubles attack speed'},
                {'name': 'Hypersonic', 'cost': 600, 'cooldown_multiplier': 0.4, 'description': 'Fires at incredible speeds'}
            ],
            'path2': [
                {'name': 'Enhanced Damage', 'cost': 200, 'damage_multiplier': 1.5, 'description': 'Increases damage by 50%'},
                {'name': 'Heavy Rounds', 'cost': 400, 'damage_multiplier': 2.0, 'description': 'Doubles damage output'},
                {'name': 'Devastating Shots', 'cost': 800, 'damage_multiplier': 3.0, 'description': 'Triple damage with armor penetration'}
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
                {'name': 'Enhanced Scope', 'cost': 200, 'range_multiplier': 1.5, 'description': 'Increases attack range by 50%'},
                {'name': 'Long Range', 'cost': 400, 'range_multiplier': 2.0, 'cooldown_multiplier': 0.9, 'description': 'Doubles range and slightly improves firing speed'},
                {'name': 'Global Range', 'cost': 800, 'range_multiplier': 10.0, 'description': 'Can target enemies anywhere on the map'}
            ],
            'path2': [
                {'name': 'Armor Piercing', 'cost': 300, 'damage_multiplier': 2.0, 'description': 'Doubles damage against all enemies'},
                {'name': 'Critical Hits', 'cost': 600, 'damage_multiplier': 3.0, 'adds_critical': True, 'description': 'Chance to deal triple damage with critical hits'},
                {'name': 'One Shot One Kill', 'cost': 1200, 'damage_multiplier': 5.0, 'critical_chance': 0.3, 'description': 'Massive damage with 30% chance of instant elimination'}
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
                {'name': 'Wider Blast', 'cost': 200, 'splash_radius_multiplier': 1.5, 'description': 'Increases explosion radius by 50%'},
                {'name': 'Massive Explosion', 'cost': 400, 'splash_radius_multiplier': 2.0, 'description': 'Doubles explosion radius'},
                {'name': 'Nuclear Blast', 'cost': 800, 'splash_radius_multiplier': 3.0, 'damage_multiplier': 1.5, 'description': 'Huge explosions with increased damage'}
            ],
            'path2': [
                {'name': 'Burning Effect', 'cost': 250, 'adds_burning': True, 'description': 'Adds burning damage over time'},
                {'name': 'Inferno', 'cost': 500, 'burning_damage_multiplier': 2.0, 'description': 'Doubles burning damage'},
                {'name': 'Hellfire', 'cost': 1000, 'burning_damage_multiplier': 3.0, 'splash_radius_multiplier': 1.5, 'description': 'Triple burning damage with increased area'}
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
                {'name': 'Extended Range', 'cost': 200, 'range_multiplier': 1.5, 'description': 'Increases support range by 50%'},
                {'name': 'Wide Support', 'cost': 500, 'range_multiplier': 2.5, 'description': 'More than doubles support range'},
                {'name': 'Global Support', 'cost': 1000, 'range_multiplier': 10.0, 'description': 'Supports all towers on the map'}
            ],
            'path2': [
                {'name': 'Enhanced Buff', 'cost': 300, 'buff_multiplier': 1.5, 'description': 'Increases buff strength by 50%'},
                {'name': 'Powerful Buff', 'cost': 600, 'buff_multiplier': 2.0, 'description': 'Doubles the buff effect'},
                {'name': 'Ultimate Buff', 'cost': 1200, 'buff_multiplier': 3.0, 'adds_special_ability': True, 'description': 'Triple buff with special ability boost'}
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
