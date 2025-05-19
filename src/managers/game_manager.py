"""
Game Manager for the Tower Defense Game
"""
import pygame
import time
from typing import List, Dict, Any, Tuple, Optional

from constants import STARTING_COINS, STARTING_LIVES, TOWER_TYPES
from managers.wave_manager import WaveManager
from towers.tower import Tower
from projectiles.projectile import Projectile
from maps.map import Map

class GameManager:
    """Manages the game state and logic"""

    def __init__(self, current_map: Map):
        """
        Initialize the game manager

        Args:
            current_map: The current map
        """
        self.current_map = current_map
        self.wave_manager = WaveManager(current_map.get_path())

        # Game state
        self.coins = STARTING_COINS
        self.lives = STARTING_LIVES
        self.game_over = False
        self.game_won = False
        self.paused = False

        # Game objects
        self.towers = []
        self.projectiles = []

        # Selection state
        self.selected_tower = None
        self.selected_tower_type = None
        self.tower_placement_valid = False

        # Time tracking
        self.start_time = time.time()
        self.current_time = self.start_time
        self.last_update_time = self.start_time

    def update(self) -> None:
        """Update the game state"""
        if self.game_over or self.paused:
            return

        # Update time
        self.current_time = time.time()
        dt = self.current_time - self.last_update_time
        self.last_update_time = self.current_time

        # Update wave manager
        enemies, wave_complete = self.wave_manager.update(self.current_time, dt)

        # Check for enemies that reached the end
        for enemy in enemies:
            if enemy.reached_end:
                self.lives -= enemy.damage
                if self.lives <= 0:
                    self.game_over = True
                    return

        # Update towers
        for tower in self.towers:
            projectile_data = tower.update(self.current_time, enemies)
            if projectile_data:
                self.create_projectile(projectile_data)

        # Update projectiles
        for projectile in self.projectiles[:]:
            hit_enemies = projectile.update(dt, enemies)

            # Remove dead projectiles
            if not projectile.alive:
                self.projectiles.remove(projectile)

            # Award coins for killed enemies
            for enemy in hit_enemies:
                if not enemy.alive and not enemy.reached_end:
                    self.coins += enemy.reward

    def create_projectile(self, projectile_data: Dict[str, Any]) -> None:
        """
        Create a new projectile

        Args:
            projectile_data: Data for the projectile
        """
        projectile = Projectile(
            projectile_data['x'],
            projectile_data['y'],
            projectile_data['target'],
            projectile_data['damage'],
            f"{projectile_data['tower_type']}_projectile",
            splash_radius=projectile_data.get('splash_radius', 0)
        )
        self.projectiles.append(projectile)

    def place_tower(self, grid_pos: Tuple[int, int], tower_type: str) -> bool:
        """
        Place a tower at the specified grid position

        Args:
            grid_pos: Grid position (column, row)
            tower_type: Type of tower to place

        Returns:
            True if the tower was placed successfully, False otherwise
        """
        # Check if position is valid
        if not self.is_valid_tower_position(grid_pos):
            return False

        # Check if we have enough coins
        tower_cost = TOWER_TYPES[tower_type]['cost']
        if self.coins < tower_cost:
            return False

        # Convert grid position to pixel position
        pixel_pos = self.current_map.grid_to_pixel(grid_pos)

        # Create the tower
        tower = Tower(pixel_pos[0], pixel_pos[1], tower_type, TOWER_TYPES[tower_type])
        self.towers.append(tower)

        # Deduct the cost
        self.coins -= tower_cost

        return True

    def is_valid_tower_position(self, grid_pos: Tuple[int, int]) -> bool:
        """
        Check if a tower can be placed at the specified grid position

        Args:
            grid_pos: Grid position (column, row)

        Returns:
            True if the position is valid, False otherwise
        """
        # Check if the position is buildable
        if not self.current_map.is_buildable(*grid_pos):
            return False

        # Check if there's already a tower at this position
        pixel_pos = self.current_map.grid_to_pixel(grid_pos)
        for tower in self.towers:
            if (tower.x, tower.y) == pixel_pos:
                return False

        return True

    def select_tower(self, pixel_pos: Tuple[int, int]) -> Optional[Tower]:
        """
        Select a tower at the specified pixel position

        Args:
            pixel_pos: Pixel position (x, y)

        Returns:
            The selected tower, or None if no tower was selected
        """
        # Deselect current tower
        if self.selected_tower:
            self.selected_tower.selected = False

        # Find tower at position
        closest_tower = None
        closest_distance = 40  # Selection radius

        for tower in self.towers:
            distance = ((tower.x - pixel_pos[0]) ** 2 + (tower.y - pixel_pos[1]) ** 2) ** 0.5
            if distance < closest_distance:
                closest_tower = tower
                closest_distance = distance

        # Select the tower
        self.selected_tower = closest_tower
        if closest_tower:
            closest_tower.selected = True

        return closest_tower

    def upgrade_selected_tower(self, path: str) -> bool:
        """
        Upgrade the selected tower along the specified path

        Args:
            path: Upgrade path ('path1' or 'path2')

        Returns:
            True if the upgrade was successful, False otherwise
        """
        if not self.selected_tower:
            return False

        # Get upgrade cost
        upgrade_cost = self.selected_tower.get_upgrade_cost(path)
        if upgrade_cost == 0:  # No more upgrades available
            return False

        # Check if we have enough coins
        if self.coins < upgrade_cost:
            return False

        # Perform the upgrade
        success = self.selected_tower.upgrade(path)
        if success:
            self.coins -= upgrade_cost

        return success

    def sell_selected_tower(self) -> int:
        """
        Sell the selected tower

        Returns:
            Amount of coins refunded, or 0 if no tower was selected
        """
        if not self.selected_tower:
            return 0

        # Calculate refund (50% of cost)
        refund = self.selected_tower.cost // 2

        # Remove the tower
        self.towers.remove(self.selected_tower)
        self.selected_tower = None

        # Add coins
        self.coins += refund

        return refund

    def start_wave(self) -> bool:
        """
        Start the next wave

        Returns:
            True if the wave was started, False otherwise
        """
        if self.wave_manager.can_start_next_wave(self.current_time):
            self.wave_manager.start_wave()
            return True
        return False

    def toggle_pause(self) -> None:
        """Toggle the game pause state"""
        self.paused = not self.paused

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the game state

        Args:
            surface: Pygame surface to draw on
        """
        # Draw map
        self.current_map.draw(surface)

        # Draw towers
        for tower in self.towers:
            tower.draw(surface)

        # Draw enemies
        for enemy in self.wave_manager.enemies:
            enemy.draw(surface)

        # Draw projectiles
        for projectile in self.projectiles:
            projectile.draw(surface)

    def get_game_state(self) -> Dict[str, Any]:
        """
        Get the current game state

        Returns:
            Dictionary with game state information
        """
        return {
            'coins': self.coins,
            'lives': self.lives,
            'wave': self.wave_manager.current_wave,
            'wave_in_progress': self.wave_manager.wave_in_progress,
            'enemies_remaining': len(self.wave_manager.enemies) + len(self.wave_manager.enemies_to_spawn),
            'cooldown_remaining': self.wave_manager.get_cooldown_remaining(self.current_time),
            'selected_tower': self.selected_tower,
            'game_over': self.game_over,
            'game_won': self.game_won,
            'paused': self.paused
        }
