"""
Path following system for the Entity Component System.
"""
from src.systems.system import System
from src.utils.vector import Vector2


class PathFollowingSystem(System):
    """System that makes entities follow paths."""
    
    def __init__(self):
        """Initialize a new PathFollowingSystem."""
        super().__init__()
        self.waypoint_threshold = 10  # Distance at which a waypoint is considered reached
    
    def process(self, dt):
        """Update the velocities of entities to follow their paths.
        
        Args:
            dt (float): The time delta since the last update in seconds.
        """
        for entity in self.entities:
            if not entity.active:
                continue
                
            position_component = entity.get_component("position")
            velocity_component = entity.get_component("velocity")
            path_following_component = entity.get_component("path_following")
            
            if not position_component or not velocity_component or not path_following_component:
                continue
            
            # Skip if the entity has reached the end of the path
            if path_following_component.has_reached_end():
                velocity_component.set_velocity(0, 0)
                continue
            
            # Get the current waypoint
            current_waypoint = path_following_component.get_current_waypoint()
            if not current_waypoint:
                velocity_component.set_velocity(0, 0)
                continue
            
            # Calculate direction to the waypoint
            current_pos = position_component.position
            direction = current_waypoint - current_pos
            distance = direction.length()
            
            # Check if we've reached the waypoint
            if distance < self.waypoint_threshold:
                # Move to the next waypoint
                if not path_following_component.advance_to_next_waypoint():
                    # End of path reached
                    velocity_component.set_velocity(0, 0)
                    continue
                
                # Get the new waypoint
                current_waypoint = path_following_component.get_current_waypoint()
                if not current_waypoint:
                    velocity_component.set_velocity(0, 0)
                    continue
                
                # Recalculate direction
                direction = current_waypoint - current_pos
                distance = direction.length()
            
            # Normalize direction and set velocity
            if distance > 0:
                direction = direction / distance
                speed = path_following_component.speed
                velocity_component.set_velocity(
                    direction.x * speed,
                    direction.y * speed
                )
    
    def should_process(self, entity):
        """Check if this system should process the given entity.
        
        Args:
            entity (Entity): The entity to check.
            
        Returns:
            bool: True if the entity should be processed, False otherwise.
        """
        return (entity.active and
                entity.has_component("position") and
                entity.has_component("velocity") and
                entity.has_component("path_following"))
