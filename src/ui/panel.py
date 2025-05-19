"""
Panel UI element for the tower defense game.
"""
import pygame
from src.ui.ui_element import UIElement
from src.config import GRAY


class Panel(UIElement):
    """Panel UI element that can contain other UI elements."""
    
    def __init__(self, x, y, width, height, bg_color=GRAY, alpha=255, border_radius=0, border_width=0, border_color=None):
        """Initialize a new Panel.
        
        Args:
            x (int): The x-coordinate of the panel.
            y (int): The y-coordinate of the panel.
            width (int): The width of the panel.
            height (int): The height of the panel.
            bg_color (tuple): The background color of the panel.
            alpha (int): The alpha value of the panel (0-255).
            border_radius (int): The radius of the panel's rounded corners.
            border_width (int): The width of the panel's border.
            border_color (tuple, optional): The color of the panel's border. If None, a darker version of bg_color is used.
        """
        super().__init__(x, y, width, height)
        
        self.bg_color = bg_color
        self.alpha = alpha
        self.border_radius = border_radius
        self.border_width = border_width
        self.border_color = border_color or self._darken_color(bg_color, 50)
        
        # Create a surface for the panel
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    def _darken_color(self, color, amount):
        """Darken a color by the given amount.
        
        Args:
            color (tuple): The RGB color to darken.
            amount (int): The amount to darken by (0-255).
            
        Returns:
            tuple: The darkened color.
        """
        r, g, b = color
        return (
            max(r - amount, 0),
            max(g - amount, 0),
            max(b - amount, 0)
        )
    
    def set_size(self, width, height):
        """Set the size of the panel.
        
        Args:
            width (int): The new width.
            height (int): The new height.
        """
        super().set_size(width, height)
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    def render(self, screen):
        """Render the panel.
        
        Args:
            screen (pygame.Surface): The screen to render to.
        """
        if not self.visible:
            return
        
        # Clear the surface
        self.surface.fill((0, 0, 0, 0))
        
        # Draw the panel background
        bg_color_with_alpha = (*self.bg_color, self.alpha)
        pygame.draw.rect(
            self.surface, 
            bg_color_with_alpha, 
            (0, 0, self.width, self.height),
            border_radius=self.border_radius
        )
        
        # Draw the border if needed
        if self.border_width > 0:
            border_color_with_alpha = (*self.border_color, self.alpha)
            pygame.draw.rect(
                self.surface,
                border_color_with_alpha,
                (0, 0, self.width, self.height),
                width=self.border_width,
                border_radius=self.border_radius
            )
        
        # Blit the surface to the screen
        screen.blit(self.surface, (self.x, self.y))
        
        # Render children
        super().render(screen)
