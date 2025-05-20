"""
Base Map class for the Tower Defense Game
"""
import pygame
from typing import List, Dict, Any, Tuple, Optional, Set
import os
from collections import namedtuple

from utils import load_image, grid_to_pixel, pixel_to_grid
from constants import GRID_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, SIDEBAR_WIDTH

PathPoint = namedtuple('PathPoint', ['x', 'y'])

class Map:
    """Base class for all maps"""

    def __init__(self, name: str, background_image: str, grid_size: int = GRID_SIZE):
        """
        Initialize a map

        Args:
            name: Name of the map
            background_image: Filename of the background image
            grid_size: Size of each grid cell in pixels
        """
        self.name = name
        self.grid_size = grid_size

        # Calculate grid dimensions
        self.grid_width = (SCREEN_WIDTH - SIDEBAR_WIDTH) // grid_size
        self.grid_height = SCREEN_HEIGHT // grid_size

        # Load background image
        self.background = load_image(os.path.join("maps", background_image), convert_alpha=False)
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH - SIDEBAR_WIDTH, SCREEN_HEIGHT))

        # Initialize path and buildable areas
        self.path = []
        self.path_grid = set()  # Grid cells that are part of the path
        self.buildable_grid = set()  # Grid cells where towers can be built

        # Initialize the grid
        self.initialize_grid()

        # Convert path to PathPoint namedtuples for efficiency
        self.path = [PathPoint(x, y) for (x, y) in self.path]

    def initialize_grid(self) -> None:
        """
        Initialize the grid with path and buildable areas
        This should be overridden by subclasses
        """
        pass

    def is_buildable(self, grid_x: int, grid_y: int) -> bool:
        """
        Check if a grid cell is buildable

        Args:
            grid_x: Grid x-coordinate
            grid_y: Grid y-coordinate

        Returns:
            True if the cell is buildable, False otherwise
        """
        return (grid_x, grid_y) in self.buildable_grid

    def is_path(self, grid_x: int, grid_y: int) -> bool:
        """
        Check if a grid cell is part of the path

        Args:
            grid_x: Grid x-coordinate
            grid_y: Grid y-coordinate

        Returns:
            True if the cell is part of the path, False otherwise
        """
        return (grid_x, grid_y) in self.path_grid

    def get_path(self) -> List[Tuple[int, int]]:
        """
        Get the path for enemies to follow

        Returns:
            List of waypoints (x, y) in pixel coordinates
        """
        return self.path

    def get_spawn_point(self) -> Tuple[int, int]:
        """
        Get the spawn point for enemies

        Returns:
            Spawn point (x, y) in pixel coordinates
        """
        return self.path[0]

    def get_end_point(self) -> Tuple[int, int]:
        """
        Get the end point of the path

        Returns:
            End point (x, y) in pixel coordinates
        """
        return self.path[-1]

    def draw(self, surface: pygame.Surface, show_grid: bool = False) -> None:
        """
        Draw the map on the surface

        Args:
            surface: Pygame surface to draw on
            show_grid: Whether to show the grid
        """
        # Draw background (pre-rendered for performance)
        surface.blit(self.background, (0, 0))

        # Draw grid if requested
        if show_grid:
            for x in range(0, SCREEN_WIDTH - SIDEBAR_WIDTH, self.grid_size):
                pygame.draw.line(surface, (200, 200, 200, 100), (x, 0), (x, SCREEN_HEIGHT), 1)
            for y in range(0, SCREEN_HEIGHT, self.grid_size):
                pygame.draw.line(surface, (200, 200, 200, 100), (0, y), (SCREEN_WIDTH - SIDEBAR_WIDTH, y), 1)

            # Highlight buildable areas
            for grid_x, grid_y in self.buildable_grid:
                rect = pygame.Rect(
                    grid_x * self.grid_size,
                    grid_y * self.grid_size,
                    self.grid_size,
                    self.grid_size
                )
                pygame.draw.rect(surface, (0, 255, 0, 50), rect)

            # Highlight path
            for grid_x, grid_y in self.path_grid:
                rect = pygame.Rect(
                    grid_x * self.grid_size,
                    grid_y * self.grid_size,
                    self.grid_size,
                    self.grid_size
                )
                pygame.draw.rect(surface, (255, 0, 0, 50), rect)

    def pixel_to_grid(self, pixel_pos: Tuple[int, int]) -> Tuple[int, int]:
        """
        Convert pixel coordinates to grid coordinates

        Args:
            pixel_pos: Pixel position (x, y)

        Returns:
            Grid position (column, row)
        """
        return pixel_to_grid(pixel_pos, self.grid_size)

    def grid_to_pixel(self, grid_pos: Tuple[int, int]) -> Tuple[int, int]:
        """
        Convert grid coordinates to pixel coordinates (center of the cell)

        Args:
            grid_pos: Grid position (column, row)

        Returns:
            Pixel position (x, y) at the center of the grid cell
        """
        pixel_pos = grid_to_pixel(grid_pos, self.grid_size)
        return (pixel_pos[0] + self.grid_size // 2, pixel_pos[1] + self.grid_size // 2)
