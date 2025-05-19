"""
Base Projectile class for the Tower Defense Game
"""
import pygame
import math
from typing import List, Dict, Any, Tuple, Optional
import os

from utils import load_image, calculate_distance, calculate_angle, rotate_image

class Projectile:
    """Base class for all projectiles"""

    def __init__(self, x: float, y: float, target: Any, damage: float,
                 projectile_type: str = "basic_projectile", speed: float = 10.0,
                 splash_radius: float = 0):
        """
        Initialize a projectile

        Args:
            x: Starting x-coordinate
            y: Starting y-coordinate
            target: Target enemy
            damage: Damage amount
            projectile_type: Type of projectile
            speed: Movement speed
            splash_radius: Radius for splash damage (0 for single target)
        """
        self.x = x
        self.y = y
        self.target = target
        self.damage = damage
        self.projectile_type = projectile_type
        self.speed = speed
        self.splash_radius = splash_radius

        # Load projectile image
        self.image = load_image(os.path.join("projectiles", f"{projectile_type}.png"))
        self.rect = self.image.get_rect(center=(x, y))

        # Projectile state
        self.alive = True
        self.hit = False
        self.angle = 0

        # Calculate initial angle to target
        if target:
            self.angle = calculate_angle((x, y), (target.x, target.y))

    def update(self, dt: float, enemies: List[Any]) -> List[Any]:
        """
        Update the projectile position and state

        Args:
            dt: Time delta in seconds
            enemies: List of all enemies

        Returns:
            List of enemies hit by this projectile
        """
        if not self.alive:
            return []

        # If target is dead, projectile disappears
        if not self.target or not self.target.alive:
            self.alive = False
            return []

        # Calculate direction to target
        self.angle = calculate_angle((self.x, self.y), (self.target.x, self.target.y))

        # Move towards target
        move_distance = self.speed * dt * 60  # Scale by 60 to make speed consistent
        self.x += math.cos(self.angle) * move_distance
        self.y += math.sin(self.angle) * move_distance

        # Update rect position
        self.rect.center = (self.x, self.y)

        # Check for collision with target
        distance_to_target = calculate_distance((self.x, self.y), (self.target.x, self.target.y))
        if distance_to_target < 20:  # Hit radius
            self.hit = True
            self.alive = False

            # Handle splash damage
            hit_enemies = []
            if self.splash_radius > 0:
                for enemy in enemies:
                    if enemy.alive:
                        distance = calculate_distance((self.target.x, self.target.y), (enemy.x, enemy.y))
                        if distance <= self.splash_radius:
                            # Calculate damage falloff based on distance
                            damage_factor = 1.0 - (distance / self.splash_radius) * 0.5
                            enemy.take_damage(self.damage * damage_factor)
                            hit_enemies.append(enemy)
            else:
                # Single target damage
                self.target.take_damage(self.damage)
                hit_enemies.append(self.target)

            return hit_enemies

        return []

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the projectile on the surface

        Args:
            surface: Pygame surface to draw on
        """
        if not self.alive:
            return

        # Draw the projectile
        rotated_image, rotated_rect = rotate_image(self.image, math.degrees(-self.angle) - 90)
        rotated_rect.center = (self.x, self.y)
        surface.blit(rotated_image, rotated_rect)
