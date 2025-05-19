"""
Path following component for the Entity Component System.
"""
from src.components.component import Component
from src.utils.vector import Vector2


class PathFollowingComponent(Component):
    """Component that allows an entity to follow a path."""
    
    def __init__(self, path=None, speed=1.0):
        """Initialize a new PathFollowingComponent.
        
        Args:
            path (list): A list of Vector2 points defining the path.
            speed (float): The movement speed along the path.
        """
        super().__init__()
        self.path = path or []
        self.speed = speed
        self.current_waypoint_index = 0
        self.reached_end = False
    
    def set_path(self, path):
        """Set a new path for the entity to follow.
        
        Args:
            path (list): A list of Vector2 points defining the path.
        """
        self.path = path
        self.current_waypoint_index = 0
        self.reached_end = False
    
    def get_current_waypoint(self):
        """Get the current waypoint the entity is moving towards.
        
        Returns:
            Vector2: The current waypoint, or None if the path is empty.
        """
        if not self.path or self.current_waypoint_index >= len(self.path):
            return None
        return self.path[self.current_waypoint_index]
    
    def advance_to_next_waypoint(self):
        """Advance to the next waypoint in the path.
        
        Returns:
            bool: True if there are more waypoints, False if the end was reached.
        """
        self.current_waypoint_index += 1
        if self.current_waypoint_index >= len(self.path):
            self.reached_end = True
            return False
        return True
    
    def has_reached_end(self):
        """Check if the entity has reached the end of the path.
        
        Returns:
            bool: True if the entity has reached the end of the path.
        """
        return self.reached_end
