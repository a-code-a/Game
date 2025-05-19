"""
HUD (Heads-Up Display) for the Tower Defense Game
"""
import pygame
from typing import Dict, Any, Tuple, Optional, List

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SIDEBAR_WIDTH, TOWER_TYPES
from utils import draw_text
from towers.tower import Tower

class HUD:
    """Heads-Up Display for the game"""

    def __init__(self):
        """Initialize the HUD"""
        self.sidebar_rect = pygame.Rect(SCREEN_WIDTH - SIDEBAR_WIDTH, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT)
        self.tower_buttons = []
        self.selected_tower_type = None

        # Create tower buttons
        y_offset = 100
        for tower_type in TOWER_TYPES:
            button_rect = pygame.Rect(
                SCREEN_WIDTH - SIDEBAR_WIDTH + 10,
                y_offset,
                SIDEBAR_WIDTH - 20,
                60
            )
            self.tower_buttons.append({
                'type': tower_type,
                'rect': button_rect,
                'cost': TOWER_TYPES[tower_type]['cost']
            })
            y_offset += 70

    def draw(self, surface: pygame.Surface, game_state: Dict[str, Any]) -> None:
        """
        Draw the HUD

        Args:
            surface: Pygame surface to draw on
            game_state: Current game state
        """
        # Draw sidebar background
        pygame.draw.rect(surface, (50, 50, 50), self.sidebar_rect)
        pygame.draw.line(surface, (200, 200, 200),
                         (SCREEN_WIDTH - SIDEBAR_WIDTH, 0),
                         (SCREEN_WIDTH - SIDEBAR_WIDTH, SCREEN_HEIGHT), 2)

        # Draw game info
        draw_text(surface, f"Coins: {game_state['coins']}",
                  (SCREEN_WIDTH - SIDEBAR_WIDTH + 10, 10), (255, 255, 0))
        draw_text(surface, f"Lives: {game_state['lives']}",
                  (SCREEN_WIDTH - SIDEBAR_WIDTH + 10, 40), (255, 0, 0))
        draw_text(surface, f"Wave: {game_state['wave']}",
                  (SCREEN_WIDTH - SIDEBAR_WIDTH + 10, 70), (255, 255, 255))

        # Draw tower buttons
        for button in self.tower_buttons:
            # Button background
            color = (100, 100, 100)
            if button['type'] == self.selected_tower_type:
                color = (150, 150, 150)
            if game_state['coins'] < button['cost']:
                color = (80, 80, 80)  # Darker if can't afford

            pygame.draw.rect(surface, color, button['rect'])
            pygame.draw.rect(surface, (200, 200, 200), button['rect'], 2)

            # Tower name and cost
            draw_text(surface, button['type'].capitalize(),
                      (button['rect'].centerx, button['rect'].y + 15),
                      (255, 255, 255), centered=True)
            draw_text(surface, f"Cost: {button['cost']}",
                      (button['rect'].centerx, button['rect'].y + 40),
                      (255, 255, 0), centered=True)

        # Draw wave control
        wave_button_rect = pygame.Rect(
            SCREEN_WIDTH - SIDEBAR_WIDTH + 10,
            SCREEN_HEIGHT - 100,
            SIDEBAR_WIDTH - 20,
            40
        )

        if game_state['wave_in_progress']:
            pygame.draw.rect(surface, (100, 100, 100), wave_button_rect)
            draw_text(surface, f"Wave in progress",
                      (wave_button_rect.centerx, wave_button_rect.centery),
                      (255, 255, 255), centered=True)
        elif game_state['cooldown_remaining'] > 0:
            pygame.draw.rect(surface, (100, 100, 100), wave_button_rect)
            draw_text(surface, f"Next wave in: {game_state['cooldown_remaining']:.1f}s",
                      (wave_button_rect.centerx, wave_button_rect.centery),
                      (255, 255, 255), centered=True)
        else:
            pygame.draw.rect(surface, (0, 150, 0), wave_button_rect)
            draw_text(surface, "Start Next Wave",
                      (wave_button_rect.centerx, wave_button_rect.centery),
                      (255, 255, 255), centered=True)

        # Draw selected tower info
        if game_state['selected_tower']:
            self.draw_tower_info(surface, game_state['selected_tower'], game_state['coins'])

    def draw_tower_info(self, surface: pygame.Surface, tower: Tower, coins: int) -> None:
        """
        Draw information about the selected tower

        Args:
            surface: Pygame surface to draw on
            tower: Selected tower
            coins: Current coin count
        """
        info_rect = pygame.Rect(
            SCREEN_WIDTH - SIDEBAR_WIDTH + 10,
            SCREEN_HEIGHT - 250,
            SIDEBAR_WIDTH - 20,
            140
        )
        pygame.draw.rect(surface, (70, 70, 70), info_rect)
        pygame.draw.rect(surface, (200, 200, 200), info_rect, 2)

        # Tower stats
        draw_text(surface, f"{tower.tower_type.capitalize()}",
                  (info_rect.centerx, info_rect.y + 10),
                  (255, 255, 255), centered=True)
        draw_text(surface, f"Damage: {tower.damage:.1f}",
                  (info_rect.x + 10, info_rect.y + 35),
                  (255, 255, 255), font_size=18)
        draw_text(surface, f"Range: {tower.range:.1f}",
                  (info_rect.x + 10, info_rect.y + 55),
                  (255, 255, 255), font_size=18)
        draw_text(surface, f"Cooldown: {tower.cooldown:.1f}s",
                  (info_rect.x + 10, info_rect.y + 75),
                  (255, 255, 255), font_size=18)

        # Upgrade buttons
        upgrade_y = info_rect.y + 100
        for path in ['path1', 'path2']:
            if path in tower.upgrade_paths:
                upgrade_cost = tower.get_upgrade_cost(path)
                if upgrade_cost > 0:
                    upgrade_info = tower.get_upgrade_info(path)
                    button_rect = pygame.Rect(
                        SCREEN_WIDTH - SIDEBAR_WIDTH + 10 + (0 if path == 'path1' else SIDEBAR_WIDTH // 2 - 15),
                        upgrade_y,
                        SIDEBAR_WIDTH // 2 - 15,
                        30
                    )

                    # Button color based on affordability
                    color = (0, 150, 0) if coins >= upgrade_cost else (100, 100, 100)
                    pygame.draw.rect(surface, color, button_rect)
                    pygame.draw.rect(surface, (200, 200, 200), button_rect, 1)

                    draw_text(surface, f"{upgrade_info['name']}",
                              (button_rect.centerx, button_rect.y + 5),
                              (255, 255, 255), centered=True, font_size=14)
                    draw_text(surface, f"${upgrade_cost}",
                              (button_rect.centerx, button_rect.y + 20),
                              (255, 255, 0), centered=True, font_size=14)

        # Sell button
        sell_rect = pygame.Rect(
            SCREEN_WIDTH - SIDEBAR_WIDTH + 10,
            upgrade_y + 40,
            SIDEBAR_WIDTH - 20,
            30
        )
        pygame.draw.rect(surface, (150, 0, 0), sell_rect)
        pygame.draw.rect(surface, (200, 200, 200), sell_rect, 1)

        sell_value = tower.cost // 2
        draw_text(surface, f"Sell (${sell_value})",
                  (sell_rect.centerx, sell_rect.centery),
                  (255, 255, 255), centered=True)

    def handle_click(self, pos: Tuple[int, int], game_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle mouse click on the HUD

        Args:
            pos: Mouse position (x, y)
            game_state: Current game state

        Returns:
            Dictionary with action information
        """
        # Check tower buttons
        for button in self.tower_buttons:
            if button['rect'].collidepoint(pos):
                if game_state['coins'] >= button['cost']:
                    self.selected_tower_type = button['type']
                    return {'action': 'select_tower_type', 'tower_type': button['type']}
                else:
                    return {'action': 'not_enough_coins'}

        # Check wave button
        wave_button_rect = pygame.Rect(
            SCREEN_WIDTH - SIDEBAR_WIDTH + 10,
            SCREEN_HEIGHT - 100,
            SIDEBAR_WIDTH - 20,
            40
        )
        if wave_button_rect.collidepoint(pos) and not game_state['wave_in_progress'] and game_state['cooldown_remaining'] <= 0:
            return {'action': 'start_wave'}

        # Check upgrade buttons if a tower is selected
        if game_state['selected_tower']:
            tower = game_state['selected_tower']
            upgrade_y = SCREEN_HEIGHT - 250 + 100

            for path in ['path1', 'path2']:
                if path in tower.upgrade_paths:
                    upgrade_cost = tower.get_upgrade_cost(path)
                    if upgrade_cost > 0:
                        button_rect = pygame.Rect(
                            SCREEN_WIDTH - SIDEBAR_WIDTH + 10 + (0 if path == 'path1' else SIDEBAR_WIDTH // 2 - 15),
                            upgrade_y,
                            SIDEBAR_WIDTH // 2 - 15,
                            30
                        )
                        if button_rect.collidepoint(pos):
                            if game_state['coins'] >= upgrade_cost:
                                return {'action': 'upgrade_tower', 'path': path}
                            else:
                                return {'action': 'not_enough_coins'}

            # Check sell button
            sell_rect = pygame.Rect(
                SCREEN_WIDTH - SIDEBAR_WIDTH + 10,
                upgrade_y + 40,
                SIDEBAR_WIDTH - 20,
                30
            )
            if sell_rect.collidepoint(pos):
                return {'action': 'sell_tower'}

        return {'action': 'none'}
