"""
Base component class for the Entity Component System.
"""


class Component:
    """Base class for all components in the Entity Component System.
    
    Components are data containers that can be attached to entities.
    They should not contain any game logic, only data.
    """
    
    def __init__(self):
        """Initialize a new Component object."""
        self.entity = None
    
    def attach(self, entity):
        """Attach this component to an entity.
        
        Args:
            entity (Entity): The entity to attach this component to.
        """
        self.entity = entity
