"""
Main game class for the tower defense game.
"""
import pygame
import sys
import time
from src.core.scene import SceneManager
from src.core.resource_manager import ResourceManager
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE


class Game:
    """Main game class that manages the game loop and state."""
    
    def __init__(self):
        """Initialize a new Game instance."""
        # Initialize pygame
        pygame.init()
        pygame.mixer.init()
        
        # Create the screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        
        # Create the clock
        self.clock = pygame.time.Clock()
        
        # Create managers
        self.scene_manager = SceneManager()
        self.resource_manager = ResourceManager()
        
        # Game state
        self.running = False
        self.paused = False
        
        # Timing
        self.last_time = time.time()
        self.dt = 0
    
    def run(self):
        """Run the main game loop."""
        self.running = True
        
        while self.running:
            # Calculate delta time
            current_time = time.time()
            self.dt = current_time - self.last_time
            self.last_time = current_time
            
            # Handle events
            self.handle_events()
            
            # Update
            if not self.paused:
                self.update()
            
            # Render
            self.render()
            
            # Cap the frame rate
            self.clock.tick(FPS)
        
        # Clean up
        pygame.quit()
        sys.exit()
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            # Quit event
            if event.type == pygame.QUIT:
                self.running = False
            
            # Escape key to quit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
            
            # Pass the event to the current scene
            self.scene_manager.handle_event(event)
    
    def update(self):
        """Update the game state."""
        self.scene_manager.update(self.dt)
    
    def render(self):
        """Render the game."""
        # Clear the screen
        self.screen.fill((0, 0, 0))
        
        # Render the current scene
        self.scene_manager.render(self.screen)
        
        # Render the pause screen if paused
        if self.paused:
            self.render_pause_screen()
        
        # Update the display
        pygame.display.flip()
    
    def render_pause_screen(self):
        """Render the pause screen overlay."""
        # Create a semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        # Render "PAUSED" text
        font = pygame.font.SysFont("arial", 48)
        text = font.render("PAUSED", True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)
    
    def quit(self):
        """Quit the game."""
        self.running = False
