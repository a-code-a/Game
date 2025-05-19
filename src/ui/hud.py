"""
HUD (Heads-Up Display) for the Tower Defense Game
"""
import pygame
from typing import Dict, Any, Tuple, Optional, List

from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, SIDEBAR_WIDTH, TOWER_TYPES,
    UI_BG, UI_PANEL, UI_BUTTON, UI_BUTTON_HOVER, UI_BUTTON_DISABLED,
    UI_TEXT, UI_HIGHLIGHT, UI_DANGER, UI_SUCCESS, UI_PATH1, UI_PATH2,
    COMIC_BLUE, COMIC_RED, COMIC_GREEN, COMIC_YELLOW, COMIC_ORANGE, COMIC_PURPLE,
    COMIC_DARK, COMIC_LIGHT
)
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
        # Draw sidebar background with comic-style gradient
        pygame.draw.rect(surface, UI_BG, self.sidebar_rect)

        # Add a comic-style border to the sidebar
        border_width = 4
        pygame.draw.rect(surface, COMIC_DARK, self.sidebar_rect, border_width)

        # Draw header section with comic-style background
        header_height = 90
        header_rect = pygame.Rect(
            SCREEN_WIDTH - SIDEBAR_WIDTH,
            0,
            SIDEBAR_WIDTH,
            header_height
        )
        pygame.draw.rect(surface, UI_PANEL, header_rect)
        pygame.draw.rect(surface, COMIC_DARK, header_rect, border_width)

        # Draw game info with comic-style text
        # Coins
        coin_icon_rect = pygame.Rect(
            SCREEN_WIDTH - SIDEBAR_WIDTH + 10,
            10,
            30,
            30
        )
        pygame.draw.circle(surface, COMIC_YELLOW, coin_icon_rect.center, 15)
        pygame.draw.circle(surface, COMIC_DARK, coin_icon_rect.center, 15, 2)

        draw_text(surface, f"Coins: {game_state['coins']}",
                  (SCREEN_WIDTH - SIDEBAR_WIDTH + 50, 15),
                  UI_HIGHLIGHT, font_size=24, bold=True, outline=True)

        # Lives
        heart_icon_rect = pygame.Rect(
            SCREEN_WIDTH - SIDEBAR_WIDTH + 10,
            45,
            30,
            30
        )
        # Draw a simple heart shape
        heart_points = [
            (heart_icon_rect.centerx, heart_icon_rect.y + 5),
            (heart_icon_rect.centerx + 10, heart_icon_rect.y + 15),
            (heart_icon_rect.centerx, heart_icon_rect.y + 25),
            (heart_icon_rect.centerx - 10, heart_icon_rect.y + 15)
        ]
        pygame.draw.polygon(surface, COMIC_RED, heart_points)
        pygame.draw.polygon(surface, COMIC_DARK, heart_points, 2)

        draw_text(surface, f"Lives: {game_state['lives']}",
                  (SCREEN_WIDTH - SIDEBAR_WIDTH + 50, 50),
                  COMIC_RED, font_size=24, bold=True, outline=True)

        # Wave
        draw_text(surface, f"Wave: {game_state['wave']}",
                  (SCREEN_WIDTH - SIDEBAR_WIDTH + 10, 75),
                  UI_TEXT, font_size=20, bold=True, outline=True)

        # Draw tower buttons with comic-style
        for i, button in enumerate(self.tower_buttons):
            # Button background with comic-style
            if button['type'] == self.selected_tower_type:
                color = UI_BUTTON_HOVER
                border_color = COMIC_YELLOW
            elif game_state['coins'] < button['cost']:
                color = UI_BUTTON_DISABLED  # Darker if can't afford
                border_color = COMIC_DARK
            else:
                color = UI_BUTTON
                border_color = COMIC_DARK

            # Draw button with rounded corners and 3D effect
            button_rect = button['rect']

            # Shadow effect (3D)
            shadow_rect = button_rect.copy()
            shadow_rect.x += 3
            shadow_rect.y += 3
            pygame.draw.rect(surface, COMIC_DARK, shadow_rect, border_radius=10)

            # Main button
            pygame.draw.rect(surface, color, button_rect, border_radius=10)
            pygame.draw.rect(surface, border_color, button_rect, 3, border_radius=10)

            # Tower icon (placeholder - could be replaced with actual tower images)
            icon_colors = {
                'basic': COMIC_BLUE,
                'sniper': COMIC_GREEN,
                'area': COMIC_ORANGE,
                'support': COMIC_PURPLE
            }
            icon_color = icon_colors.get(button['type'], COMIC_BLUE)
            icon_rect = pygame.Rect(
                button_rect.x + 10,
                button_rect.y + 15,
                30,
                30
            )
            pygame.draw.rect(surface, icon_color, icon_rect, border_radius=5)
            pygame.draw.rect(surface, COMIC_DARK, icon_rect, 2, border_radius=5)

            # Tower name with comic-style text
            draw_text(surface, button['type'].capitalize(),
                      (button_rect.x + 50, button_rect.y + 15),
                      UI_TEXT, font_size=20, bold=True, outline=True)

            # Cost with comic-style text
            draw_text(surface, f"Cost: {button['cost']}",
                      (button_rect.x + 50, button_rect.y + 40),
                      UI_HIGHLIGHT, font_size=18, bold=True, outline=True)

        # Draw wave control button with comic-style
        wave_button_rect = pygame.Rect(
            SCREEN_WIDTH - SIDEBAR_WIDTH + 10,
            SCREEN_HEIGHT - 60,  # Moved up to avoid overlap
            SIDEBAR_WIDTH - 20,
            40
        )

        # Shadow effect
        shadow_rect = wave_button_rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        pygame.draw.rect(surface, COMIC_DARK, shadow_rect, border_radius=10)

        if game_state['wave_in_progress']:
            # Wave in progress - disabled button
            pygame.draw.rect(surface, UI_BUTTON_DISABLED, wave_button_rect, border_radius=10)
            pygame.draw.rect(surface, COMIC_DARK, wave_button_rect, 3, border_radius=10)
            draw_text(surface, f"Wave in progress",
                      (wave_button_rect.centerx, wave_button_rect.centery),
                      UI_TEXT, font_size=18, bold=True, centered=True, outline=True)
        elif game_state['cooldown_remaining'] > 0:
            # Cooldown - countdown button
            pygame.draw.rect(surface, UI_BUTTON_DISABLED, wave_button_rect, border_radius=10)
            pygame.draw.rect(surface, COMIC_DARK, wave_button_rect, 3, border_radius=10)
            draw_text(surface, f"Next wave in: {game_state['cooldown_remaining']:.1f}s",
                      (wave_button_rect.centerx, wave_button_rect.centery),
                      UI_TEXT, font_size=18, bold=True, centered=True, outline=True)
        else:
            # Ready - active button
            pygame.draw.rect(surface, UI_SUCCESS, wave_button_rect, border_radius=10)
            pygame.draw.rect(surface, COMIC_DARK, wave_button_rect, 3, border_radius=10)
            draw_text(surface, "Start Next Wave",
                      (wave_button_rect.centerx, wave_button_rect.centery),
                      UI_TEXT, font_size=18, bold=True, centered=True, outline=True)

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
        # Main info panel with comic-style
        info_panel_height = 150
        info_rect = pygame.Rect(
            SCREEN_WIDTH - SIDEBAR_WIDTH + 10,
            SCREEN_HEIGHT - 350,  # Moved up to avoid overlap
            SIDEBAR_WIDTH - 20,
            info_panel_height
        )

        # Shadow effect
        shadow_rect = info_rect.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        pygame.draw.rect(surface, COMIC_DARK, shadow_rect, border_radius=10)

        # Main panel
        pygame.draw.rect(surface, UI_PANEL, info_rect, border_radius=10)
        pygame.draw.rect(surface, COMIC_DARK, info_rect, 3, border_radius=10)

        # Tower icon and name in a comic-style header
        icon_colors = {
            'basic': COMIC_BLUE,
            'sniper': COMIC_GREEN,
            'area': COMIC_ORANGE,
            'support': COMIC_PURPLE
        }
        icon_color = icon_colors.get(tower.tower_type, COMIC_BLUE)

        # Tower header
        header_rect = pygame.Rect(
            info_rect.x,
            info_rect.y,
            info_rect.width,
            40
        )
        pygame.draw.rect(surface, icon_color, header_rect, border_radius=10)
        pygame.draw.rect(surface, COMIC_DARK, header_rect, 3, border_radius=10)

        # Tower name with comic-style text
        draw_text(surface, f"{tower.tower_type.capitalize()} Tower",
                  (header_rect.centerx, header_rect.centery),
                  UI_TEXT, font_size=22, bold=True, centered=True, outline=True)

        # Tower stats with comic-style icons
        stats_y = info_rect.y + 50

        # Damage stat
        damage_icon_rect = pygame.Rect(info_rect.x + 10, stats_y, 20, 20)
        pygame.draw.rect(surface, COMIC_RED, damage_icon_rect, border_radius=3)
        pygame.draw.rect(surface, COMIC_DARK, damage_icon_rect, 2, border_radius=3)
        draw_text(surface, f"DMG: {tower.damage:.1f}",
                  (info_rect.x + 40, stats_y + 2),
                  UI_TEXT, font_size=16, bold=True, outline=True)

        # Range stat
        range_icon_rect = pygame.Rect(info_rect.x + 110, stats_y, 20, 20)
        pygame.draw.circle(surface, COMIC_BLUE, range_icon_rect.center, 10)
        pygame.draw.circle(surface, COMIC_DARK, range_icon_rect.center, 10, 2)
        draw_text(surface, f"RNG: {tower.range:.0f}",
                  (info_rect.x + 140, stats_y + 2),
                  UI_TEXT, font_size=16, bold=True, outline=True)

        # Cooldown stat
        cooldown_y = stats_y + 25
        cooldown_icon_rect = pygame.Rect(info_rect.x + 10, cooldown_y, 20, 20)
        pygame.draw.polygon(surface, COMIC_GREEN, [
            (cooldown_icon_rect.x, cooldown_icon_rect.y + 10),
            (cooldown_icon_rect.x + 20, cooldown_icon_rect.y),
            (cooldown_icon_rect.x + 20, cooldown_icon_rect.y + 20)
        ])
        pygame.draw.polygon(surface, COMIC_DARK, [
            (cooldown_icon_rect.x, cooldown_icon_rect.y + 10),
            (cooldown_icon_rect.x + 20, cooldown_icon_rect.y),
            (cooldown_icon_rect.x + 20, cooldown_icon_rect.y + 20)
        ], 2)
        draw_text(surface, f"SPD: {1/tower.cooldown:.1f}/s",
                  (info_rect.x + 40, cooldown_y + 2),
                  UI_TEXT, font_size=16, bold=True, outline=True)

        # Special abilities with comic-style badges
        special_abilities = []
        special_colors = []

        if tower.splash_radius > 0:
            special_abilities.append(f"Splash: {tower.splash_radius:.0f}")
            special_colors.append(COMIC_ORANGE)
        if tower.buff_multiplier > 1.0:
            special_abilities.append(f"Buff: x{tower.buff_multiplier:.1f}")
            special_colors.append(COMIC_PURPLE)
        if tower.adds_burning:
            special_abilities.append(f"Burn: x{tower.burning_damage_multiplier:.1f}")
            special_colors.append(COMIC_RED)
        if tower.adds_critical:
            special_abilities.append(f"Crit: {int(tower.critical_chance * 100)}%")
            special_colors.append(COMIC_YELLOW)
        if tower.adds_special_ability:
            special_abilities.append("Special")
            special_colors.append(COMIC_PURPLE)

        if special_abilities:
            special_y = cooldown_y + 25
            for i, (ability, color) in enumerate(zip(special_abilities, special_colors)):
                # Create a comic-style badge for each ability
                badge_width = len(ability) * 8 + 20
                badge_rect = pygame.Rect(
                    info_rect.x + 10 + (i * (badge_width + 5)),
                    special_y,
                    badge_width,
                    22
                )

                # Don't draw if it would go outside the panel
                if badge_rect.right > info_rect.right - 5:
                    break

                pygame.draw.rect(surface, color, badge_rect, border_radius=8)
                pygame.draw.rect(surface, COMIC_DARK, badge_rect, 2, border_radius=8)
                draw_text(surface, ability,
                          (badge_rect.centerx, badge_rect.centery),
                          UI_TEXT, font_size=14, bold=True, centered=True, outline=True)

        # Upgrade paths section
        upgrade_section_rect = pygame.Rect(
            SCREEN_WIDTH - SIDEBAR_WIDTH + 10,
            info_rect.bottom + 10,
            SIDEBAR_WIDTH - 20,
            160  # Height for two upgrade paths
        )

        # Shadow effect
        shadow_rect = upgrade_section_rect.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        pygame.draw.rect(surface, COMIC_DARK, shadow_rect, border_radius=10)

        # Main panel
        pygame.draw.rect(surface, UI_PANEL, upgrade_section_rect, border_radius=10)
        pygame.draw.rect(surface, COMIC_DARK, upgrade_section_rect, 3, border_radius=10)

        # Upgrade paths header
        header_rect = pygame.Rect(
            upgrade_section_rect.x,
            upgrade_section_rect.y,
            upgrade_section_rect.width,
            30
        )
        pygame.draw.rect(surface, COMIC_DARK, header_rect, border_radius=10)

        draw_text(surface, "Upgrade Paths",
                  (header_rect.centerx, header_rect.centery),
                  UI_TEXT, font_size=18, bold=True, centered=True, outline=True)

        # Upgrade buttons with comic-style
        upgrade_y = upgrade_section_rect.y + 40
        path_height = 55

        for path_idx, path in enumerate(['path1', 'path2']):
            path_name = "Path 1: Speed/Range" if path == 'path1' else "Path 2: Damage/Special"
            path_color = UI_PATH1 if path == 'path1' else UI_PATH2

            # Path header with current level
            level = tower.upgrades.get(path, 0)
            max_level = len(tower.upgrade_paths.get(path, [])) if path in tower.upgrade_paths else 0

            # Path header background
            path_header_rect = pygame.Rect(
                upgrade_section_rect.x + 5,
                upgrade_y + path_idx * path_height,
                upgrade_section_rect.width - 10,
                20
            )
            pygame.draw.rect(surface, path_color, path_header_rect, border_radius=5)
            pygame.draw.rect(surface, COMIC_DARK, path_header_rect, 2, border_radius=5)

            # Path name and level
            draw_text(surface, f"{path_name} ({level}/{max_level})",
                      (path_header_rect.centerx, path_header_rect.centery),
                      UI_TEXT, font_size=14, bold=True, centered=True, outline=True)

            # Draw upgrade button if available
            if path in tower.upgrade_paths:
                upgrade_cost = tower.get_upgrade_cost(path)
                if upgrade_cost > 0:
                    upgrade_info = tower.get_upgrade_info(path)
                    button_rect = pygame.Rect(
                        upgrade_section_rect.x + 5,
                        upgrade_y + 25 + path_idx * path_height,
                        upgrade_section_rect.width - 10,
                        25
                    )

                    # Shadow effect
                    shadow_rect = button_rect.copy()
                    shadow_rect.x += 2
                    shadow_rect.y += 2
                    pygame.draw.rect(surface, COMIC_DARK, shadow_rect, border_radius=5)

                    # Button color based on affordability
                    color = UI_SUCCESS if coins >= upgrade_cost else UI_BUTTON_DISABLED
                    pygame.draw.rect(surface, color, button_rect, border_radius=5)
                    pygame.draw.rect(surface, path_color, button_rect, 2, border_radius=5)

                    # Upgrade name and cost
                    name_text = f"{upgrade_info['name']} (${upgrade_cost})"
                    draw_text(surface, name_text,
                              (button_rect.centerx, button_rect.centery),
                              UI_TEXT, font_size=14, bold=True, centered=True, outline=True)

                    # Draw description tooltip on hover
                    mouse_pos = pygame.mouse.get_pos()
                    if button_rect.collidepoint(mouse_pos) and 'description' in upgrade_info:
                        # Comic-style speech bubble tooltip
                        tooltip_width = len(upgrade_info['description']) * 6 + 20
                        tooltip_height = 30
                        tooltip_rect = pygame.Rect(
                            mouse_pos[0] - tooltip_width // 2,
                            mouse_pos[1] - tooltip_height - 15,
                            tooltip_width,
                            tooltip_height
                        )

                        # Keep tooltip on screen
                        if tooltip_rect.right > SCREEN_WIDTH:
                            tooltip_rect.right = SCREEN_WIDTH - 5
                        if tooltip_rect.left < 0:
                            tooltip_rect.left = 5
                        if tooltip_rect.top < 0:
                            tooltip_rect.top = 5

                        # Draw speech bubble
                        pygame.draw.rect(surface, UI_PANEL, tooltip_rect, border_radius=8)
                        pygame.draw.rect(surface, COMIC_DARK, tooltip_rect, 2, border_radius=8)

                        # Draw little triangle pointer
                        pointer_points = [
                            (tooltip_rect.centerx - 10, tooltip_rect.bottom),
                            (tooltip_rect.centerx + 10, tooltip_rect.bottom),
                            (tooltip_rect.centerx, tooltip_rect.bottom + 10)
                        ]
                        pygame.draw.polygon(surface, UI_PANEL, pointer_points)
                        pygame.draw.polygon(surface, COMIC_DARK, pointer_points, 2)

                        draw_text(surface, upgrade_info['description'],
                                  (tooltip_rect.centerx, tooltip_rect.centery),
                                  UI_TEXT, font_size=14, bold=True, centered=True, outline=True)
                else:
                    # Path is maxed out
                    maxed_rect = pygame.Rect(
                        upgrade_section_rect.x + 5,
                        upgrade_y + 25 + path_idx * path_height,
                        upgrade_section_rect.width - 10,
                        25
                    )
                    pygame.draw.rect(surface, UI_BUTTON_DISABLED, maxed_rect, border_radius=5)
                    pygame.draw.rect(surface, path_color, maxed_rect, 2, border_radius=5)
                    draw_text(surface, "Maxed Out",
                              (maxed_rect.centerx, maxed_rect.centery),
                              UI_TEXT, font_size=14, bold=True, centered=True, outline=True)
            elif level > 0:
                # Path is locked because the other path is upgraded
                locked_rect = pygame.Rect(
                    upgrade_section_rect.x + 5,
                    upgrade_y + 25 + path_idx * path_height,
                    upgrade_section_rect.width - 10,
                    25
                )
                pygame.draw.rect(surface, UI_BUTTON_DISABLED, locked_rect, border_radius=5)
                pygame.draw.rect(surface, UI_DANGER, locked_rect, 2, border_radius=5)
                draw_text(surface, "Locked",
                          (locked_rect.centerx, locked_rect.centery),
                          UI_TEXT, font_size=14, bold=True, centered=True, outline=True)

        # Sell button with comic-style
        sell_rect = pygame.Rect(
            SCREEN_WIDTH - SIDEBAR_WIDTH + 10,
            upgrade_section_rect.bottom + 10,
            SIDEBAR_WIDTH - 20,
            35
        )

        # Shadow effect
        shadow_rect = sell_rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        pygame.draw.rect(surface, COMIC_DARK, shadow_rect, border_radius=8)

        # Main button
        pygame.draw.rect(surface, UI_DANGER, sell_rect, border_radius=8)
        pygame.draw.rect(surface, COMIC_DARK, sell_rect, 3, border_radius=8)

        # Sell text with comic-style
        sell_value = tower.cost // 2
        draw_text(surface, f"Sell Tower (${sell_value})",
                  (sell_rect.centerx, sell_rect.centery),
                  UI_TEXT, font_size=18, bold=True, centered=True, outline=True)

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

        # Check wave button (updated position to match the draw method)
        wave_button_rect = pygame.Rect(
            SCREEN_WIDTH - SIDEBAR_WIDTH + 10,
            SCREEN_HEIGHT - 60,  # Moved up to avoid overlap
            SIDEBAR_WIDTH - 20,
            40
        )
        if wave_button_rect.collidepoint(pos) and not game_state['wave_in_progress'] and game_state['cooldown_remaining'] <= 0:
            return {'action': 'start_wave'}

        # Check upgrade buttons if a tower is selected
        if game_state['selected_tower']:
            tower = game_state['selected_tower']

            # Calculate panel positions based on our new layout
            info_panel_height = 150
            info_rect_y = SCREEN_HEIGHT - 350

            # Upgrade section position
            upgrade_section_rect = pygame.Rect(
                SCREEN_WIDTH - SIDEBAR_WIDTH + 10,
                info_rect_y + info_panel_height + 10,
                SIDEBAR_WIDTH - 20,
                160
            )

            upgrade_y = upgrade_section_rect.y + 40
            path_height = 55

            # Check upgrade buttons for each path
            for path_idx, path in enumerate(['path1', 'path2']):
                if path in tower.upgrade_paths:
                    upgrade_cost = tower.get_upgrade_cost(path)
                    if upgrade_cost > 0:
                        button_rect = pygame.Rect(
                            upgrade_section_rect.x + 5,
                            upgrade_y + 25 + path_idx * path_height,
                            upgrade_section_rect.width - 10,
                            25
                        )
                        if button_rect.collidepoint(pos):
                            if game_state['coins'] >= upgrade_cost:
                                return {'action': 'upgrade_tower', 'path': path}
                            else:
                                return {'action': 'not_enough_coins'}

            # Check sell button
            sell_rect = pygame.Rect(
                SCREEN_WIDTH - SIDEBAR_WIDTH + 10,
                upgrade_section_rect.bottom + 10,
                SIDEBAR_WIDTH - 20,
                35
            )
            if sell_rect.collidepoint(pos):
                return {'action': 'sell_tower'}

        return {'action': 'none'}
