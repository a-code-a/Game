"""
Button UI element for the tower defense game.
"""
import pygame
from src.ui.ui_element import UIElement
from src.config import WHITE, BLACK, GRAY


class Button(UIElement):
    """Button UI element that can be clicked."""

    def __init__(self, x, y, width, height, text, callback=None,
                 bg_color=GRAY, hover_color=None, text_color=BLACK,
                 font_name="arial", font_size=24, border_radius=5):
        """Initialize a new Button.

        Args:
            x (int): The x-coordinate of the button.
            y (int): The y-coordinate of the button.
            width (int): The width of the button.
            height (int): The height of the button.
            text (str): The text to display on the button.
            callback (function, optional): The function to call when the button is clicked.
            bg_color (tuple): The background color of the button.
            hover_color (tuple, optional): The background color when hovering. If None, a lighter version of bg_color is used.
            text_color (tuple): The color of the text.
            font_name (str): The name of the font to use.
            font_size (int): The size of the font.
            border_radius (int): The radius of the button's rounded corners.
        """
        super().__init__(x, y, width, height)

        self.callback = callback
        self.bg_color = bg_color
        self.hover_color = hover_color or self._lighten_color(bg_color, 30)
        self.text_color = text_color
        self.font = pygame.font.SysFont(font_name, font_size)
        self.border_radius = border_radius

        # State
        self.hovered = False
        self.pressed = False

        # Initialize text (will create text_surface and text_rect)
        self._text = ""
        self.text = text

    def _lighten_color(self, color, amount):
        """Lighten a color by the given amount.

        Args:
            color (tuple): The RGB color to lighten.
            amount (int): The amount to lighten by (0-255).

        Returns:
            tuple: The lightened color.
        """
        r, g, b = color
        return (
            min(r + amount, 255),
            min(g + amount, 255),
            min(b + amount, 255)
        )

    @property
    def text(self):
        """Get the button text.

        Returns:
            str: The button text.
        """
        return self._text

    @text.setter
    def text(self, value):
        """Set the button text.

        Args:
            value (str): The new text.
        """
        self._text = value
        self.text_surface = self.font.render(value, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))

    def set_text(self, text):
        """Set the text of the button.

        Args:
            text (str): The new text.
        """
        self.text = text

    def set_position(self, x, y):
        """Set the position of the button.

        Args:
            x (int): The new x-coordinate.
            y (int): The new y-coordinate.
        """
        super().set_position(x, y)
        self.text_rect = self.text_surface.get_rect(center=(x + self.width // 2, y + self.height // 2))

    def update(self, dt):
        """Update the button.

        Args:
            dt (float): The time delta since the last update in seconds.
        """
        super().update(dt)

        # Check if the mouse is hovering over the button
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.is_point_inside(mouse_pos)

    def render(self, screen):
        """Render the button.

        Args:
            screen (pygame.Surface): The screen to render to.
        """
        if not self.visible:
            return

        # Draw the button background
        color = self.hover_color if self.hovered else self.bg_color
        if self.pressed:
            color = self._lighten_color(color, -20)  # Darken when pressed

        pygame.draw.rect(screen, color, self.rect, border_radius=self.border_radius)

        # Draw the button text
        screen.blit(self.text_surface, self.text_rect)

        # Render children
        super().render(screen)

    def handle_event(self, event):
        """Handle a pygame event.

        Args:
            event (pygame.event.Event): The event to handle.

        Returns:
            bool: True if the event was handled, False otherwise.
        """
        if not self.enabled:
            return False

        # Check if children handled the event
        if super().handle_event(event):
            return True

        # Handle button events
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            if self.hovered:
                self.pressed = True
                return True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # Left mouse button
            was_pressed = self.pressed
            self.pressed = False

            if was_pressed and self.hovered and self.callback:
                self.callback()
                return True

        return False
