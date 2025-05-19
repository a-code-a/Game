"""
Base system class for the Entity Component System.
"""


class System:
    """Base class for all systems in the Entity Component System.
    
    Systems contain the game logic that operates on entities with specific components.
    """
    
    def __init__(self):
        """Initialize a new System object."""
        self.entities = []
    
    def add_entity(self, entity):
        """Add an entity to this system.
        
        Args:
            entity (Entity): The entity to add.
            
        Returns:
            bool: True if the entity was added, False if it was already in the system.
        """
        if entity not in self.entities:
            self.entities.append(entity)
            return True
        return False
    
    def remove_entity(self, entity):
        """Remove an entity from this system.
        
        Args:
            entity (Entity): The entity to remove.
            
        Returns:
            bool: True if the entity was removed, False if it was not in the system.
        """
        if entity in self.entities:
            self.entities.remove(entity)
            return True
        return False
    
    def process(self, dt):
        """Process all entities in this system.
        
        This method should be overridden by subclasses.
        
        Args:
            dt (float): The time delta since the last update in seconds.
        """
        pass
