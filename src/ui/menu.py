"""
Menu system for the Tower Defense Game
"""
import pygame
from typing import List, Dict, Any, Tuple, Optional, Callable

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from utils import draw_text

class Button:
    """Button class for menus"""

    def __init__(self, rect: pygame.Rect, text: str, action: str,
                 color: Tuple[int, int, int] = (100, 100, 100),
                 hover_color: Tuple[int, int, int] = (150, 150, 150),
                 text_color: Tuple[int, int, int] = (255, 255, 255)):
        """
        Initialize a button

        Args:
            rect: Button rectangle
            text: Button text
            action: Action identifier
            color: Button color
            hover_color: Button color when hovered
            text_color: Text color
        """
        self.rect = rect
        self.text = text
        self.action = action
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hovered = False

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the button

        Args:
            surface: Pygame surface to draw on
        """
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (200, 200, 200), self.rect, 2)

        draw_text(surface, self.text,
                  (self.rect.centerx, self.rect.centery),
                  self.text_color, centered=True)

    def update(self, mouse_pos: Tuple[int, int]) -> None:
        """
        Update button state based on mouse position

        Args:
            mouse_pos: Mouse position (x, y)
        """
        self.hovered = self.rect.collidepoint(mouse_pos)

    def handle_click(self, mouse_pos: Tuple[int, int]) -> Optional[str]:
        """
        Handle mouse click

        Args:
            mouse_pos: Mouse position (x, y)

        Returns:
            Action identifier if clicked, None otherwise
        """
        if self.rect.collidepoint(mouse_pos):
            return self.action
        return None

class Menu:
    """Base class for menus"""

    def __init__(self):
        """Initialize the menu"""
        self.buttons = []

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the menu

        Args:
            surface: Pygame surface to draw on
        """
        # Draw background
        surface.fill((30, 30, 30))

        # Draw buttons
        for button in self.buttons:
            button.draw(surface)

    def update(self, mouse_pos: Tuple[int, int]) -> None:
        """
        Update menu state

        Args:
            mouse_pos: Mouse position (x, y)
        """
        for button in self.buttons:
            button.update(mouse_pos)

    def handle_click(self, mouse_pos: Tuple[int, int]) -> Optional[str]:
        """
        Handle mouse click

        Args:
            mouse_pos: Mouse position (x, y)

        Returns:
            Action identifier if a button was clicked, None otherwise
        """
        for button in self.buttons:
            action = button.handle_click(mouse_pos)
            if action:
                return action
        return None

class MainMenu(Menu):
    """Main menu"""

    def __init__(self):
        """Initialize the main menu"""
        super().__init__()

        # Create buttons
        button_width = 200
        button_height = 50
        button_spacing = 20
        start_y = SCREEN_HEIGHT // 2 - 50

        # Start game button
        self.buttons.append(Button(
            pygame.Rect(
                SCREEN_WIDTH // 2 - button_width // 2,
                start_y,
                button_width,
                button_height
            ),
            "Start Game",
            "start_game",
            color=(0, 150, 0),
            hover_color=(0, 200, 0)
        ))

        # Options button
        self.buttons.append(Button(
            pygame.Rect(
                SCREEN_WIDTH // 2 - button_width // 2,
                start_y + button_height + button_spacing,
                button_width,
                button_height
            ),
            "Options",
            "options",
            color=(0, 100, 150),
            hover_color=(0, 150, 200)
        ))

        # Quit button
        self.buttons.append(Button(
            pygame.Rect(
                SCREEN_WIDTH // 2 - button_width // 2,
                start_y + (button_height + button_spacing) * 2,
                button_width,
                button_height
            ),
            "Quit",
            "quit",
            color=(150, 0, 0),
            hover_color=(200, 0, 0)
        ))

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the main menu

        Args:
            surface: Pygame surface to draw on
        """
        super().draw(surface)

        # Draw title
        draw_text(surface, "Minion Tower Defense",
                  (SCREEN_WIDTH // 2, 100),
                  (255, 255, 255), font_size=48, centered=True)

        # Draw subtitle
        draw_text(surface, "Defend against the minions!",
                  (SCREEN_WIDTH // 2, 160),
                  (200, 200, 200), font_size=24, centered=True)

class PauseMenu(Menu):
    """Pause menu"""

    def __init__(self):
        """Initialize the pause menu"""
        super().__init__()

        # Create buttons
        button_width = 200
        button_height = 50
        button_spacing = 20
        start_y = SCREEN_HEIGHT // 2 - 50

        # Resume button
        self.buttons.append(Button(
            pygame.Rect(
                SCREEN_WIDTH // 2 - button_width // 2,
                start_y,
                button_width,
                button_height
            ),
            "Resume",
            "resume",
            color=(0, 150, 0),
            hover_color=(0, 200, 0)
        ))

        # Main menu button
        self.buttons.append(Button(
            pygame.Rect(
                SCREEN_WIDTH // 2 - button_width // 2,
                start_y + button_height + button_spacing,
                button_width,
                button_height
            ),
            "Main Menu",
            "main_menu",
            color=(0, 100, 150),
            hover_color=(0, 150, 200)
        ))

        # Quit button
        self.buttons.append(Button(
            pygame.Rect(
                SCREEN_WIDTH // 2 - button_width // 2,
                start_y + (button_height + button_spacing) * 2,
                button_width,
                button_height
            ),
            "Quit",
            "quit",
            color=(150, 0, 0),
            hover_color=(200, 0, 0)
        ))

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the pause menu

        Args:
            surface: Pygame surface to draw on
        """
        # Draw semi-transparent background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        surface.blit(overlay, (0, 0))

        # Draw title
        draw_text(surface, "Game Paused",
                  (SCREEN_WIDTH // 2, 100),
                  (255, 255, 255), font_size=48, centered=True)

        # Draw buttons
        for button in self.buttons:
            button.draw(surface)

class GameOverMenu(Menu):
    """Game over menu"""

    def __init__(self, won: bool = False):
        """
        Initialize the game over menu

        Args:
            won: Whether the player won the game
        """
        super().__init__()
        self.won = won

        # Create buttons
        button_width = 200
        button_height = 50
        button_spacing = 20
        start_y = SCREEN_HEIGHT // 2 + 50

        # Restart button
        self.buttons.append(Button(
            pygame.Rect(
                SCREEN_WIDTH // 2 - button_width // 2,
                start_y,
                button_width,
                button_height
            ),
            "Play Again",
            "restart",
            color=(0, 150, 0),
            hover_color=(0, 200, 0)
        ))

        # Main menu button
        self.buttons.append(Button(
            pygame.Rect(
                SCREEN_WIDTH // 2 - button_width // 2,
                start_y + button_height + button_spacing,
                button_width,
                button_height
            ),
            "Main Menu",
            "main_menu",
            color=(0, 100, 150),
            hover_color=(0, 150, 200)
        ))

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the game over menu

        Args:
            surface: Pygame surface to draw on
        """
        # Draw semi-transparent background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 192))
        surface.blit(overlay, (0, 0))

        # Draw title
        if self.won:
            draw_text(surface, "Victory!",
                      (SCREEN_WIDTH // 2, 100),
                      (0, 255, 0), font_size=64, centered=True)
            draw_text(surface, "You have defeated all the minions!",
                      (SCREEN_WIDTH // 2, 170),
                      (200, 255, 200), font_size=24, centered=True)
        else:
            draw_text(surface, "Game Over",
                      (SCREEN_WIDTH // 2, 100),
                      (255, 0, 0), font_size=64, centered=True)
            draw_text(surface, "The minions have overwhelmed your defenses!",
                      (SCREEN_WIDTH // 2, 170),
                      (255, 200, 200), font_size=24, centered=True)

        # Draw buttons
        for button in self.buttons:
            button.draw(surface)
