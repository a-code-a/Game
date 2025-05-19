"""
Base entity class for the Entity Component System.
"""
import uuid


class Entity:
    """Base class for all entities in the Entity Component System.
    
    Entities are containers for components. They have no behavior of their own.
    """
    
    def __init__(self, entity_id=None):
        """Initialize a new Entity object.
        
        Args:
            entity_id (str, optional): A unique ID for this entity. If not provided,
                a random UUID will be generated.
        """
        self.id = entity_id or str(uuid.uuid4())
        self.components = {}
        self.tags = set()
        self.active = True
    
    def add_component(self, component_type, component):
        """Add a component to this entity.
        
        Args:
            component_type (str): The type of the component.
            component (Component): The component to add.
        """
        component.attach(self)
        self.components[component_type] = component
    
    def remove_component(self, component_type):
        """Remove a component from this entity.
        
        Args:
            component_type (str): The type of the component to remove.
            
        Returns:
            Component: The removed component, or None if the component was not found.
        """
        return self.components.pop(component_type, None)
    
    def get_component(self, component_type):
        """Get a component from this entity.
        
        Args:
            component_type (str): The type of the component to get.
            
        Returns:
            Component: The component, or None if the component was not found.
        """
        return self.components.get(component_type)
    
    def has_component(self, component_type):
        """Check if this entity has a component of the given type.
        
        Args:
            component_type (str): The type of the component to check for.
            
        Returns:
            bool: True if the entity has the component, False otherwise.
        """
        return component_type in self.components
    
    def add_tag(self, tag):
        """Add a tag to this entity.
        
        Args:
            tag (str): The tag to add.
        """
        self.tags.add(tag)
    
    def remove_tag(self, tag):
        """Remove a tag from this entity.
        
        Args:
            tag (str): The tag to remove.
        """
        self.tags.discard(tag)
    
    def has_tag(self, tag):
        """Check if this entity has the given tag.
        
        Args:
            tag (str): The tag to check for.
            
        Returns:
            bool: True if the entity has the tag, False otherwise.
        """
        return tag in self.tags
