"""
Main game module for the Tower Defense Game
"""
import pygame
import sys
from typing import Dict, Any, Optional, Tuple

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, SIDEBAR_WIDTH
from managers.game_manager import GameManager
from maps.map1 import Map1
from ui.hud import HUD
from ui.menu import MainMenu, PauseMenu, GameOverMenu

class Game:
    """Main game class"""

    def __init__(self):
        """Initialize the game"""
        pygame.init()
        pygame.mixer.init()

        # Create the window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Minion Tower Defense")

        # Set up the clock
        self.clock = pygame.time.Clock()

        # Game state
        self.running = True
        self.current_screen = "main_menu"

        # Create menus
        self.main_menu = MainMenu()
        self.pause_menu = PauseMenu()
        self.game_over_menu = None

        # Create game objects
        self.current_map = Map1()
        self.game_manager = GameManager(self.current_map)
        self.hud = HUD()

        # Tower placement
        self.placing_tower = False
        self.tower_placement_valid = False

    def run(self) -> None:
        """Run the game loop"""
        while self.running:
            # Handle events
            self.handle_events()

            # Update game state
            self.update()

            # Draw the screen
            self.draw()

            # Cap the frame rate
            self.clock.tick(FPS)

        # Clean up
        pygame.quit()
        sys.exit()

    def handle_events(self) -> None:
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.current_screen == "game":
                        self.current_screen = "pause_menu"
                    elif self.current_screen == "pause_menu":
                        self.current_screen = "game"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.handle_mouse_click(pygame.mouse.get_pos())

    def handle_mouse_click(self, pos: Tuple[int, int]) -> None:
        """
        Handle mouse click

        Args:
            pos: Mouse position (x, y)
        """
        if self.current_screen == "main_menu":
            action = self.main_menu.handle_click(pos)
            if action == "start_game":
                self.current_screen = "game"
            elif action == "options":
                pass  # TODO: Implement options menu
            elif action == "quit":
                self.running = False

        elif self.current_screen == "pause_menu":
            action = self.pause_menu.handle_click(pos)
            if action == "resume":
                self.current_screen = "game"
            elif action == "main_menu":
                self.current_screen = "main_menu"
                self.game_manager = GameManager(self.current_map)
            elif action == "quit":
                self.running = False

        elif self.current_screen == "game_over":
            action = self.game_over_menu.handle_click(pos)
            if action == "restart":
                self.current_screen = "game"
                self.game_manager = GameManager(self.current_map)
            elif action == "main_menu":
                self.current_screen = "main_menu"
                self.game_manager = GameManager(self.current_map)

        elif self.current_screen == "game":
            # First check for menu button clicks (can be anywhere on screen)
            action_info = self.hud.handle_click(pos, self.game_manager.get_game_state())
            action = action_info.get('action', 'none')

            # Handle menu actions
            if action in ['main_menu', 'settings', 'resume']:
                self.handle_menu_action(action)
                return
            elif action in ['toggle_menu', 'close_menu']:
                return  # Just toggle menu state, no further action needed

            # If not a menu action, continue with normal game clicks
            if pos[0] > SCREEN_WIDTH - SIDEBAR_WIDTH:
                # Handle HUD click
                self.handle_hud_action(action_info)
            else:
                # Handle game area click
                if self.placing_tower:
                    # Try to place the tower
                    grid_pos = self.current_map.pixel_to_grid(pos)
                    if self.game_manager.place_tower(grid_pos, self.hud.selected_tower_type):
                        self.placing_tower = False
                        self.hud.selected_tower_type = None
                else:
                    # Try to select a tower
                    self.game_manager.select_tower(pos)

    def handle_menu_action(self, action: str) -> None:
        """
        Handle menu button actions

        Args:
            action: Action to perform
        """
        if action == 'main_menu':
            self.current_screen = "main_menu"
            self.game_manager = GameManager(self.current_map)
        elif action == 'settings':
            # For now, just pause the game
            # In the future, this could open a settings menu
            self.current_screen = "pause_menu"
        elif action == 'resume':
            # Resume from pause menu
            self.current_screen = "game"

    def handle_hud_action(self, action_info: Dict[str, Any]) -> None:
        """
        Handle HUD action

        Args:
            action_info: Action information
        """
        action = action_info.get('action', 'none')

        if action == 'select_tower_type':
            self.placing_tower = True
            self.hud.selected_tower_type = action_info['tower_type']

        elif action == 'start_wave':
            self.game_manager.start_wave()

        elif action == 'upgrade_tower':
            self.game_manager.upgrade_selected_tower(action_info['path'])

        elif action == 'sell_tower':
            self.game_manager.sell_selected_tower()

        elif action == 'set_targeting':
            self.game_manager.set_tower_targeting(action_info['strategy'])

        elif action == 'deselect_tower':
            # Deselect the current tower
            if self.game_manager.selected_tower:
                self.game_manager.selected_tower.selected = False
                self.game_manager.selected_tower = None

    def update(self) -> None:
        """Update game state"""
        if self.current_screen == "main_menu":
            self.main_menu.update(pygame.mouse.get_pos())

        elif self.current_screen == "pause_menu":
            self.pause_menu.update(pygame.mouse.get_pos())

        elif self.current_screen == "game_over":
            self.game_over_menu.update(pygame.mouse.get_pos())

        elif self.current_screen == "game":
            # Update game manager
            self.game_manager.update()

            # Check for game over
            game_state = self.game_manager.get_game_state()
            if game_state['game_over']:
                self.game_over_menu = GameOverMenu(won=game_state['game_won'])
                self.current_screen = "game_over"

            # Update tower placement validity
            if self.placing_tower:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[0] < SCREEN_WIDTH - SIDEBAR_WIDTH:
                    grid_pos = self.current_map.pixel_to_grid(mouse_pos)
                    self.tower_placement_valid = self.game_manager.is_valid_tower_position(grid_pos)
                else:
                    self.tower_placement_valid = False

    def draw(self) -> None:
        """Draw the current screen"""
        if self.current_screen == "main_menu":
            self.main_menu.draw(self.screen)

        elif self.current_screen == "pause_menu":
            # Draw the game in the background
            self.game_manager.draw(self.screen)
            self.hud.draw(self.screen, self.game_manager.get_game_state())

            # Draw the pause menu on top
            self.pause_menu.draw(self.screen)

        elif self.current_screen == "game_over":
            # Draw the game in the background
            self.game_manager.draw(self.screen)
            self.hud.draw(self.screen, self.game_manager.get_game_state())

            # Draw the game over menu on top
            self.game_over_menu.draw(self.screen)

        elif self.current_screen == "game":
            # Draw the game
            self.game_manager.draw(self.screen)

            # Draw tower placement preview
            if self.placing_tower:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[0] < SCREEN_WIDTH - SIDEBAR_WIDTH:
                    grid_pos = self.current_map.pixel_to_grid(mouse_pos)

                    # Draw placement indicator
                    color = (0, 255, 0, 128) if self.tower_placement_valid else (255, 0, 0, 128)
                    indicator = pygame.Surface((self.current_map.grid_size, self.current_map.grid_size), pygame.SRCALPHA)
                    indicator.fill(color)
                    self.screen.blit(indicator, (grid_pos[0] * self.current_map.grid_size, grid_pos[1] * self.current_map.grid_size))

            # Draw the HUD
            self.hud.draw(self.screen, self.game_manager.get_game_state())

        # Update the display
        pygame.display.flip()
