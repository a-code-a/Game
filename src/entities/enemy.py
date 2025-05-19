"""
Enemy entity for the tower defense game.
"""
from src.entities.entity import Entity
from src.components.position import PositionComponent
from src.components.render import RenderComponent
from src.components.health import HealthComponent
from src.components.velocity import VelocityComponent
from src.components.path_following import PathFollowingComponent
from src.config import ENEMY_HEALTH, ENEMY_SPEED


class Enemy(Entity):
    """Enemy entity that follows a path and can be targeted by towers."""
    
    def __init__(self, x, y, path=None, enemy_type="basic"):
        """Initialize a new Enemy entity.
        
        Args:
            x (float): The x-coordinate of the enemy.
            y (float): The y-coordinate of the enemy.
            path (list): A list of Vector2 points defining the path.
            enemy_type (str): The type of enemy to create.
        """
        super().__init__()
        self.add_tag("enemy")
        self.add_tag(enemy_type)
        
        # Add position component
        self.add_component("position", PositionComponent(x, y))
        
        # Add render component
        if enemy_type == "basic":
            self.add_component("render", RenderComponent(
                width=30,
                height=30,
                color=(255, 0, 0),
                layer=1
            ))
        else:
            # Can be extended for different enemy types
            self.add_component("render", RenderComponent(
                width=30,
                height=30,
                color=(255, 0, 0),
                layer=1
            ))
        
        # Add health component
        self.add_component("health", HealthComponent(max_health=ENEMY_HEALTH))
        
        # Add velocity component
        self.add_component("velocity", VelocityComponent(max_speed=ENEMY_SPEED))
        
        # Add path following component
        self.add_component("path_following", PathFollowingComponent(
            path=path,
            speed=ENEMY_SPEED
        ))
