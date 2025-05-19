"""
Tower entity for the tower defense game.
"""
from src.entities.entity import Entity
from src.components.position import PositionComponent
from src.components.render import RenderComponent
from src.components.targeting import TargetingComponent
from src.config import TOWER_RANGE, TOWER_DAMAGE, TOWER_COOLDOWN


class Tower(Entity):
    """Tower entity that can target and attack enemies."""
    
    def __init__(self, x, y, tower_type="basic"):
        """Initialize a new Tower entity.
        
        Args:
            x (float): The x-coordinate of the tower.
            y (float): The y-coordinate of the tower.
            tower_type (str): The type of tower to create.
        """
        super().__init__()
        self.add_tag("tower")
        self.add_tag(tower_type)
        
        # Add position component
        self.add_component("position", PositionComponent(x, y))
        
        # Add render component
        if tower_type == "basic":
            self.add_component("render", RenderComponent(
                width=40,
                height=40,
                color=(0, 0, 255),
                layer=1
            ))
        else:
            # Can be extended for different tower types
            self.add_component("render", RenderComponent(
                width=40,
                height=40,
                color=(0, 0, 255),
                layer=1
            ))
        
        # Add targeting component
        self.add_component("targeting", TargetingComponent(
            range=TOWER_RANGE,
            damage=TOWER_DAMAGE,
            cooldown=TOWER_COOLDOWN
        ))
