"""
Utility functions for the Tower Defense Game
"""
import os
import pygame
import math
from typing import Tuple, List, Dict, Any, Optional

def load_image(filename: str, scale: float = 1.0, convert_alpha: bool = True) -> pygame.Surface:
    """
    Load an image from the assets folder

    Args:
        filename: Path to the image file relative to the assets/images directory
        scale: Scale factor to resize the image
        convert_alpha: Whether to convert the image to include alpha channel

    Returns:
        Loaded and processed pygame Surface
    """
    filepath = os.path.join("assets", "images", filename)
    try:
        if convert_alpha:
            image = pygame.image.load(filepath).convert_alpha()
        else:
            image = pygame.image.load(filepath).convert()

        if scale != 1.0:
            original_size = image.get_size()
            new_size = (int(original_size[0] * scale), int(original_size[1] * scale))
            image = pygame.transform.scale(image, new_size)

        return image
    except pygame.error as e:
        print(f"Error loading image {filepath}: {e}")
        # Create a placeholder surface with a warning pattern
        surface = pygame.Surface((64, 64))
        surface.fill((255, 0, 255))  # Magenta
        pygame.draw.line(surface, (0, 0, 0), (0, 0), (64, 64), 2)
        pygame.draw.line(surface, (0, 0, 0), (64, 0), (0, 64), 2)
        return surface

def load_sound(filename: str) -> pygame.mixer.Sound:
    """
    Load a sound from the assets folder

    Args:
        filename: Path to the sound file relative to the assets/sounds directory

    Returns:
        Loaded pygame Sound object
    """
    filepath = os.path.join("assets", "sounds", filename)
    try:
        return pygame.mixer.Sound(filepath)
    except pygame.error as e:
        print(f"Error loading sound {filepath}: {e}")
        # Return a silent sound
        return pygame.mixer.Sound(buffer=bytes([0] * 44))

def calculate_distance(pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
    """
    Calculate the Euclidean distance between two points

    Args:
        pos1: First position (x, y)
        pos2: Second position (x, y)

    Returns:
        Distance between the two points
    """
    return math.sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)

def calculate_angle(pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
    """
    Calculate the angle in radians between two points

    Args:
        pos1: First position (x, y)
        pos2: Second position (x, y)

    Returns:
        Angle in radians
    """
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    return math.atan2(dy, dx)

def rotate_image(image: pygame.Surface, angle_degrees: float) -> Tuple[pygame.Surface, pygame.Rect]:
    """
    Rotate an image around its center

    Args:
        image: Surface to rotate
        angle_degrees: Angle in degrees

    Returns:
        Tuple of (rotated surface, new rect)
    """
    original_rect = image.get_rect()
    rotated_image = pygame.transform.rotate(image, angle_degrees)
    rotated_rect = original_rect.copy()
    rotated_rect.center = rotated_image.get_rect().center
    return rotated_image, rotated_rect

def grid_to_pixel(grid_pos: Tuple[int, int], grid_size: int) -> Tuple[int, int]:
    """
    Convert grid coordinates to pixel coordinates

    Args:
        grid_pos: Grid position (column, row)
        grid_size: Size of each grid cell in pixels

    Returns:
        Pixel position (x, y)
    """
    return (grid_pos[0] * grid_size, grid_pos[1] * grid_size)

def pixel_to_grid(pixel_pos: Tuple[int, int], grid_size: int) -> Tuple[int, int]:
    """
    Convert pixel coordinates to grid coordinates

    Args:
        pixel_pos: Pixel position (x, y)
        grid_size: Size of each grid cell in pixels

    Returns:
        Grid position (column, row)
    """
    return (pixel_pos[0] // grid_size, pixel_pos[1] // grid_size)

def draw_text(surface: pygame.Surface, text: str, pos: Tuple[int, int],
              color: Tuple[int, int, int], font_size: int = 24,
              centered: bool = False, bold: bool = False,
              outline: bool = False, outline_color: Tuple[int, int, int] = (0, 0, 0),
              font_name: str = 'Arial') -> pygame.Rect:
    """
    Draw text on a surface with comic-style options

    Args:
        surface: Surface to draw on
        text: Text to draw
        pos: Position to draw at (x, y)
        color: RGB color tuple
        font_size: Font size in points
        centered: Whether to center the text at the position
        bold: Whether to use bold font
        outline: Whether to add an outline (comic-style)
        outline_color: RGB color tuple for the outline
        font_name: Name of the font to use

    Returns:
        The rectangle containing the text
    """
    # Create font
    font = pygame.font.SysFont(font_name, font_size, bold=bold)

    # Create the main text surface
    text_surface = font.render(text, True, color)

    # Get the text rectangle
    if centered:
        text_rect = text_surface.get_rect(center=pos)
    else:
        text_rect = text_surface.get_rect(topleft=pos)

    # Draw outline if requested (creates a comic-book style text)
    if outline:
        # Create outline by drawing the text multiple times with small offsets
        outline_positions = [
            (-1, -1), (0, -1), (1, -1),
            (-1, 0),           (1, 0),
            (-1, 1),  (0, 1),  (1, 1)
        ]

        for dx, dy in outline_positions:
            outline_rect = text_rect.copy()
            outline_rect.x += dx
            outline_rect.y += dy
            outline_surface = font.render(text, True, outline_color)
            surface.blit(outline_surface, outline_rect)

    # Draw the main text on top
    surface.blit(text_surface, text_rect)

    return text_rect
