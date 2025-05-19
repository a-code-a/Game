"""
Map 1 implementation for the Tower Defense Game
"""
import pygame
from typing import List, Tuple, Set

from maps.map import Map
from constants import GRID_SIZE

class Map1(Map):
    """First map with a simple S-shaped path"""

    def __init__(self):
        """Initialize Map 1"""
        super().__init__("Minion Valley", "map1.png")

    def initialize_grid(self) -> None:
        """Initialize the grid with path and buildable areas"""
        # Define the path waypoints in grid coordinates
        path_waypoints = [
            (0, 5),      # Start from left
            (3, 5),
            (3, 2),
            (8, 2),
            (8, 8),
            (12, 8),
            (12, 4),
            (15, 4)      # End at right
        ]

        # Convert path waypoints to pixel coordinates (center of cells)
        self.path = [self.grid_to_pixel(pos) for pos in path_waypoints]

        # Fill in the path grid cells
        self._fill_path_grid(path_waypoints)

        # Set buildable areas (all cells except path and border)
        self._set_buildable_grid()

    def _fill_path_grid(self, waypoints: List[Tuple[int, int]]) -> None:
        """
        Fill in the path grid cells based on waypoints

        Args:
            waypoints: List of waypoints in grid coordinates
        """
        self.path_grid = set()

        # For each pair of consecutive waypoints
        for i in range(len(waypoints) - 1):
            start_x, start_y = waypoints[i]
            end_x, end_y = waypoints[i + 1]

            # Determine direction
            dx = 1 if end_x > start_x else -1 if end_x < start_x else 0
            dy = 1 if end_y > start_y else -1 if end_y < start_y else 0

            # Fill in cells between waypoints
            current_x, current_y = start_x, start_y
            while (current_x, current_y) != (end_x, end_y):
                self.path_grid.add((current_x, current_y))

                # Move to next cell
                if current_x != end_x:
                    current_x += dx
                elif current_y != end_y:
                    current_y += dy

            # Add the end point
            self.path_grid.add((end_x, end_y))

    def _set_buildable_grid(self) -> None:
        """Set buildable areas (all cells except path and border)"""
        self.buildable_grid = set()

        # For each cell in the grid
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                # Skip path cells
                if (x, y) in self.path_grid:
                    continue

                # Skip border cells (1 cell buffer around path)
                is_border = False
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if (x + dx, y + dy) in self.path_grid:
                            is_border = True
                            break
                    if is_border:
                        break

                if not is_border:
                    self.buildable_grid.add((x, y))
