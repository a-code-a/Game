"""
Create placeholder images for the Tower Defense Game
"""
import os
import pygame
import sys

def create_image(filename, size, color, shape='rect'):
    """
    Create a placeholder image
    
    Args:
        filename: Output filename
        size: Image size (width, height)
        color: RGB color tuple
        shape: Shape to draw ('rect', 'circle', 'triangle')
    """
    # Create the surface
    surface = pygame.Surface(size, pygame.SRCALPHA)
    
    # Draw the shape
    if shape == 'rect':
        pygame.draw.rect(surface, color, (0, 0, size[0], size[1]))
        pygame.draw.rect(surface, (0, 0, 0), (0, 0, size[0], size[1]), 2)
    elif shape == 'circle':
        pygame.draw.circle(surface, color, (size[0] // 2, size[1] // 2), min(size) // 2)
        pygame.draw.circle(surface, (0, 0, 0), (size[0] // 2, size[1] // 2), min(size) // 2, 2)
    elif shape == 'triangle':
        points = [(size[0] // 2, 0), (0, size[1]), (size[0], size[1])]
        pygame.draw.polygon(surface, color, points)
        pygame.draw.polygon(surface, (0, 0, 0), points, 2)
    
    # Save the image
    pygame.image.save(surface, filename)
    print(f"Created {filename}")

def main():
    """Create all placeholder images"""
    # Initialize pygame
    pygame.init()
    
    # Create directories if they don't exist
    directories = [
        'assets/images/towers',
        'assets/images/enemies',
        'assets/images/projectiles',
        'assets/images/maps',
        'assets/images/ui'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # Create tower images
    create_image('assets/images/towers/basic.png', (48, 48), (0, 0, 255), 'rect')
    create_image('assets/images/towers/sniper.png', (48, 48), (255, 0, 0), 'rect')
    create_image('assets/images/towers/area.png', (48, 48), (0, 255, 0), 'circle')
    create_image('assets/images/towers/support.png', (48, 48), (255, 255, 0), 'triangle')
    
    # Create enemy images
    create_image('assets/images/enemies/basic_minion.png', (32, 32), (255, 255, 0), 'circle')
    create_image('assets/images/enemies/fast_minion.png', (24, 24), (255, 100, 0), 'circle')
    create_image('assets/images/enemies/tank_minion.png', (40, 40), (100, 100, 255), 'circle')
    create_image('assets/images/enemies/boss_minion.png', (64, 64), (255, 0, 255), 'circle')
    
    # Create projectile images
    create_image('assets/images/projectiles/basic_projectile.png', (16, 16), (0, 0, 255), 'circle')
    create_image('assets/images/projectiles/sniper_projectile.png', (16, 16), (255, 0, 0), 'rect')
    create_image('assets/images/projectiles/area_projectile.png', (16, 16), (0, 255, 0), 'triangle')
    
    # Create map image
    map_surface = pygame.Surface((1024 - 200, 768))
    map_surface.fill((100, 150, 100))  # Green background
    
    # Draw a path
    path_points = [
        (0, 5 * 64 + 32),
        (3 * 64 + 32, 5 * 64 + 32),
        (3 * 64 + 32, 2 * 64 + 32),
        (8 * 64 + 32, 2 * 64 + 32),
        (8 * 64 + 32, 8 * 64 + 32),
        (12 * 64 + 32, 8 * 64 + 32),
        (12 * 64 + 32, 4 * 64 + 32),
        (1024 - 200, 4 * 64 + 32)
    ]
    
    # Draw the path
    pygame.draw.lines(map_surface, (150, 100, 50), False, path_points, 64)
    pygame.draw.lines(map_surface, (200, 150, 100), False, path_points, 60)
    
    # Save the map
    pygame.image.save(map_surface, 'assets/images/maps/map1.png')
    print("Created assets/images/maps/map1.png")
    
    # Clean up
    pygame.quit()

if __name__ == "__main__":
    main()
