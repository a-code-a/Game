"""
Pause menu overlay for the tower defense game.
"""
import pygame
from src.ui.panel import Panel
from src.ui.button import Button
from src.ui.label import Label
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, GRAY, BLUE


class PauseMenu:
    """Pause menu overlay that can be added to any scene."""
    
    def __init__(self, game):
        """Initialize a new PauseMenu.
        
        Args:
            game: The game instance this menu belongs to.
        """
        self.game = game
        self.visible = False
        
        # Create UI elements
        self.create_ui()
    
    def create_ui(self):
        """Create the UI elements for the pause menu."""
        # Main panel
        panel_width = 300
        panel_height = 350
        panel_x = (SCREEN_WIDTH - panel_width) // 2
        panel_y = (SCREEN_HEIGHT - panel_height) // 2
        
        self.main_panel = Panel(
            panel_x, panel_y, panel_width, panel_height,
            bg_color=(50, 50, 50), alpha=230, border_radius=10
        )
        
        # Title
        title_label = Label(
            0, 30, "PAUSED",
            text_color=WHITE, font_size=36, align="center"
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
        
        # Resume button
        resume_button = Button(
            button_x, panel_y + 100,
            button_width, button_height,
            "Resume", self.on_resume_clicked,
            bg_color=BLUE, text_color=WHITE
        )
        
        # Restart button
        restart_button = Button(
            button_x, resume_button.y + button_height + button_spacing,
            button_width, button_height,
            "Restart", self.on_restart_clicked,
            bg_color=GRAY, text_color=BLACK
        )
        
        # Main Menu button
        main_menu_button = Button(
            button_x, restart_button.y + button_height + button_spacing,
            button_width, button_height,
            "Main Menu", self.on_main_menu_clicked,
            bg_color=GRAY, text_color=BLACK
        )
        
        # Add elements to the menu
        self.ui_elements = [
            self.main_panel,
            title_label,
            resume_button,
            restart_button,
            main_menu_button
        ]
    
    def on_resume_clicked(self):
        """Handle the resume button click."""
        self.game.paused = False
        self.visible = False
    
    def on_restart_clicked(self):
        """Handle the restart button click."""
        # Reset the current scene
        current_scene_name = None
        for name, scene in self.game.scene_manager.scenes.items():
            if scene == self.game.scene_manager.current_scene:
                current_scene_name = name
                break
        
        if current_scene_name:
            # Create a new instance of the current scene
            scene_class = self.game.scene_manager.current_scene.__class__
            new_scene = scene_class(self.game)
            
            # Replace the old scene
            self.game.scene_manager.scenes[current_scene_name] = new_scene
            self.game.scene_manager.set_scene(current_scene_name)
        
        # Unpause the game
        self.game.paused = False
        self.visible = False
    
    def on_main_menu_clicked(self):
        """Handle the main menu button click."""
        # Go to the main menu
        self.game.scene_manager.set_scene("menu")
        
        # Unpause the game
        self.game.paused = False
        self.visible = False
    
    def show(self):
        """Show the pause menu."""
        self.visible = True
    
    def hide(self):
        """Hide the pause menu."""
        self.visible = False
    
    def update(self, dt):
        """Update the pause menu.
        
        Args:
            dt (float): The time delta since the last update in seconds.
        """
        if not self.visible:
            return
        
        # Update UI elements
        for element in self.ui_elements:
            element.update(dt)
    
    def render(self, screen):
        """Render the pause menu.
        
        Args:
            screen (pygame.Surface): The screen to render to.
        """
        if not self.visible:
            return
        
        # Create a semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))
        
        # Render UI elements
        for element in self.ui_elements:
            element.render(screen)
    
    def handle_event(self, event):
        """Handle a pygame event.
        
        Args:
            event (pygame.event.Event): The event to handle.
            
        Returns:
            bool: True if the event was handled, False otherwise.
        """
        if not self.visible:
            return False
        
        # Handle UI element events
        for element in reversed(self.ui_elements):
            if element.handle_event(event):
                return True
        
        return False
