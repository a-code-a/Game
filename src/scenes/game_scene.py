"""
Game scene for the tower defense gameplay.
"""
import pygame
from src.core.scene import Scene
from src.managers.entity_manager import EntityManager
from src.managers.wave_manager import WaveManager
from src.managers.economy_manager import EconomyManager
from src.systems.render_system import RenderSystem
from src.systems.movement_system import MovementSystem
from src.systems.path_following_system import PathFollowingSystem
from src.systems.targeting_system import TargetingSystem
from src.systems.collision_system import CollisionSystem
from src.entities.tower import Tower
from src.utils.vector import Vector2
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, PATH_WIDTH, PATH_COLOR, TOWER_COST


class GameScene(Scene):
    """Scene for the tower defense gameplay."""
    
    def __init__(self, game):
        """Initialize a new GameScene.
        
        Args:
            game: The game instance this scene belongs to.
        """
        super().__init__(game)
        
        # Create managers
        self.entity_manager = EntityManager()
        self.wave_manager = WaveManager(self.entity_manager)
        self.economy_manager = EconomyManager()
        
        # Create systems
        self.render_system = RenderSystem(game.screen)
        self.movement_system = MovementSystem()
        self.path_following_system = PathFollowingSystem()
        self.targeting_system = TargetingSystem(self.entity_manager)
        self.collision_system = CollisionSystem(self.entity_manager)
        
        # Add systems to the entity manager
        self.entity_manager.add_system(self.render_system)
        self.entity_manager.add_system(self.movement_system)
        self.entity_manager.add_system(self.path_following_system)
        self.entity_manager.add_system(self.targeting_system)
        self.entity_manager.add_system(self.collision_system)
        
        # Game state
        self.selected_tower_type = "basic"
        self.placing_tower = False
        self.can_place_tower = False
        self.tower_placement_pos = Vector2(0, 0)
        
        # Create the path
        self.create_path()
        
        # Set up the wave manager
        self.wave_manager.set_path(self.path)
        
        # UI elements
        self.font = pygame.font.SysFont("arial", 24)
    
    def enter(self):
        """Called when the scene is entered."""
        # Start the wave manager
        self.wave_manager.start()
    
    def exit(self):
        """Called when the scene is exited."""
        # Stop the wave manager
        self.wave_manager.stop()
    
    def update(self, dt):
        """Update the scene.
        
        Args:
            dt (float): The time delta since the last update in seconds.
        """
        # Update the wave manager
        self.wave_manager.update()
        
        # Update the entity manager
        self.entity_manager.update(dt)
        
        # Update the targeting system with the current enemies
        enemies = self.entity_manager.get_entities_with_tag("enemy")
        self.targeting_system.set_enemies(enemies)
        
        # Update the collision system with the current projectiles and enemies
        projectiles = self.entity_manager.get_entities_with_tag("projectile")
        self.collision_system.set_projectiles(projectiles)
        self.collision_system.set_enemies(enemies)
        
        # Update tower placement
        if self.placing_tower:
            mouse_pos = pygame.mouse.get_pos()
            self.tower_placement_pos = Vector2(mouse_pos[0], mouse_pos[1])
            self.can_place_tower = self.check_tower_placement()
    
    def render(self, screen):
        """Render the scene.
        
        Args:
            screen (pygame.Surface): The screen to render to.
        """
        # Clear the screen
        screen.fill((0, 128, 0))  # Green background
        
        # Draw the path
        self.draw_path(screen)
        
        # Let the render system draw all entities
        # (This is already handled by the entity manager)
        
        # Draw tower placement preview
        if self.placing_tower:
            color = (0, 255, 0, 128) if self.can_place_tower else (255, 0, 0, 128)
            preview_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
            preview_surface.fill(color)
            screen.blit(preview_surface, (
                self.tower_placement_pos.x - 20,
                self.tower_placement_pos.y - 20
            ))
        
        # Draw UI
        self.draw_ui(screen)
    
    def handle_event(self, event):
        """Handle a pygame event.
        
        Args:
            event (pygame.event.Event): The event to handle.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if self.placing_tower:
                    # Try to place the tower
                    if self.can_place_tower and self.economy_manager.can_afford(self.selected_tower_type):
                        self.place_tower()
                    self.placing_tower = False
                else:
                    # Start placing a tower
                    if self.economy_manager.can_afford(self.selected_tower_type):
                        self.placing_tower = True
                        mouse_pos = pygame.mouse.get_pos()
                        self.tower_placement_pos = Vector2(mouse_pos[0], mouse_pos[1])
                        self.can_place_tower = self.check_tower_placement()
            elif event.button == 3:  # Right mouse button
                # Cancel tower placement
                self.placing_tower = False
    
    def create_path(self):
        """Create the path for enemies to follow."""
        # Simple path from left to right with some turns
        self.path = [
            Vector2(0, SCREEN_HEIGHT // 2),
            Vector2(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2),
            Vector2(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4),
            Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4),
            Vector2(SCREEN_WIDTH // 2, 3 * SCREEN_HEIGHT // 4),
            Vector2(3 * SCREEN_WIDTH // 4, 3 * SCREEN_HEIGHT // 4),
            Vector2(3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2),
            Vector2(SCREEN_WIDTH, SCREEN_HEIGHT // 2)
        ]
    
    def draw_path(self, screen):
        """Draw the path on the screen.
        
        Args:
            screen (pygame.Surface): The screen to draw on.
        """
        if not self.path:
            return
        
        # Draw the path segments
        for i in range(len(self.path) - 1):
            start = self.path[i].to_int_tuple()
            end = self.path[i + 1].to_int_tuple()
            pygame.draw.line(screen, PATH_COLOR, start, end, PATH_WIDTH)
        
        # Draw circles at the waypoints
        for point in self.path:
            pygame.draw.circle(screen, PATH_COLOR, point.to_int_tuple(), PATH_WIDTH // 2)
    
    def draw_ui(self, screen):
        """Draw the UI elements.
        
        Args:
            screen (pygame.Surface): The screen to draw on.
        """
        # Draw resources
        resources_text = f"Resources: {self.economy_manager.get_resources()}"
        resources_surface = self.font.render(resources_text, True, (255, 255, 255))
        screen.blit(resources_surface, (10, 10))
        
        # Draw wave information
        wave_text = f"Wave: {self.wave_manager.get_current_wave()}"
        wave_surface = self.font.render(wave_text, True, (255, 255, 255))
        screen.blit(wave_surface, (10, 40))
        
        # Draw enemies remaining
        enemies_text = f"Enemies: {self.wave_manager.get_enemies_remaining()}"
        enemies_surface = self.font.render(enemies_text, True, (255, 255, 255))
        screen.blit(enemies_surface, (10, 70))
        
        # Draw tower cost
        tower_cost_text = f"Tower Cost: {TOWER_COST}"
        tower_cost_surface = self.font.render(tower_cost_text, True, (255, 255, 255))
        screen.blit(tower_cost_surface, (10, 100))
    
    def check_tower_placement(self):
        """Check if a tower can be placed at the current position.
        
        Returns:
            bool: True if the tower can be placed, False otherwise.
        """
        # Check if the tower is on the path
        for i in range(len(self.path) - 1):
            start = self.path[i]
            end = self.path[i + 1]
            
            # Calculate the distance from the point to the line segment
            line_vec = end - start
            point_vec = self.tower_placement_pos - start
            line_len = line_vec.length()
            line_unitvec = line_vec / line_len
            point_vec_scaled = point_vec.dot(line_unitvec)
            
            # Check if the point is within the line segment
            if point_vec_scaled < 0 or point_vec_scaled > line_len:
                continue
            
            # Calculate the closest point on the line
            closest_point = start + line_unitvec * point_vec_scaled
            
            # Check if the tower is too close to the path
            if closest_point.distance_to(self.tower_placement_pos) < PATH_WIDTH / 2 + 20:
                return False
        
        # Check if the tower is too close to other towers
        towers = self.entity_manager.get_entities_with_tag("tower")
        for tower in towers:
            tower_pos = tower.get_component("position").position
            if tower_pos.distance_to(self.tower_placement_pos) < 40:
                return False
        
        return True
    
    def place_tower(self):
        """Place a tower at the current position."""
        # Purchase the tower
        if not self.economy_manager.purchase_tower(self.selected_tower_type):
            return
        
        # Create the tower
        tower = Tower(
            self.tower_placement_pos.x,
            self.tower_placement_pos.y,
            self.selected_tower_type
        )
        
        # Add the tower to the entity manager
        self.entity_manager.add_entity(tower)
