"""
Health component for the Entity Component System.
"""
from src.components.component import Component


class HealthComponent(Component):
    """Component that stores the health of an entity."""
    
    def __init__(self, max_health=100):
        """Initialize a new HealthComponent.
        
        Args:
            max_health (float): The maximum health of the entity.
        """
        super().__init__()
        self.max_health = max_health
        self.current_health = max_health
    
    def take_damage(self, amount):
        """Reduce the entity's health by the given amount.
        
        Args:
            amount (float): The amount of damage to take.
            
        Returns:
            bool: True if the entity is still alive, False if it died.
        """
        self.current_health -= amount
        return self.is_alive()
    
    def heal(self, amount):
        """Increase the entity's health by the given amount.
        
        Args:
            amount (float): The amount of health to restore.
        """
        self.current_health = min(self.current_health + amount, self.max_health)
    
    def is_alive(self):
        """Check if the entity is still alive.
        
        Returns:
            bool: True if the entity is alive, False if it's dead.
        """
        return self.current_health > 0
