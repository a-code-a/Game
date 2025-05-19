"""
Wave manager for spawning enemies in waves.
"""
import time
import random
from src.entities.enemy import Enemy
from src.utils.vector import Vector2
from src.config import WAVE_COOLDOWN, ENEMIES_PER_WAVE_BASE, ENEMIES_PER_WAVE_MULTIPLIER


class WaveManager:
    """Manager for spawning enemies in waves."""
    
    def __init__(self, entity_manager):
        """Initialize a new WaveManager.
        
        Args:
            entity_manager: The entity manager to use for creating enemies.
        """
        self.entity_manager = entity_manager
        self.current_wave = 0
        self.enemies_remaining = 0
        self.spawn_timer = 0
        self.wave_timer = 0
        self.last_wave_time = 0
        self.spawn_interval = 1.0  # seconds between enemy spawns
        self.path = []
        self.active = False
    
    def set_path(self, path):
        """Set the path for enemies to follow.
        
        Args:
            path (list): A list of Vector2 points defining the path.
        """
        self.path = path
    
    def start(self):
        """Start the wave manager."""
        self.active = True
        self.last_wave_time = time.time() - WAVE_COOLDOWN  # Start first wave immediately
    
    def stop(self):
        """Stop the wave manager."""
        self.active = False
    
    def update(self):
        """Update the wave manager, spawning enemies as needed."""
        if not self.active or not self.path:
            return
        
        current_time = time.time()
        
        # Check if it's time for a new wave
        if self.enemies_remaining <= 0 and current_time - self.last_wave_time >= WAVE_COOLDOWN:
            self.start_next_wave()
        
        # Spawn enemies if needed
        if self.enemies_remaining > 0 and current_time - self.spawn_timer >= self.spawn_interval:
            self.spawn_enemy()
            self.spawn_timer = current_time
    
    def start_next_wave(self):
        """Start the next wave of enemies."""
        self.current_wave += 1
        self.enemies_remaining = ENEMIES_PER_WAVE_BASE + (self.current_wave - 1) * ENEMIES_PER_WAVE_MULTIPLIER
        self.last_wave_time = time.time()
        self.spawn_timer = time.time()
        
        # Decrease spawn interval for higher waves (more difficult)
        self.spawn_interval = max(0.5, 1.0 - (self.current_wave - 1) * 0.05)
        
        print(f"Wave {self.current_wave} started! Enemies: {self.enemies_remaining}")
    
    def spawn_enemy(self):
        """Spawn a single enemy at the start of the path."""
        if not self.path:
            return
        
        # Create an enemy at the start of the path
        start_pos = self.path[0]
        enemy = Enemy(start_pos.x, start_pos.y, self.path)
        
        # Add the enemy to the entity manager
        self.entity_manager.add_entity(enemy)
        
        # Decrease the number of enemies remaining
        self.enemies_remaining -= 1
    
    def get_current_wave(self):
        """Get the current wave number.
        
        Returns:
            int: The current wave number.
        """
        return self.current_wave
    
    def get_enemies_remaining(self):
        """Get the number of enemies remaining in the current wave.
        
        Returns:
            int: The number of enemies remaining.
        """
        return self.enemies_remaining
    
    def get_next_wave_time(self):
        """Get the time until the next wave starts.
        
        Returns:
            float: The time in seconds until the next wave starts.
        """
        if self.enemies_remaining > 0:
            return 0
        
        time_elapsed = time.time() - self.last_wave_time
        return max(0, WAVE_COOLDOWN - time_elapsed)
