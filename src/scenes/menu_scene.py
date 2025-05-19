"""
Menu scene for the tower defense game.
"""
import pygame
from src.core.scene import Scene
from src.ui.button import Button
from src.ui.panel import Panel
from src.ui.label import Label
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, GRAY, BLUE, TITLE


class MenuScene(Scene):
    """Scene for the main menu."""
    
    def __init__(self, game):
        """Initialize a new MenuScene.
        
        Args:
            game: The game instance this scene belongs to.
        """
        super().__init__(game)
        
        # Create UI elements
        self.create_ui()
    
    def create_ui(self):
        """Create the UI elements for the menu."""
        # Main panel
        panel_width = 400
        panel_height = 450
        panel_x = (SCREEN_WIDTH - panel_width) // 2
        panel_y = (SCREEN_HEIGHT - panel_height) // 2
        
        self.main_panel = Panel(
            panel_x, panel_y, panel_width, panel_height,
            bg_color=(50, 50, 50), alpha=230, border_radius=10
        )
        
        # Title
        title_label = Label(
            0, 30, TITLE,
            text_color=WHITE, font_size=48, align="center"
        )
        title_label.set_position(
            panel_x + (panel_width - title_label.width) // 2,
            panel_y + 30
        )
        
        # Buttons
        button_width = 200
        button_height = 50
        button_x = panel_x + (panel_width - button_width) // 2
        button_spacing = 20
        
        # Play button
        play_button = Button(
            button_x, panel_y + 150,
            button_width, button_height,
            "Play", self.on_play_clicked,
            bg_color=BLUE, text_color=WHITE
        )
        
        # Options button
        options_button = Button(
            button_x, play_button.y + button_height + button_spacing,
            button_width, button_height,
            "Options", self.on_options_clicked,
            bg_color=GRAY, text_color=BLACK
        )
        
        # Quit button
        quit_button = Button(
            button_x, options_button.y + button_height + button_spacing,
            button_width, button_height,
            "Quit", self.on_quit_clicked,
            bg_color=GRAY, text_color=BLACK
        )
        
        # Add elements to the scene
        self.ui_elements = [
            self.main_panel,
            title_label,
            play_button,
            options_button,
            quit_button
        ]
    
    def on_play_clicked(self):
        """Handle the play button click."""
        self.game.scene_manager.set_scene("game")
    
    def on_options_clicked(self):
        """Handle the options button click."""
        # For now, just print a message
        print("Options button clicked")
    
    def on_quit_clicked(self):
        """Handle the quit button click."""
        self.game.quit()
    
    def update(self, dt):
        """Update the scene.
        
        Args:
            dt (float): The time delta since the last update in seconds.
        """
        # Update UI elements
        for element in self.ui_elements:
            element.update(dt)
    
    def render(self, screen):
        """Render the scene.
        
        Args:
            screen (pygame.Surface): The screen to render to.
        """
        # Clear the screen with a dark background
        screen.fill((20, 20, 20))
        
        # Render UI elements
        for element in self.ui_elements:
            element.render(screen)
    
    def handle_event(self, event):
        """Handle a pygame event.
        
        Args:
            event (pygame.event.Event): The event to handle.
        """
        # Handle UI element events
        for element in reversed(self.ui_elements):
            if element.handle_event(event):
                return True
        
        return False
