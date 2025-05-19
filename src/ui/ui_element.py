"""
Base UI element class for the tower defense game.
"""
import pygame


class UIElement:
    """Base class for all UI elements."""
    
    def __init__(self, x, y, width, height):
        """Initialize a new UIElement.
        
        Args:
            x (int): The x-coordinate of the element.
            y (int): The y-coordinate of the element.
            width (int): The width of the element.
            height (int): The height of the element.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True
        self.enabled = True
        self.parent = None
        self.children = []
    
    def set_position(self, x, y):
        """Set the position of the element.
        
        Args:
            x (int): The new x-coordinate.
            y (int): The new y-coordinate.
        """
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        
        # Update children positions if they have relative positioning
        for child in self.children:
            if hasattr(child, 'relative_x') and hasattr(child, 'relative_y'):
                child.set_position(x + child.relative_x, y + child.relative_y)
    
    def set_size(self, width, height):
        """Set the size of the element.
        
        Args:
            width (int): The new width.
            height (int): The new height.
        """
        self.width = width
        self.height = height
        self.rect.width = width
        self.rect.height = height
    
    def add_child(self, child):
        """Add a child element.
        
        Args:
            child (UIElement): The child element to add.
        """
        child.parent = self
        self.children.append(child)
    
    def remove_child(self, child):
        """Remove a child element.
        
        Args:
            child (UIElement): The child element to remove.
        """
        if child in self.children:
            child.parent = None
            self.children.remove(child)
    
    def is_point_inside(self, point):
        """Check if a point is inside the element.
        
        Args:
            point (tuple): The point to check (x, y).
            
        Returns:
            bool: True if the point is inside the element, False otherwise.
        """
        return self.rect.collidepoint(point)
    
    def update(self, dt):
        """Update the element.
        
        Args:
            dt (float): The time delta since the last update in seconds.
        """
        # Update children
        for child in self.children:
            child.update(dt)
    
    def render(self, screen):
        """Render the element.
        
        Args:
            screen (pygame.Surface): The screen to render to.
        """
        if not self.visible:
            return
        
        # Render children
        for child in self.children:
            child.render(screen)
    
    def handle_event(self, event):
        """Handle a pygame event.
        
        Args:
            event (pygame.event.Event): The event to handle.
            
        Returns:
            bool: True if the event was handled, False otherwise.
        """
        if not self.enabled:
            return False
        
        # Handle children events first (in reverse order for proper layering)
        for child in reversed(self.children):
            if child.handle_event(event):
                return True
        
        return False
