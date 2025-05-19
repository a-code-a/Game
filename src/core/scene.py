"""
Scene class for managing different game scenes.
"""


class Scene:
    """Base class for all game scenes."""
    
    def __init__(self, game):
        """Initialize a new Scene.
        
        Args:
            game: The game instance this scene belongs to.
        """
        self.game = game
    
    def enter(self):
        """Called when the scene is entered."""
        pass
    
    def exit(self):
        """Called when the scene is exited."""
        pass
    
    def update(self, dt):
        """Update the scene.
        
        Args:
            dt (float): The time delta since the last update in seconds.
        """
        pass
    
    def render(self, screen):
        """Render the scene.
        
        Args:
            screen (pygame.Surface): The screen to render to.
        """
        pass
    
    def handle_event(self, event):
        """Handle a pygame event.
        
        Args:
            event (pygame.event.Event): The event to handle.
        """
        pass


class SceneManager:
    """Manager for switching between different game scenes."""
    
    def __init__(self):
        """Initialize a new SceneManager."""
        self.scenes = {}
        self.current_scene = None
    
    def add_scene(self, name, scene):
        """Add a scene to the manager.
        
        Args:
            name (str): The name of the scene.
            scene (Scene): The scene to add.
        """
        self.scenes[name] = scene
    
    def set_scene(self, name):
        """Set the current scene.
        
        Args:
            name (str): The name of the scene to set.
            
        Returns:
            bool: True if the scene was set, False if the scene was not found.
        """
        if name not in self.scenes:
            return False
        
        # Exit the current scene if there is one
        if self.current_scene:
            self.current_scene.exit()
        
        # Set the new scene
        self.current_scene = self.scenes[name]
        
        # Enter the new scene
        self.current_scene.enter()
        
        return True
    
    def update(self, dt):
        """Update the current scene.
        
        Args:
            dt (float): The time delta since the last update in seconds.
        """
        if self.current_scene:
            self.current_scene.update(dt)
    
    def render(self, screen):
        """Render the current scene.
        
        Args:
            screen (pygame.Surface): The screen to render to.
        """
        if self.current_scene:
            self.current_scene.render(screen)
    
    def handle_event(self, event):
        """Handle a pygame event.
        
        Args:
            event (pygame.event.Event): The event to handle.
        """
        if self.current_scene:
            self.current_scene.handle_event(event)
