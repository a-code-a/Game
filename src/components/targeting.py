"""
Targeting component for the Entity Component System.
"""
import time
from src.components.component import Component


class TargetingComponent(Component):
    """Component that stores targeting information for towers."""
    
    def __init__(self, range=150, damage=10, cooldown=1.0):
        """Initialize a new TargetingComponent.
        
        Args:
            range (float): The range of the tower in pixels.
            damage (float): The damage dealt by the tower.
            cooldown (float): The cooldown between attacks in seconds.
        """
        super().__init__()
        self.range = range
        self.damage = damage
        self.cooldown = cooldown
        self.last_attack_time = 0
        self.current_target = None
    
    def can_attack(self):
        """Check if the tower can attack (cooldown has expired).
        
        Returns:
            bool: True if the tower can attack, False otherwise.
        """
        return time.time() - self.last_attack_time >= self.cooldown
    
    def attack(self):
        """Register an attack, updating the last attack time.
        
        Returns:
            float: The current time when the attack occurred.
        """
        self.last_attack_time = time.time()
        return self.last_attack_time
