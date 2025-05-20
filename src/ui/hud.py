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
from utils import draw_text, draw_aa_circle, FloatingText
from towers.tower import Tower, TARGET_CLOSEST, TARGET_FIRST, TARGET_LAST, TARGET_RANDOM

class HUD:
    """Heads-Up Display for the game"""

    def __init__(self):
        """Initialize the HUD"""
        self.sidebar_rect = pygame.Rect(SCREEN_WIDTH - SIDEBAR_WIDTH, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT)
        self.tower_buttons = []
        self.selected_tower_type = None

        # Define sections for better organization
        self.header_height = 90
        self.tower_section_y = self.header_height + 10
        self.tower_section_height = 240  # Adjusted height for tower buttons

        # Create menu button in top left corner
        self.menu_button_size = 40
        self.menu_button_rect = pygame.Rect(
            10,  # Left margin
            10,  # Top margin
            self.menu_button_size,
            self.menu_button_size
        )

        # Menu dropdown state
        self.menu_open = False
        self.menu_options = [
            {"text": "Settings", "action": "settings"},
            {"text": "Main Menu", "action": "main_menu"},
            {"text": "Resume", "action": "resume"}
        ]
        self.menu_option_height = 35
        self.menu_width = 150

        # Create tower buttons - more compact layout
        y_offset = self.tower_section_y + 30  # Start after section header
        button_height = 50  # Reduced height
        button_spacing = 10  # Space between buttons

        for tower_type in TOWER_TYPES:
            button_rect = pygame.Rect(
                SCREEN_WIDTH - SIDEBAR_WIDTH + 10,
                y_offset,
                SIDEBAR_WIDTH - 20,
                button_height
            )
            self.tower_buttons.append({
                'type': tower_type,
                'rect': button_rect,
                'cost': TOWER_TYPES[tower_type]['cost']
            })
            y_offset += button_height + button_spacing

        self.floating_texts = []  # For floating damage numbers and effects

    def draw(self, surface: pygame.Surface, game_state: Dict[str, Any]) -> None:
        """
        Draw the HUD

        Args:
            surface: Pygame surface to draw on
            game_state: Current game state
        """
        # Draw menu button in top left corner
        self._draw_menu_button(surface)

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

        # Only show tower selection if no tower is selected
        if not game_state['selected_tower']:
            # Draw tower selection section header
            tower_section_header = pygame.Rect(
                SCREEN_WIDTH - SIDEBAR_WIDTH + 10,
                self.tower_section_y,
                SIDEBAR_WIDTH - 20,
                25
            )
            pygame.draw.rect(surface, COMIC_DARK, tower_section_header, border_radius=8)
            draw_text(surface, "Select Tower",
                      (tower_section_header.centerx, tower_section_header.centery),
                      UI_TEXT, font_size=16, bold=True, centered=True, outline=True)

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
                shadow_rect.x += 2
                shadow_rect.y += 2
                pygame.draw.rect(surface, COMIC_DARK, shadow_rect, border_radius=8)

                # Main button
                pygame.draw.rect(surface, color, button_rect, border_radius=8)
                pygame.draw.rect(surface, border_color, button_rect, 2, border_radius=8)

                # Tower icon (placeholder - could be replaced with actual tower images)
                icon_colors = {
                    'basic': COMIC_BLUE,
                    'sniper': COMIC_GREEN,
                    'area': COMIC_ORANGE,
                    'support': COMIC_PURPLE
                }
                icon_color = icon_colors.get(button['type'], COMIC_BLUE)
                icon_rect = pygame.Rect(
                    button_rect.x + 8,
                    button_rect.y + 10,
                    30,
                    30
                )
                pygame.draw.rect(surface, icon_color, icon_rect, border_radius=5)
                pygame.draw.rect(surface, COMIC_DARK, icon_rect, 2, border_radius=5)

                # Tower name and cost in a more compact layout
                draw_text(surface, button['type'].capitalize(),
                          (button_rect.x + 45, button_rect.y + 12),
                          UI_TEXT, font_size=16, bold=True, outline=True)

                # Cost with coin icon
                coin_icon_size = 14
                coin_icon_rect = pygame.Rect(
                    button_rect.x + 45,
                    button_rect.y + 30,
                    coin_icon_size,
                    coin_icon_size
                )
                pygame.draw.circle(surface, COMIC_YELLOW, coin_icon_rect.center, coin_icon_size/2)
                pygame.draw.circle(surface, COMIC_DARK, coin_icon_rect.center, coin_icon_size/2, 1)

                draw_text(surface, f"{button['cost']}",
                          (button_rect.x + 65, button_rect.y + 30),
                          UI_HIGHLIGHT, font_size=16, bold=True, outline=True)

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

        # Draw floating texts on top of everything
        for ft in self.floating_texts:
            ft.draw(surface)

    def draw_tower_info(self, surface: pygame.Surface, tower: Tower, coins: int) -> None:
        """
        Draw information about the selected tower
        Optimized: Avoid unnecessary work and only update tooltips on hover.

        Args:
            surface: Pygame surface to draw on
            tower: Selected tower
            coins: Current coin count
        """
        # Calculate positions - when a tower is selected, we use the full sidebar
        # Tower info panel starts right after the header
        info_panel_y = self.header_height + 10
        info_panel_height = 120  # Reduced height

        # Main info panel with comic-style
        info_rect = pygame.Rect(
            SCREEN_WIDTH - SIDEBAR_WIDTH + 10,
            info_panel_y,
            SIDEBAR_WIDTH - 20,
            info_panel_height
        )

        # Shadow effect
        shadow_rect = info_rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        pygame.draw.rect(surface, COMIC_DARK, shadow_rect, border_radius=8)

        # Main panel
        pygame.draw.rect(surface, UI_PANEL, info_rect, border_radius=8)
        pygame.draw.rect(surface, COMIC_DARK, info_rect, 2, border_radius=8)

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
            30  # Reduced height
        )
        pygame.draw.rect(surface, icon_color, header_rect, border_radius=8)
        pygame.draw.rect(surface, COMIC_DARK, header_rect, 2, border_radius=8)

        # Tower name with comic-style text
        draw_text(surface, f"{tower.tower_type.capitalize()} Tower",
                  (header_rect.centerx, header_rect.centery),
                  UI_TEXT, font_size=18, bold=True, centered=True, outline=True)

        # Tower stats with comic-style icons in a grid layout
        # First row
        stats_y = info_rect.y + 40
        col_width = 85  # Width for each stat column

        # Damage stat
        damage_icon_rect = pygame.Rect(info_rect.x + 10, stats_y, 16, 16)
        pygame.draw.rect(surface, COMIC_RED, damage_icon_rect, border_radius=3)
        pygame.draw.rect(surface, COMIC_DARK, damage_icon_rect, 1, border_radius=3)
        draw_text(surface, f"DMG: {tower.damage:.1f}",
                  (info_rect.x + 32, stats_y + 1),
                  UI_TEXT, font_size=14, bold=True, outline=False)

        # Range stat
        range_icon_rect = pygame.Rect(info_rect.x + col_width + 10, stats_y, 16, 16)
        pygame.draw.circle(surface, COMIC_BLUE, range_icon_rect.center, 8)
        pygame.draw.circle(surface, COMIC_DARK, range_icon_rect.center, 8, 1)
        draw_text(surface, f"RNG: {tower.range:.0f}",
                  (info_rect.x + col_width + 32, stats_y + 1),
                  UI_TEXT, font_size=14, bold=True, outline=False)

        # Second row - Cooldown stat
        cooldown_y = stats_y + 25
        cooldown_icon_rect = pygame.Rect(info_rect.x + 10, cooldown_y, 16, 16)
        pygame.draw.polygon(surface, COMIC_GREEN, [
            (cooldown_icon_rect.x, cooldown_icon_rect.y + 8),
            (cooldown_icon_rect.x + 16, cooldown_icon_rect.y),
            (cooldown_icon_rect.x + 16, cooldown_icon_rect.y + 16)
        ])
        pygame.draw.polygon(surface, COMIC_DARK, [
            (cooldown_icon_rect.x, cooldown_icon_rect.y + 8),
            (cooldown_icon_rect.x + 16, cooldown_icon_rect.y),
            (cooldown_icon_rect.x + 16, cooldown_icon_rect.y + 16)
        ], 1)
        draw_text(surface, f"SPD: {1/tower.cooldown:.1f}/s",
                  (info_rect.x + 32, cooldown_y + 1),
                  UI_TEXT, font_size=14, bold=True, outline=False)

        # Special abilities with compact badges
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

        # Draw special abilities in a more compact way
        if special_abilities:
            special_y = cooldown_y + 25
            draw_text(surface, "Special:",
                      (info_rect.x + 10, special_y + 1),
                      UI_TEXT, font_size=14, bold=True, outline=True)

            badge_x = info_rect.x + 70
            badge_y = special_y
            badge_height = 18

            for i, (ability, color) in enumerate(zip(special_abilities, special_colors)):
                # Create smaller badges for each ability
                badge_width = min(len(ability) * 6 + 10, 80)

                # If we would go off the panel, move to next row
                if badge_x + badge_width > info_rect.right - 5:
                    badge_x = info_rect.x + 70
                    badge_y += badge_height + 2

                    # If we're out of vertical space, stop drawing
                    if badge_y + badge_height > info_rect.bottom - 5:
                        break

                badge_rect = pygame.Rect(
                    badge_x,
                    badge_y,
                    badge_width,
                    badge_height
                )

                pygame.draw.rect(surface, color, badge_rect, border_radius=5)
                pygame.draw.rect(surface, COMIC_DARK, badge_rect, 1, border_radius=5)
                draw_text(surface, ability,
                          (badge_rect.centerx, badge_rect.centery),
                          UI_TEXT, font_size=12, bold=True, centered=True, outline=True)

                badge_x += badge_width + 5

        # Upgrade paths section - positioned after tower info
        upgrade_section_rect = pygame.Rect(
            SCREEN_WIDTH - SIDEBAR_WIDTH + 10,
            info_rect.bottom + 10,
            SIDEBAR_WIDTH - 20,
            140  # Reduced height for two upgrade paths
        )

        # Shadow effect
        shadow_rect = upgrade_section_rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        pygame.draw.rect(surface, COMIC_DARK, shadow_rect, border_radius=8)

        # Main panel
        pygame.draw.rect(surface, UI_PANEL, upgrade_section_rect, border_radius=8)
        pygame.draw.rect(surface, COMIC_DARK, upgrade_section_rect, 2, border_radius=8)

        # Upgrade paths header
        header_rect = pygame.Rect(
            upgrade_section_rect.x,
            upgrade_section_rect.y,
            upgrade_section_rect.width,
            25  # Reduced height
        )
        pygame.draw.rect(surface, COMIC_DARK, header_rect, border_radius=8)

        draw_text(surface, "Upgrade Paths",
                  (header_rect.centerx, header_rect.centery),
                  UI_TEXT, font_size=16, bold=True, centered=True, outline=True)

        # Upgrade buttons with comic-style - more compact layout
        upgrade_y = upgrade_section_rect.y + 30  # Reduced spacing
        path_height = 50  # Reduced height

        for path_idx, path in enumerate(['path1', 'path2']):
            path_name = "Path 1: Speed/Range" if path == 'path1' else "Path 2: Damage/Special"
            path_color = UI_PATH1 if path == 'path1' else UI_PATH2

            # Path header with current level
            level = tower.upgrades.get(path, 0)
            max_level = len(tower.upgrade_paths.get(path, [])) if path in tower.upgrade_paths else 0

            # Path header background - more compact
            path_header_rect = pygame.Rect(
                upgrade_section_rect.x + 5,
                upgrade_y + path_idx * path_height,
                upgrade_section_rect.width - 10,
                18  # Reduced height
            )
            pygame.draw.rect(surface, path_color, path_header_rect, border_radius=5)
            pygame.draw.rect(surface, COMIC_DARK, path_header_rect, 1, border_radius=5)

            # Path name and level - smaller font
            draw_text(surface, f"{path_name} ({level}/{max_level})",
                      (path_header_rect.centerx, path_header_rect.centery),
                      UI_TEXT, font_size=12, bold=True, centered=True, outline=True)

            # Draw upgrade button if available
            if path in tower.upgrade_paths:
                upgrade_cost = tower.get_upgrade_cost(path)
                if upgrade_cost > 0:
                    upgrade_info = tower.get_upgrade_info(path)
                    button_rect = pygame.Rect(
                        upgrade_section_rect.x + 5,
                        upgrade_y + 22 + path_idx * path_height,  # Adjusted position
                        upgrade_section_rect.width - 10,
                        22  # Reduced height
                    )

                    # Shadow effect - smaller
                    shadow_rect = button_rect.copy()
                    shadow_rect.x += 2
                    shadow_rect.y += 2
                    pygame.draw.rect(surface, COMIC_DARK, shadow_rect, border_radius=5)

                    # Button color based on affordability
                    color = UI_SUCCESS if coins >= upgrade_cost else UI_BUTTON_DISABLED
                    pygame.draw.rect(surface, color, button_rect, border_radius=5)
                    pygame.draw.rect(surface, path_color, button_rect, 1, border_radius=5)

                    # Upgrade name and cost - more compact with coin icon
                    coin_icon_size = 12
                    coin_icon_rect = pygame.Rect(
                        button_rect.x + 5,
                        button_rect.centery - coin_icon_size//2,
                        coin_icon_size,
                        coin_icon_size
                    )
                    pygame.draw.circle(surface, COMIC_YELLOW, coin_icon_rect.center, coin_icon_size/2)
                    pygame.draw.circle(surface, COMIC_DARK, coin_icon_rect.center, coin_icon_size/2, 1)

                    # Upgrade name with cost
                    name_text = f"{upgrade_info['name']} (${upgrade_cost})"
                    draw_text(surface, name_text,
                              (button_rect.centerx + 5, button_rect.centery),
                              UI_TEXT, font_size=12, bold=True, centered=True, outline=True)

                    # Draw description tooltip on hover
                    mouse_pos = pygame.mouse.get_pos()
                    if button_rect.collidepoint(mouse_pos) and 'description' in upgrade_info:
                        # Comic-style speech bubble tooltip
                        tooltip_width = min(len(upgrade_info['description']) * 5 + 20, 180)
                        tooltip_height = 25
                        tooltip_rect = pygame.Rect(
                            mouse_pos[0] - tooltip_width // 2,
                            mouse_pos[1] - tooltip_height - 10,
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
                        pygame.draw.rect(surface, UI_PANEL, tooltip_rect, border_radius=5)
                        pygame.draw.rect(surface, COMIC_DARK, tooltip_rect, 1, border_radius=5)

                        # Draw little triangle pointer
                        pointer_points = [
                            (tooltip_rect.centerx - 8, tooltip_rect.bottom),
                            (tooltip_rect.centerx + 8, tooltip_rect.bottom),
                            (tooltip_rect.centerx, tooltip_rect.bottom + 8)
                        ]
                        pygame.draw.polygon(surface, UI_PANEL, pointer_points)
                        pygame.draw.polygon(surface, COMIC_DARK, pointer_points, 1)

                        draw_text(surface, upgrade_info['description'],
                                  (tooltip_rect.centerx, tooltip_rect.centery),
                                  UI_TEXT, font_size=12, bold=True, centered=True, outline=True)
                else:
                    # Path is maxed out
                    maxed_rect = pygame.Rect(
                        upgrade_section_rect.x + 5,
                        upgrade_y + 22 + path_idx * path_height,
                        upgrade_section_rect.width - 10,
                        22
                    )
                    pygame.draw.rect(surface, UI_BUTTON_DISABLED, maxed_rect, border_radius=5)
                    pygame.draw.rect(surface, path_color, maxed_rect, 1, border_radius=5)
                    draw_text(surface, "Maxed Out",
                              (maxed_rect.centerx, maxed_rect.centery),
                              UI_TEXT, font_size=12, bold=True, centered=True, outline=True)
            elif level > 0:
                # Path is locked because the other path is upgraded
                locked_rect = pygame.Rect(
                    upgrade_section_rect.x + 5,
                    upgrade_y + 22 + path_idx * path_height,
                    upgrade_section_rect.width - 10,
                    22
                )
                pygame.draw.rect(surface, UI_BUTTON_DISABLED, locked_rect, border_radius=5)
                pygame.draw.rect(surface, UI_DANGER, locked_rect, 1, border_radius=5)
                draw_text(surface, "Locked",
                          (locked_rect.centerx, locked_rect.centery),
                          UI_TEXT, font_size=12, bold=True, centered=True, outline=True)

        # Targeting options section - positioned after upgrade section
        targeting_section_rect = pygame.Rect(
            SCREEN_WIDTH - SIDEBAR_WIDTH + 10,
            upgrade_section_rect.bottom + 10,
            SIDEBAR_WIDTH - 20,
            90  # Height for targeting options
        )

        # Shadow effect
        shadow_rect = targeting_section_rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        pygame.draw.rect(surface, COMIC_DARK, shadow_rect, border_radius=8)

        # Main panel
        pygame.draw.rect(surface, UI_PANEL, targeting_section_rect, border_radius=8)
        pygame.draw.rect(surface, COMIC_DARK, targeting_section_rect, 2, border_radius=8)

        # Targeting header
        header_rect = pygame.Rect(
            targeting_section_rect.x,
            targeting_section_rect.y,
            targeting_section_rect.width,
            25  # Header height
        )
        pygame.draw.rect(surface, COMIC_DARK, header_rect, border_radius=8)

        draw_text(surface, "Targeting Options",
                  (header_rect.centerx, header_rect.centery),
                  UI_TEXT, font_size=16, bold=True, centered=True, outline=True)

        # Targeting buttons
        button_y = targeting_section_rect.y + 30
        button_height = 25
        button_spacing = 5
        button_width = (targeting_section_rect.width - 20) // 2  # Two buttons per row

        # Define targeting options
        targeting_options = [
            {"name": "Closest", "value": TARGET_CLOSEST, "color": COMIC_BLUE},
            {"name": "First", "value": TARGET_FIRST, "color": COMIC_GREEN},
            {"name": "Last", "value": TARGET_LAST, "color": COMIC_ORANGE},
            {"name": "Random", "value": TARGET_RANDOM, "color": COMIC_PURPLE}
        ]

        # Draw targeting buttons in a 2x2 grid
        for i, option in enumerate(targeting_options):
            row = i // 2
            col = i % 2

            button_rect = pygame.Rect(
                targeting_section_rect.x + 10 + col * (button_width + 10),
                button_y + row * (button_height + button_spacing),
                button_width,
                button_height
            )

            # Highlight current strategy
            is_selected = tower.targeting_strategy == option["value"]
            color = option["color"] if is_selected else UI_BUTTON
            border_color = COMIC_YELLOW if is_selected else COMIC_DARK

            # Shadow effect
            shadow_rect = button_rect.copy()
            shadow_rect.x += 2
            shadow_rect.y += 2
            pygame.draw.rect(surface, COMIC_DARK, shadow_rect, border_radius=5)

            # Button
            pygame.draw.rect(surface, color, button_rect, border_radius=5)
            pygame.draw.rect(surface, border_color, button_rect, 2, border_radius=5)

            # Button text
            draw_text(surface, option["name"],
                      (button_rect.centerx, button_rect.centery),
                      UI_TEXT, font_size=14, bold=True, centered=True, outline=True)

        # Sell button with comic-style - positioned below the targeting section
        # Calculate position to ensure it doesn't overlap with other elements
        sell_rect = pygame.Rect(
            SCREEN_WIDTH - SIDEBAR_WIDTH + 10,
            targeting_section_rect.bottom + 10,  # Position relative to targeting section
            SIDEBAR_WIDTH - 20,
            30  # Reduced height
        )

        # Back button to return to tower selection
        back_button_rect = pygame.Rect(
            SCREEN_WIDTH - SIDEBAR_WIDTH + 10,
            sell_rect.bottom + 10,
            SIDEBAR_WIDTH - 20,
            30
        )

        # Shadow effect
        shadow_rect = back_button_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        pygame.draw.rect(surface, COMIC_DARK, shadow_rect, border_radius=8)

        # Main button
        pygame.draw.rect(surface, UI_BUTTON, back_button_rect, border_radius=8)
        pygame.draw.rect(surface, COMIC_DARK, back_button_rect, 2, border_radius=8)

        # Back button text
        draw_text(surface, "Back to Tower Selection",
                  (back_button_rect.centerx, back_button_rect.centery),
                  UI_TEXT, font_size=16, bold=True, centered=True, outline=True)

        # Shadow effect
        shadow_rect = sell_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        pygame.draw.rect(surface, COMIC_DARK, shadow_rect, border_radius=8)

        # Main button
        pygame.draw.rect(surface, UI_DANGER, sell_rect, border_radius=8)
        pygame.draw.rect(surface, COMIC_DARK, sell_rect, 2, border_radius=8)

        # Sell text with comic-style
        sell_value = tower.cost // 2
        draw_text(surface, f"Sell Tower (${sell_value})",
                  (sell_rect.centerx, sell_rect.centery),
                  UI_TEXT, font_size=16, bold=True, centered=True, outline=True)

    def _draw_menu_button(self, surface: pygame.Surface) -> None:
        """
        Draw the menu button and dropdown if open

        Args:
            surface: Pygame surface to draw on
        """
        # Draw menu button with comic-style
        # Shadow effect
        shadow_rect = self.menu_button_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        pygame.draw.rect(surface, COMIC_DARK, shadow_rect, border_radius=8)

        # Main button
        button_color = UI_BUTTON_HOVER if self.menu_open else UI_BUTTON
        pygame.draw.rect(surface, button_color, self.menu_button_rect, border_radius=8)
        pygame.draw.rect(surface, COMIC_DARK, self.menu_button_rect, 2, border_radius=8)

        # Draw hamburger menu icon
        line_width = self.menu_button_size - 16
        line_height = 3
        line_spacing = 6
        start_x = self.menu_button_rect.x + 8
        start_y = self.menu_button_rect.y + 12

        for i in range(3):
            line_rect = pygame.Rect(
                start_x,
                start_y + i * line_spacing,
                line_width,
                line_height
            )
            pygame.draw.rect(surface, UI_TEXT, line_rect, border_radius=1)

        # Draw dropdown menu if open
        if self.menu_open:
            dropdown_height = len(self.menu_options) * self.menu_option_height
            dropdown_rect = pygame.Rect(
                self.menu_button_rect.x,
                self.menu_button_rect.bottom + 5,
                self.menu_width,
                dropdown_height
            )

            # Shadow effect
            shadow_dropdown = dropdown_rect.copy()
            shadow_dropdown.x += 3
            shadow_dropdown.y += 3
            pygame.draw.rect(surface, COMIC_DARK, shadow_dropdown, border_radius=8)

            # Main dropdown panel
            pygame.draw.rect(surface, UI_PANEL, dropdown_rect, border_radius=8)
            pygame.draw.rect(surface, COMIC_DARK, dropdown_rect, 2, border_radius=8)

            # Draw options
            for i, option in enumerate(self.menu_options):
                option_rect = pygame.Rect(
                    dropdown_rect.x,
                    dropdown_rect.y + i * self.menu_option_height,
                    dropdown_rect.width,
                    self.menu_option_height
                )

                # Highlight on hover
                mouse_pos = pygame.mouse.get_pos()
                if option_rect.collidepoint(mouse_pos):
                    pygame.draw.rect(surface, UI_BUTTON_HOVER, option_rect, border_radius=0)

                # Draw option text
                draw_text(surface, option["text"],
                          (dropdown_rect.x + 10, option_rect.centery),
                          UI_TEXT, font_size=16, bold=True, outline=True)

    def add_floating_text(self, text, pos, color=(255,255,255)):
        self.floating_texts.append(FloatingText(text, pos, color))

    def handle_click(self, pos: Tuple[int, int], game_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle mouse click on the HUD

        Args:
            pos: Mouse position (x, y)
            game_state: Current game state

        Returns:
            Dictionary with action information
        """
        # Check menu button
        if self.menu_button_rect.collidepoint(pos):
            self.menu_open = not self.menu_open
            return {'action': 'toggle_menu'}

        # Check menu options if menu is open
        if self.menu_open:
            dropdown_height = len(self.menu_options) * self.menu_option_height
            dropdown_rect = pygame.Rect(
                self.menu_button_rect.x,
                self.menu_button_rect.bottom + 5,
                self.menu_width,
                dropdown_height
            )

            if dropdown_rect.collidepoint(pos):
                # Determine which option was clicked
                option_idx = (pos[1] - dropdown_rect.y) // self.menu_option_height
                if 0 <= option_idx < len(self.menu_options):
                    action = self.menu_options[option_idx]["action"]
                    self.menu_open = False  # Close menu after selection
                    return {'action': action}
            else:
                # Close menu if clicked outside
                self.menu_open = False
                return {'action': 'close_menu'}

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
            SCREEN_HEIGHT - 60,
            SIDEBAR_WIDTH - 20,
            40
        )
        if wave_button_rect.collidepoint(pos) and not game_state['wave_in_progress'] and game_state['cooldown_remaining'] <= 0:
            return {'action': 'start_wave'}

        # Check upgrade buttons if a tower is selected
        if game_state['selected_tower']:
            tower = game_state['selected_tower']

            # Calculate positions based on our new layout
            info_panel_y = self.header_height + 10
            info_panel_height = 120

            # Upgrade section position - matches the draw method
            upgrade_section_rect = pygame.Rect(
                SCREEN_WIDTH - SIDEBAR_WIDTH + 10,
                info_panel_y + info_panel_height + 10,
                SIDEBAR_WIDTH - 20,
                140
            )

            upgrade_y = upgrade_section_rect.y + 30
            path_height = 50

            # Check upgrade buttons for each path
            for path_idx, path in enumerate(['path1', 'path2']):
                if path in tower.upgrade_paths:
                    upgrade_cost = tower.get_upgrade_cost(path)
                    if upgrade_cost > 0:
                        button_rect = pygame.Rect(
                            upgrade_section_rect.x + 5,
                            upgrade_y + 22 + path_idx * path_height,
                            upgrade_section_rect.width - 10,
                            22
                        )
                        if button_rect.collidepoint(pos):
                            if game_state['coins'] >= upgrade_cost:
                                return {'action': 'upgrade_tower', 'path': path}
                            else:
                                return {'action': 'not_enough_coins'}

            # Check targeting options
            info_panel_y = self.header_height + 10
            info_panel_height = 120

            # Calculate targeting section position - matches the draw method
            upgrade_section_rect = pygame.Rect(
                SCREEN_WIDTH - SIDEBAR_WIDTH + 10,
                info_panel_y + info_panel_height + 10,
                SIDEBAR_WIDTH - 20,
                140
            )

            targeting_section_rect = pygame.Rect(
                SCREEN_WIDTH - SIDEBAR_WIDTH + 10,
                upgrade_section_rect.bottom + 10,
                SIDEBAR_WIDTH - 20,
                90
            )

            button_y = targeting_section_rect.y + 30
            button_height = 25
            button_spacing = 5
            button_width = (targeting_section_rect.width - 20) // 2

            # Define targeting options (same as in draw method)
            targeting_options = [
                {"name": "Closest", "value": TARGET_CLOSEST, "color": COMIC_BLUE},
                {"name": "First", "value": TARGET_FIRST, "color": COMIC_GREEN},
                {"name": "Last", "value": TARGET_LAST, "color": COMIC_ORANGE},
                {"name": "Random", "value": TARGET_RANDOM, "color": COMIC_PURPLE}
            ]

            # Check if any targeting button was clicked
            for i, option in enumerate(targeting_options):
                row = i // 2
                col = i % 2

                button_rect = pygame.Rect(
                    targeting_section_rect.x + 10 + col * (button_width + 10),
                    button_y + row * (button_height + button_spacing),
                    button_width,
                    button_height
                )

                if button_rect.collidepoint(pos):
                    return {'action': 'set_targeting', 'strategy': option["value"]}

            # Check sell button - positioned below targeting section
            sell_rect = pygame.Rect(
                SCREEN_WIDTH - SIDEBAR_WIDTH + 10,
                targeting_section_rect.bottom + 10,  # Position relative to targeting section
                SIDEBAR_WIDTH - 20,
                30
            )
            if sell_rect.collidepoint(pos):
                return {'action': 'sell_tower'}

            # Check back button
            back_button_rect = pygame.Rect(
                SCREEN_WIDTH - SIDEBAR_WIDTH + 10,
                sell_rect.bottom + 10,
                SIDEBAR_WIDTH - 20,
                30
            )
            if back_button_rect.collidepoint(pos):
                return {'action': 'deselect_tower'}

        return {'action': 'none'}

    def update(self, dt):
        # Update floating texts
        self.floating_texts = [ft for ft in self.floating_texts if ft.alive]
        for ft in self.floating_texts:
            ft.update(dt)
