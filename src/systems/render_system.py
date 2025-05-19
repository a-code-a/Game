"""
Render system for the Entity Component System.
"""
import pygame
from src.systems.system import System


class RenderSystem(System):
    """System that renders all entities with position and render components."""
    
    def __init__(self, screen):
        """Initialize a new RenderSystem.
        
        Args:
            screen (pygame.Surface): The screen to render to.
        """
        super().__init__()
        self.screen = screen
    
    def process(self, dt):
        """Render all entities with position and render components.
        
        Args:
            dt (float): The time delta since the last update in seconds.
        """
        # Sort entities by layer
        sorted_entities = sorted(
            self.entities,
            key=lambda e: e.get_component("render").layer
        )
        
        # Render each entity
        for entity in sorted_entities:
            if not entity.active:
                continue
                
            position_component = entity.get_component("position")
            render_component = entity.get_component("render")
            
            if not position_component or not render_component:
                continue
            
            # Get the position and render rect
            pos = position_component.position
            rect = render_component.get_rect(pos)
            
            # Render the entity
            if render_component.image:
                # Rotate and scale the image if needed
                if position_component.rotation != 0 or position_component.scale != 1:
                    rotated_image = pygame.transform.rotozoom(
                        render_component.image,
                        position_component.rotation,
                        position_component.scale
                    )
                    rotated_rect = rotated_image.get_rect(center=rect.center)
                    self.screen.blit(rotated_image, rotated_rect)
                else:
                    self.screen.blit(render_component.image, rect)
            else:
                # Draw a rectangle if no image is available
                pygame.draw.rect(self.screen, render_component.color, rect)
    
    def should_process(self, entity):
        """Check if this system should process the given entity.
        
        Args:
            entity (Entity): The entity to check.
            
        Returns:
            bool: True if the entity should be processed, False otherwise.
        """
        return (entity.active and
                entity.has_component("position") and
                entity.has_component("render"))
