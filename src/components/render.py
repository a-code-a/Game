"""
Render component for the Entity Component System.
"""
import pygame
from src.components.component import Component


class RenderComponent(Component):
    """Component that stores rendering information for an entity."""
    
    def __init__(self, width=32, height=32, color=(255, 0, 0), image_path=None, layer=0):
        """Initialize a new RenderComponent.
        
        Args:
            width (int): The width of the entity's visual representation.
            height (int): The height of the entity's visual representation.
            color (tuple): The RGB color of the entity if no image is provided.
            image_path (str, optional): Path to the image file to use for rendering.
            layer (int): The rendering layer (higher values are rendered on top).
        """
        super().__init__()
        self.width = width
        self.height = height
        self.color = color
        self.image_path = image_path
        self.image = None
        self.layer = layer
        
        # Load the image if a path was provided
        if image_path:
            try:
                self.image = pygame.image.load(image_path).convert_alpha()
                self.image = pygame.transform.scale(self.image, (width, height))
            except pygame.error:
                print(f"Warning: Could not load image {image_path}")
                self.image = None
    
    def get_rect(self, position):
        """Get the pygame Rect for this entity at the given position.
        
        Args:
            position (Vector2): The position to get the rect for.
            
        Returns:
            pygame.Rect: The rect for this entity at the given position.
        """
        return pygame.Rect(
            position.x - self.width / 2,
            position.y - self.height / 2,
            self.width,
            self.height
        )
