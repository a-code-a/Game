"""
Position component for the Entity Component System.
"""
from src.components.component import Component
from src.utils.vector import Vector2


class PositionComponent(Component):
    """Component that stores the position, rotation, and scale of an entity."""
    
    def __init__(self, x=0, y=0, rotation=0, scale=1):
        """Initialize a new PositionComponent.
        
        Args:
            x (float): The x-coordinate of the entity.
            y (float): The y-coordinate of the entity.
            rotation (float): The rotation of the entity in degrees.
            scale (float): The scale of the entity.
        """
        super().__init__()
        self.position = Vector2(x, y)
        self.rotation = rotation
        self.scale = scale
