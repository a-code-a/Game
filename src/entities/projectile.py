"""
Projectile entity for the tower defense game.
"""
from src.entities.entity import Entity
from src.components.position import PositionComponent
from src.components.render import RenderComponent
from src.components.velocity import VelocityComponent
from src.config import PROJECTILE_SPEED, PROJECTILE_RADIUS


class Projectile(Entity):
    """Projectile entity that moves towards a target and deals damage on impact."""
    
    def __init__(self, x, y, target_entity, damage, projectile_type="basic"):
        """Initialize a new Projectile entity.
        
        Args:
            x (float): The x-coordinate of the projectile.
            y (float): The y-coordinate of the projectile.
            target_entity (Entity): The target entity to move towards.
            damage (float): The damage this projectile deals on impact.
            projectile_type (str): The type of projectile to create.
        """
        super().__init__()
        self.add_tag("projectile")
        self.add_tag(projectile_type)
        
        # Store target and damage
        self.target_entity = target_entity
        self.damage = damage
        
        # Add position component
        self.add_component("position", PositionComponent(x, y))
        
        # Add render component
        if projectile_type == "basic":
            self.add_component("render", RenderComponent(
                width=PROJECTILE_RADIUS * 2,
                height=PROJECTILE_RADIUS * 2,
                color=(255, 255, 0),
                layer=2
            ))
        else:
            # Can be extended for different projectile types
            self.add_component("render", RenderComponent(
                width=PROJECTILE_RADIUS * 2,
                height=PROJECTILE_RADIUS * 2,
                color=(255, 255, 0),
                layer=2
            ))
        
        # Add velocity component
        self.add_component("velocity", VelocityComponent(max_speed=PROJECTILE_SPEED))
