"""
Entity manager for managing all entities in the game.
"""


class EntityManager:
    """Manager for all entities in the game."""
    
    def __init__(self):
        """Initialize a new EntityManager."""
        self.entities = []
        self.entities_to_add = []
        self.entities_to_remove = []
        self.systems = []
    
    def add_entity(self, entity):
        """Add an entity to the game.
        
        Args:
            entity: The entity to add.
        """
        self.entities_to_add.append(entity)
    
    def remove_entity(self, entity):
        """Remove an entity from the game.
        
        Args:
            entity: The entity to remove.
        """
        self.entities_to_remove.append(entity)
    
    def add_system(self, system):
        """Add a system to the game.
        
        Args:
            system: The system to add.
        """
        self.systems.append(system)
    
    def update(self, dt):
        """Update all systems and process entity changes.
        
        Args:
            dt (float): The time delta since the last update in seconds.
        """
        # Process entity additions
        for entity in self.entities_to_add:
            if entity not in self.entities:
                self.entities.append(entity)
                
                # Add the entity to all systems that should process it
                for system in self.systems:
                    if hasattr(system, "should_process") and system.should_process(entity):
                        system.add_entity(entity)
        
        # Clear the list of entities to add
        self.entities_to_add = []
        
        # Process entity removals
        for entity in self.entities_to_remove:
            if entity in self.entities:
                self.entities.remove(entity)
                
                # Remove the entity from all systems
                for system in self.systems:
                    system.remove_entity(entity)
        
        # Clear the list of entities to remove
        self.entities_to_remove = []
        
        # Update all systems
        for system in self.systems:
            system.process(dt)
    
    def get_entities_with_tag(self, tag):
        """Get all entities with the given tag.
        
        Args:
            tag (str): The tag to filter by.
            
        Returns:
            list: A list of entities with the given tag.
        """
        return [entity for entity in self.entities if entity.has_tag(tag)]
    
    def get_entities_with_component(self, component_type):
        """Get all entities with the given component type.
        
        Args:
            component_type (str): The component type to filter by.
            
        Returns:
            list: A list of entities with the given component type.
        """
        return [entity for entity in self.entities if entity.has_component(component_type)]
