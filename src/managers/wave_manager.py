"""
Wave Manager for the Tower Defense Game
"""
import pygame
import random
from typing import List, Dict, Any, Tuple, Optional
import time

from constants import ENEMY_TYPES, WAVE_COOLDOWN
from enemies.enemy import Enemy

class WaveManager:
    """Manages enemy waves and spawning"""

    def __init__(self, path: List[Tuple[int, int]]):
        """
        Initialize the wave manager

        Args:
            path: Path for enemies to follow
        """
        self.path = path
        self.current_wave = 0
        self.enemies = []
        self.wave_in_progress = False
        self.wave_start_time = 0
        self.next_spawn_time = 0
        self.spawn_interval = 1.0  # Time between enemy spawns
        self.enemies_to_spawn = []  # Queue of enemies to spawn
        self.wave_cooldown = WAVE_COOLDOWN
        self.wave_cooldown_start = 0

    def start_wave(self) -> None:
        """Start the next wave"""
        if self.wave_in_progress:
            return

        self.current_wave += 1
        self.wave_in_progress = True
        self.wave_start_time = time.time()
        self.next_spawn_time = self.wave_start_time

        # Generate enemies for this wave
        self.generate_wave()

    def generate_wave(self) -> None:
        """Generate the enemies for the current wave"""
        self.enemies_to_spawn = []

        # Basic wave scaling formula
        num_basic = 5 + self.current_wave * 2
        num_fast = max(0, self.current_wave - 2) * 2
        num_tank = max(0, self.current_wave - 4)
        has_boss = self.current_wave % 5 == 0 and self.current_wave > 0

        # Add basic minions
        for _ in range(num_basic):
            self.enemies_to_spawn.append('basic_minion')

        # Add fast minions
        for _ in range(num_fast):
            self.enemies_to_spawn.append('fast_minion')

        # Add tank minions
        for _ in range(num_tank):
            self.enemies_to_spawn.append('tank_minion')

        # Add boss if it's a boss wave
        if has_boss:
            self.enemies_to_spawn.append('boss_minion')

        # Shuffle the enemies for variety
        random.shuffle(self.enemies_to_spawn)

        # Adjust spawn interval based on wave number (faster spawns in later waves)
        self.spawn_interval = max(0.5, 1.0 - (self.current_wave * 0.05))

    def update(self, current_time: float, dt: float) -> Tuple[List[Enemy], bool]:
        """
        Update the wave manager

        Args:
            current_time: Current game time in seconds
            dt: Time delta in seconds

        Returns:
            Tuple of (list of active enemies, whether wave is complete)
        """
        # Update existing enemies
        for enemy in self.enemies[:]:
            # Call the enemy's update method to move it
            enemy.update(dt)

            # Remove dead enemies
            if not enemy.alive:
                self.enemies.remove(enemy)

        # Spawn new enemies if wave is in progress
        if self.wave_in_progress and self.enemies_to_spawn:
            if current_time >= self.next_spawn_time:
                enemy_type = self.enemies_to_spawn.pop(0)
                enemy = Enemy(self.path, enemy_type, ENEMY_TYPES[enemy_type])
                self.enemies.append(enemy)
                self.next_spawn_time = current_time + self.spawn_interval

        # Check if wave is complete
        wave_complete = False
        if self.wave_in_progress and not self.enemies_to_spawn and not self.enemies:
            self.wave_in_progress = False
            self.wave_cooldown_start = current_time
            wave_complete = True

        return self.enemies, wave_complete

    def can_start_next_wave(self, current_time: float) -> bool:
        """
        Check if the next wave can be started

        Args:
            current_time: Current game time in seconds

        Returns:
            True if the next wave can be started, False otherwise
        """
        if self.wave_in_progress:
            return False

        # Check if cooldown has passed
        return current_time - self.wave_cooldown_start >= self.wave_cooldown

    def get_cooldown_remaining(self, current_time: float) -> float:
        """
        Get the remaining cooldown time before the next wave

        Args:
            current_time: Current game time in seconds

        Returns:
            Remaining cooldown time in seconds
        """
        if self.wave_in_progress:
            return 0

        return max(0, self.wave_cooldown - (current_time - self.wave_cooldown_start))

    def get_wave_info(self) -> Dict[str, Any]:
        """
        Get information about the current wave

        Returns:
            Dictionary with wave information
        """
        return {
            'current_wave': self.current_wave,
            'wave_in_progress': self.wave_in_progress,
            'enemies_remaining': len(self.enemies) + len(self.enemies_to_spawn)
        }
