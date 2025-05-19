"""
Label UI element for the tower defense game.
"""
import pygame
from src.ui.ui_element import UIElement
from src.config import WHITE, BLACK


class Label(UIElement):
    """Label UI element that displays text."""
    
    def __init__(self, x, y, text, text_color=WHITE, font_name="arial", font_size=24, 
                 align="left", bg_color=None, padding=0):
        """Initialize a new Label.
        
        Args:
            x (int): The x-coordinate of the label.
            y (int): The y-coordinate of the label.
            text (str): The text to display.
            text_color (tuple): The color of the text.
            font_name (str): The name of the font to use.
            font_size (int): The size of the font.
            align (str): The text alignment ("left", "center", or "right").
            bg_color (tuple, optional): The background color of the label. If None, the background is transparent.
            padding (int): Padding around the text.
        """
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.SysFont(font_name, font_size)
        self.align = align
        self.bg_color = bg_color
        self.padding = padding
        
        # Render the text to determine its size
        self.text_surface = self.font.render(text, True, text_color)
        text_width, text_height = self.text_surface.get_size()
        
        # Set the label size based on the text size and padding
        width = text_width + (padding * 2)
        height = text_height + (padding * 2)
        
        super().__init__(x, y, width, height)
        
        # Set the text position based on alignment
        self._update_text_position()
    
    def _update_text_position(self):
        """Update the position of the text based on alignment."""
        if self.align == "left":
            self.text_rect = self.text_surface.get_rect(
                topleft=(self.x + self.padding, self.y + self.padding)
            )
        elif self.align == "center":
            self.text_rect = self.text_surface.get_rect(
                center=(self.x + self.width // 2, self.y + self.height // 2)
            )
        elif self.align == "right":
            self.text_rect = self.text_surface.get_rect(
                topright=(self.x + self.width - self.padding, self.y + self.padding)
            )
    
    def set_text(self, text):
        """Set the text of the label.
        
        Args:
            text (str): The new text.
        """
        self.text = text
        self.text_surface = self.font.render(text, True, self.text_color)
        
        # Update the label size if needed
        text_width, text_height = self.text_surface.get_size()
        width = text_width + (self.padding * 2)
        height = text_height + (self.padding * 2)
        self.set_size(width, height)
        
        # Update the text position
        self._update_text_position()
    
    def set_position(self, x, y):
        """Set the position of the label.
        
        Args:
            x (int): The new x-coordinate.
            y (int): The new y-coordinate.
        """
        super().set_position(x, y)
        self._update_text_position()
    
    def render(self, screen):
        """Render the label.
        
        Args:
            screen (pygame.Surface): The screen to render to.
        """
        if not self.visible:
            return
        
        # Draw the background if needed
        if self.bg_color:
            pygame.draw.rect(screen, self.bg_color, self.rect)
        
        # Draw the text
        screen.blit(self.text_surface, self.text_rect)
        
        # Render children
        super().render(screen)
