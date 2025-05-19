"""
Game configuration settings.
"""

# Display settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Tower Defense"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# Game settings
STARTING_RESOURCES = 100
TOWER_COST = 50
TOWER_RANGE = 150
TOWER_DAMAGE = 10
TOWER_COOLDOWN = 1.0  # seconds

# Enemy settings
ENEMY_SPEED = 1.0
ENEMY_HEALTH = 100
ENEMY_REWARD = 20

# Wave settings
WAVE_COOLDOWN = 10  # seconds between waves
ENEMIES_PER_WAVE_BASE = 5
ENEMIES_PER_WAVE_MULTIPLIER = 2  # Each wave has this many more enemies

# Path settings
PATH_WIDTH = 40
PATH_COLOR = GRAY

# Projectile settings
PROJECTILE_SPEED = 5.0
PROJECTILE_RADIUS = 5

# Debug settings
DEBUG = True
