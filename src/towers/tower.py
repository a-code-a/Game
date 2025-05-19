"""
Base Tower class for the Tower Defense Game
"""
import pygame
import math
import random
from typing import List, Dict, Any, Tuple, Optional
import os

from utils import load_image, calculate_distance, calculate_angle, rotate_image

class Tower:
    """Base class for all towers"""

    def __init__(self, x: int, y: int, tower_type: str, tower_data: Dict[str, Any]):
        """
        Initialize a tower

        Args:
            x: X coordinate in pixels
            y: Y coordinate in pixels
            tower_type: Type of tower (e.g., 'basic', 'sniper')
            tower_data: Tower configuration data
        """
        self.x = x
        self.y = y
        self.tower_type = tower_type

        # Set tower properties from tower_data
        self.cost = tower_data['cost']
        self.damage = tower_data['damage']
        self.range = tower_data['range']
        self.cooldown = tower_data['cooldown']

        # Initialize upgrade paths
        self.upgrade_paths = tower_data.get('upgrade_paths', {})
        self.upgrades = {'path1': 0, 'path2': 0}

        # Load tower image
        self.image = load_image(os.path.join("towers", f"{tower_type}.png"))
        self.rect = self.image.get_rect(center=(x, y))

        # Tower state
        self.target = None
        self.last_shot_time = 0
        self.angle = 0
        self.selected = False

        # Special properties
        self.splash_radius = tower_data.get('splash_radius', 0)
        self.buff_multiplier = tower_data.get('buff_multiplier', 1.0)

        # Advanced properties for upgrades
        self.adds_burning = False
        self.burning_damage_multiplier = 1.0
        self.adds_critical = False
        self.critical_chance = 0.1  # 10% chance by default if critical hits are enabled
        self.adds_special_ability = False

    def update(self, current_time: float, enemies: List[Any]) -> Optional[Dict[str, Any]]:
        """
        Update the tower state

        Args:
            current_time: Current game time in seconds
            enemies: List of enemy objects

        Returns:
            Dictionary with projectile data if a shot is fired, None otherwise
        """
        # Find a target if we don't have one or if the current target is out of range/dead
        if not self.target or not self.target.alive or calculate_distance(
                (self.x, self.y), (self.target.x, self.target.y)) > self.range:
            self.find_target(enemies)

        # If we have a target, rotate towards it and shoot if cooldown has passed
        if self.target and self.target.alive:
            # Calculate angle to target
            self.angle = calculate_angle((self.x, self.y), (self.target.x, self.target.y))
            angle_degrees = math.degrees(-self.angle) - 90  # Adjust for image orientation

            # Check if cooldown has passed
            if current_time - self.last_shot_time >= self.cooldown:
                self.last_shot_time = current_time
                return self.shoot()

        return None

    def find_target(self, enemies: List[Any]) -> None:
        """
        Find the closest enemy in range

        Args:
            enemies: List of enemy objects
        """
        closest_enemy = None
        closest_distance = float('inf')

        for enemy in enemies:
            if enemy.alive:
                distance = calculate_distance((self.x, self.y), (enemy.x, enemy.y))
                if distance <= self.range and distance < closest_distance:
                    closest_enemy = enemy
                    closest_distance = distance

        self.target = closest_enemy

    def shoot(self) -> Dict[str, Any]:
        """
        Create a projectile

        Returns:
            Dictionary with projectile data
        """
        # Calculate actual damage (apply critical hit if applicable)
        actual_damage = self.damage
        is_critical = False

        if self.adds_critical and random.random() < self.critical_chance:
            actual_damage *= 2  # Double damage for critical hits
            is_critical = True

        return {
            'x': self.x,
            'y': self.y,
            'target': self.target,
            'damage': actual_damage,
            'tower_type': self.tower_type,
            'splash_radius': self.splash_radius,
            'adds_burning': self.adds_burning,
            'burning_damage_multiplier': self.burning_damage_multiplier,
            'is_critical': is_critical
        }

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the tower on the surface

        Args:
            surface: Pygame surface to draw on
        """
        # Draw range circle if selected
        if self.selected:
            transparent_surface = pygame.Surface((self.range * 2, self.range * 2), pygame.SRCALPHA)
            pygame.draw.circle(transparent_surface, (0, 255, 0, 64), (self.range, self.range), self.range)
            surface.blit(transparent_surface, (self.x - self.range, self.y - self.range))

        # Draw the tower
        rotated_image, rotated_rect = rotate_image(self.image, math.degrees(-self.angle) - 90)
        rotated_rect.center = (self.x, self.y)
        surface.blit(rotated_image, rotated_rect)

    def upgrade(self, path: str) -> bool:
        """
        Upgrade the tower along the specified path

        Args:
            path: Upgrade path ('path1' or 'path2')

        Returns:
            True if upgrade was successful, False otherwise
        """
        if path not in self.upgrade_paths:
            return False

        current_level = self.upgrades[path]

        # Check if we can upgrade further on this path
        if current_level >= len(self.upgrade_paths[path]):
            return False

        # Get the upgrade data
        upgrade_data = self.upgrade_paths[path][current_level]

        # Apply the upgrade effects
        if 'damage_multiplier' in upgrade_data:
            self.damage *= upgrade_data['damage_multiplier']
        if 'range_multiplier' in upgrade_data:
            self.range *= upgrade_data['range_multiplier']
        if 'cooldown_multiplier' in upgrade_data:
            self.cooldown *= upgrade_data['cooldown_multiplier']
        if 'splash_radius_multiplier' in upgrade_data:
            self.splash_radius *= upgrade_data['splash_radius_multiplier']
        if 'buff_multiplier' in upgrade_data:
            self.buff_multiplier = upgrade_data['buff_multiplier']

        # Special abilities
        if 'adds_burning' in upgrade_data:
            self.adds_burning = upgrade_data['adds_burning']
        if 'burning_damage_multiplier' in upgrade_data:
            self.burning_damage_multiplier *= upgrade_data['burning_damage_multiplier']
        if 'adds_critical' in upgrade_data:
            self.adds_critical = upgrade_data['adds_critical']
        if 'critical_chance' in upgrade_data:
            self.critical_chance = upgrade_data['critical_chance']
        if 'adds_special_ability' in upgrade_data:
            self.adds_special_ability = upgrade_data['adds_special_ability']

        # Increment the upgrade level for this path
        self.upgrades[path] += 1

        # If we upgraded one path to level 3, lock the other path
        if self.upgrades[path] == 3:
            other_path = 'path2' if path == 'path1' else 'path1'
            if self.upgrades[other_path] == 0:
                # Lock the other path by removing it
                self.upgrade_paths.pop(other_path, None)

        return True

    def get_upgrade_cost(self, path: str) -> int:
        """
        Get the cost of the next upgrade on the specified path

        Args:
            path: Upgrade path ('path1' or 'path2')

        Returns:
            Cost of the upgrade, or 0 if no more upgrades are available
        """
        if path not in self.upgrade_paths:
            return 0

        current_level = self.upgrades[path]

        # Check if we can upgrade further on this path
        if current_level >= len(self.upgrade_paths[path]):
            return 0

        # Return the cost of the next upgrade
        return self.upgrade_paths[path][current_level]['cost']

    def get_upgrade_info(self, path: str) -> Dict[str, Any]:
        """
        Get information about the next upgrade on the specified path

        Args:
            path: Upgrade path ('path1' or 'path2')

        Returns:
            Dictionary with upgrade information, or empty dict if no more upgrades
        """
        if path not in self.upgrade_paths:
            return {}

        current_level = self.upgrades[path]

        # Check if we can upgrade further on this path
        if current_level >= len(self.upgrade_paths[path]):
            return {}

        # Return the upgrade data
        return self.upgrade_paths[path][current_level]
