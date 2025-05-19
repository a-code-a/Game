"""
Movement system for the Entity Component System.
"""
from src.systems.system import System
from src.utils.vector import Vector2


class MovementSystem(System):
    """System that updates the positions of entities based on their velocities."""
    
    def __init__(self):
        """Initialize a new MovementSystem."""
        super().__init__()
    
    def process(self, dt):
        """Update the positions of all entities with position and velocity components.
        
        Args:
            dt (float): The time delta since the last update in seconds.
        """
        for entity in self.entities:
            if not entity.active:
                continue
                
            position_component = entity.get_component("position")
            velocity_component = entity.get_component("velocity")
            
            if not position_component or not velocity_component:
                continue
            
            # Update position based on velocity
            position_component.position.x += velocity_component.velocity.x * dt
            position_component.position.y += velocity_component.velocity.y * dt
    
    def should_process(self, entity):
        """Check if this system should process the given entity.
        
        Args:
            entity (Entity): The entity to check.
            
        Returns:
            bool: True if the entity should be processed, False otherwise.
        """
        return (entity.active and
                entity.has_component("position") and
                entity.has_component("velocity"))
