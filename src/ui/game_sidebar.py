"""
Game sidebar UI for the tower defense game.
"""
import pygame
from src.ui.panel import Panel
from src.ui.button import Button
from src.ui.label import Label
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, GRAY, BLUE, GREEN, RED


class GameSidebar:
    """Sidebar UI for the game scene."""

    def __init__(self, game_scene):
        """Initialize a new GameSidebar.

        Args:
            game_scene: The game scene this sidebar belongs to.
        """
        self.game_scene = game_scene
        self.game = game_scene.game

        # Create UI elements
        self.create_ui()

    def create_ui(self):
        """Create the UI elements for the sidebar."""
        # Sidebar panel
        sidebar_width = 200
        sidebar_height = SCREEN_HEIGHT
        sidebar_x = SCREEN_WIDTH - sidebar_width
        sidebar_y = 0

        self.sidebar_panel = Panel(
            sidebar_x, sidebar_y, sidebar_width, sidebar_height,
            bg_color=(40, 40, 40), alpha=200
        )

        # Title
        title_label = Label(
            0, 20, "Tower Defense",
            text_color=WHITE, font_size=24, align="center"
        )
        title_label.set_position(
            sidebar_x + (sidebar_width - title_label.width) // 2,
            20
        )

        # Resources
        self.resources_label = Label(
            sidebar_x + 10, 70, "Resources: 0",
            text_color=WHITE, font_size=18
        )

        # Wave info
        self.wave_label = Label(
            sidebar_x + 10, 100, "Wave: 0",
            text_color=WHITE, font_size=18
        )

        self.enemies_label = Label(
            sidebar_x + 10, 130, "Enemies: 0",
            text_color=WHITE, font_size=18
        )

        # Tower selection title
        tower_selection_label = Label(
            0, 180, "Tower Selection",
            text_color=WHITE, font_size=20, align="center"
        )
        tower_selection_label.set_position(
            sidebar_x + (sidebar_width - tower_selection_label.width) // 2,
            180
        )

        # Tower buttons
        button_width = 160
        button_height = 50
        button_x = sidebar_x + (sidebar_width - button_width) // 2
        button_spacing = 20

        # Basic tower button
        self.basic_tower_button = Button(
            button_x, 220,
            button_width, button_height,
            "Basic Tower (50)", self.on_basic_tower_clicked,
            bg_color=BLUE, text_color=WHITE
        )

        # Start wave button
        self.start_wave_button = Button(
            button_x, SCREEN_HEIGHT - 100,
            button_width, button_height,
            "Start Wave", self.on_start_wave_clicked,
            bg_color=GREEN, text_color=WHITE
        )

        # Add elements to the sidebar
        self.ui_elements = [
            self.sidebar_panel,
            title_label,
            self.resources_label,
            self.wave_label,
            self.enemies_label,
            tower_selection_label,
            self.basic_tower_button,
            self.start_wave_button
        ]

    def on_basic_tower_clicked(self):
        """Handle the basic tower button click."""
        if self.game_scene.economy_manager.can_afford("basic"):
            self.game_scene.selected_tower_type = "basic"
            self.game_scene.placing_tower = True
            mouse_pos = pygame.mouse.get_pos()
            self.game_scene.tower_placement_pos.x = mouse_pos[0]
            self.game_scene.tower_placement_pos.y = mouse_pos[1]
            self.game_scene.can_place_tower = self.game_scene.check_tower_placement()

    def on_start_wave_clicked(self):
        """Handle the start wave button click."""
        self.game_scene.wave_manager.start_next_wave()

    def update(self, dt):
        """Update the sidebar.

        Args:
            dt (float): The time delta since the last update in seconds.
        """
        # Update resource display
        resources = self.game_scene.economy_manager.get_resources()
        self.resources_label.set_text(f"Resources: {resources}")

        # Update wave info
        wave = self.game_scene.wave_manager.get_current_wave()
        self.wave_label.set_text(f"Wave: {wave}")

        enemies = self.game_scene.wave_manager.get_enemies_remaining()
        self.enemies_label.set_text(f"Enemies: {enemies}")

        # Update button states
        can_afford_basic = self.game_scene.economy_manager.can_afford("basic")
        self.basic_tower_button.enabled = can_afford_basic
        self.basic_tower_button.bg_color = BLUE if can_afford_basic else GRAY

        # Update Start Wave button state
        wave_in_progress = enemies > 0
        self.start_wave_button.enabled = not wave_in_progress
        self.start_wave_button.bg_color = GREEN if not wave_in_progress else GRAY
        self.start_wave_button.text = "Wave in Progress..." if wave_in_progress else "Start Wave"

        # Update UI elements
        for element in self.ui_elements:
            element.update(dt)

    def render(self, screen):
        """Render the sidebar.

        Args:
            screen (pygame.Surface): The screen to render to.
        """
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
        # Handle UI element events
        for element in reversed(self.ui_elements):
            if element.handle_event(event):
                return True

        return False
