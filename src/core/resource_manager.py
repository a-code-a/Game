"""
Resource manager for loading and caching game assets.
"""
import os
import pygame


class ResourceManager:
    """Manager for loading and caching game assets."""
    
    def __init__(self):
        """Initialize a new ResourceManager."""
        self.images = {}
        self.sounds = {}
        self.fonts = {}
    
    def load_image(self, name, path, scale=None):
        """Load an image and cache it.
        
        Args:
            name (str): The name to use for caching the image.
            path (str): The path to the image file.
            scale (tuple, optional): A tuple (width, height) to scale the image to.
            
        Returns:
            pygame.Surface: The loaded image.
        """
        # Check if the image is already loaded
        if name in self.images:
            return self.images[name]
        
        # Load the image
        try:
            image = pygame.image.load(path).convert_alpha()
            
            # Scale the image if needed
            if scale:
                image = pygame.transform.scale(image, scale)
            
            # Cache the image
            self.images[name] = image
            return image
        except pygame.error:
            print(f"Error loading image: {path}")
            # Return a placeholder image
            placeholder = pygame.Surface((32, 32))
            placeholder.fill((255, 0, 255))  # Magenta for missing textures
            return placeholder
    
    def load_sound(self, name, path):
        """Load a sound and cache it.
        
        Args:
            name (str): The name to use for caching the sound.
            path (str): The path to the sound file.
            
        Returns:
            pygame.mixer.Sound: The loaded sound.
        """
        # Check if the sound is already loaded
        if name in self.sounds:
            return self.sounds[name]
        
        # Load the sound
        try:
            sound = pygame.mixer.Sound(path)
            
            # Cache the sound
            self.sounds[name] = sound
            return sound
        except pygame.error:
            print(f"Error loading sound: {path}")
            return None
    
    def load_font(self, name, path, size):
        """Load a font and cache it.
        
        Args:
            name (str): The name to use for caching the font.
            path (str): The path to the font file.
            size (int): The font size.
            
        Returns:
            pygame.font.Font: The loaded font.
        """
        # Create a unique name for the font and size
        font_name = f"{name}_{size}"
        
        # Check if the font is already loaded
        if font_name in self.fonts:
            return self.fonts[font_name]
        
        # Load the font
        try:
            if os.path.exists(path):
                font = pygame.font.Font(path, size)
            else:
                # Use a system font if the file doesn't exist
                font = pygame.font.SysFont(name, size)
            
            # Cache the font
            self.fonts[font_name] = font
            return font
        except pygame.error:
            print(f"Error loading font: {path}")
            # Return a default font
            return pygame.font.SysFont("arial", size)
    
    def get_image(self, name):
        """Get a cached image.
        
        Args:
            name (str): The name of the image to get.
            
        Returns:
            pygame.Surface: The cached image, or None if not found.
        """
        return self.images.get(name)
    
    def get_sound(self, name):
        """Get a cached sound.
        
        Args:
            name (str): The name of the sound to get.
            
        Returns:
            pygame.mixer.Sound: The cached sound, or None if not found.
        """
        return self.sounds.get(name)
    
    def get_font(self, name, size):
        """Get a cached font.
        
        Args:
            name (str): The name of the font to get.
            size (int): The font size.
            
        Returns:
            pygame.font.Font: The cached font, or None if not found.
        """
        font_name = f"{name}_{size}"
        return self.fonts.get(font_name)
