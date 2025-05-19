"""
Base Enemy class for the Tower Defense Game
"""
import pygame
import math
from typing import List, Dict, Any, Tuple, Optional
import os

from utils import load_image, calculate_distance, calculate_angle, rotate_image

class Enemy:
    """Base class for all enemies"""

    def __init__(self, path: List[Tuple[int, int]], enemy_type: str, enemy_data: Dict[str, Any]):
        """
        Initialize an enemy

        Args:
            path: List of waypoints (x, y) for the enemy to follow
            enemy_type: Type of enemy (e.g., 'basic_minion', 'fast_minion')
            enemy_data: Enemy configuration data
        """
        self.path = path
        self.enemy_type = enemy_type

        # Set enemy properties from enemy_data
        self.max_health = enemy_data['health']
        self.health = self.max_health
        self.speed = enemy_data['speed']
        self.reward = enemy_data['reward']
        self.damage = enemy_data['damage']

        # Initialize position at the start of the path
        self.path_index = 0
        self.x, self.y = path[0]
        self.target_x, self.target_y = path[1]

        # Load enemy image
        self.image = load_image(os.path.join("enemies", f"{enemy_type}.png"))
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Enemy state
        self.alive = True
        self.reached_end = False
        self.angle = 0
        self.burning = False
        self.burning_damage = 0
        self.burning_duration = 0
        self.slowed = False
        self.slow_factor = 1.0
        self.slow_duration = 0

    def update(self, dt: float) -> bool:
        """
        Update the enemy position and state

        Args:
            dt: Time delta in seconds

        Returns:
            True if the enemy reached the end of the path, False otherwise
        """
        if not self.alive:
            return False

        # Apply status effects
        self.update_status_effects(dt)

        # Calculate direction to the next waypoint
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        # Calculate movement for this frame
        actual_speed = self.speed * self.slow_factor
        move_distance = actual_speed * dt * 60  # Scale by 60 to make speed consistent regardless of framerate

        # If we would reach or pass the waypoint, move to it and target the next one
        if distance <= move_distance:
            self.x = self.target_x
            self.y = self.target_y
            self.path_index += 1

            # If we reached the end of the path
            if self.path_index >= len(self.path):
                self.reached_end = True
                self.alive = False
                return True

            # Set the next target
            self.target_x, self.target_y = self.path[self.path_index]
        else:
            # Move towards the waypoint
            self.x += (dx / distance) * move_distance
            self.y += (dy / distance) * move_distance

        # Update the angle for rotation
        self.angle = math.atan2(dy, dx)

        # Update the rect position
        self.rect.center = (self.x, self.y)

        return False

    def update_status_effects(self, dt: float) -> None:
        """
        Update status effects like burning or slowing

        Args:
            dt: Time delta in seconds
        """
        # Update burning effect
        if self.burning:
            self.health -= self.burning_damage * dt
            self.burning_duration -= dt
            if self.burning_duration <= 0:
                self.burning = False

        # Update slow effect
        if self.slowed:
            self.slow_duration -= dt
            if self.slow_duration <= 0:
                self.slowed = False
                self.slow_factor = 1.0

        # Check if enemy died from status effects
        if self.health <= 0:
            self.alive = False

    def take_damage(self, damage: float) -> bool:
        """
        Apply damage to the enemy

        Args:
            damage: Amount of damage to apply

        Returns:
            True if the enemy died, False otherwise
        """
        self.health -= damage
        if self.health <= 0:
            self.alive = False
            return True
        return False

    def apply_burning(self, damage: float, duration: float) -> None:
        """
        Apply a burning effect to the enemy

        Args:
            damage: Damage per second
            duration: Duration in seconds
        """
        # If already burning, take the higher damage and reset duration
        if self.burning:
            self.burning_damage = max(self.burning_damage, damage)
            self.burning_duration = max(self.burning_duration, duration)
        else:
            self.burning = True
            self.burning_damage = damage
            self.burning_duration = duration

    def apply_slow(self, slow_factor: float, duration: float) -> None:
        """
        Apply a slowing effect to the enemy

        Args:
            slow_factor: Factor to multiply speed by (0.5 = half speed)
            duration: Duration in seconds
        """
        # If already slowed, take the lower factor and reset duration
        if self.slowed:
            self.slow_factor = min(self.slow_factor, slow_factor)
            self.slow_duration = max(self.slow_duration, duration)
        else:
            self.slowed = True
            self.slow_factor = slow_factor
            self.slow_duration = duration

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the enemy on the surface

        Args:
            surface: Pygame surface to draw on
        """
        # Draw the enemy
        rotated_image, rotated_rect = rotate_image(self.image, math.degrees(-self.angle) - 90)
        rotated_rect.center = (self.x, self.y)
        surface.blit(rotated_image, rotated_rect)

        # Draw health bar
        health_bar_width = 40
        health_bar_height = 5
        health_ratio = max(0, self.health / self.max_health)

        # Background (red)
        pygame.draw.rect(surface, (255, 0, 0),
                         (self.x - health_bar_width // 2,
                          self.y - 30,
                          health_bar_width,
                          health_bar_height))

        # Foreground (green)
        pygame.draw.rect(surface, (0, 255, 0),
                         (self.x - health_bar_width // 2,
                          self.y - 30,
                          int(health_bar_width * health_ratio),
                          health_bar_height))

        # Draw status effect indicators
        if self.burning:
            pygame.draw.circle(surface, (255, 100, 0), (self.x + 15, self.y - 25), 4)

        if self.slowed:
            pygame.draw.circle(surface, (0, 200, 255), (self.x + 25, self.y - 25), 4)
