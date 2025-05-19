"""
Velocity component for the Entity Component System.
"""
from src.components.component import Component
from src.utils.vector import Vector2


class VelocityComponent(Component):
    """Component that stores the velocity of an entity."""
    
    def __init__(self, x=0, y=0, max_speed=None):
        """Initialize a new VelocityComponent.
        
        Args:
            x (float): The x-component of the velocity.
            y (float): The y-component of the velocity.
            max_speed (float, optional): The maximum speed of the entity.
        """
        super().__init__()
        self.velocity = Vector2(x, y)
        self.max_speed = max_speed
    
    def set_velocity(self, x, y):
        """Set the velocity of the entity.
        
        Args:
            x (float): The x-component of the velocity.
            y (float): The y-component of the velocity.
        """
        self.velocity.x = x
        self.velocity.y = y
        
        # Clamp to max speed if needed
        if self.max_speed is not None:
            speed = self.velocity.length()
            if speed > self.max_speed:
                self.velocity = self.velocity.normalize() * self.max_speed
