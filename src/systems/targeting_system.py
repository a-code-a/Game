"""
Targeting system for the Entity Component System.
"""
from src.systems.system import System
from src.entities.projectile import Projectile


class TargetingSystem(System):
    """System that handles tower targeting and firing at enemies."""
    
    def __init__(self, entity_manager):
        """Initialize a new TargetingSystem.
        
        Args:
            entity_manager: The entity manager to use for creating projectiles.
        """
        super().__init__()
        self.entity_manager = entity_manager
        self.enemies = []
    
    def set_enemies(self, enemies):
        """Set the list of enemies that can be targeted.
        
        Args:
            enemies (list): The list of enemy entities.
        """
        self.enemies = enemies
    
    def process(self, dt):
        """Process all towers with targeting components.
        
        Args:
            dt (float): The time delta since the last update in seconds.
        """
        for entity in self.entities:
            if not entity.active:
                continue
                
            position_component = entity.get_component("position")
            targeting_component = entity.get_component("targeting")
            
            if not position_component or not targeting_component:
                continue
            
            # Skip if the tower is on cooldown
            if not targeting_component.can_attack():
                continue
            
            # Find the closest enemy in range
            tower_pos = position_component.position
            closest_enemy = None
            closest_distance = float('inf')
            
            for enemy in self.enemies:
                if not enemy.active:
                    continue
                    
                enemy_position = enemy.get_component("position")
                if not enemy_position:
                    continue
                
                enemy_pos = enemy_position.position
                distance = tower_pos.distance_to(enemy_pos)
                
                if distance <= targeting_component.range and distance < closest_distance:
                    closest_enemy = enemy
                    closest_distance = distance
            
            # If an enemy is in range, attack it
            if closest_enemy:
                # Register the attack (starts cooldown)
                targeting_component.attack()
                
                # Create a projectile
                enemy_pos = closest_enemy.get_component("position").position
                projectile = Projectile(
                    tower_pos.x,
                    tower_pos.y,
                    closest_enemy,
                    targeting_component.damage
                )
                
                # Calculate direction to enemy
                direction = (enemy_pos - tower_pos).normalize()
                projectile.get_component("velocity").set_velocity(
                    direction.x * projectile.get_component("velocity").max_speed,
                    direction.y * projectile.get_component("velocity").max_speed
                )
                
                # Add the projectile to the entity manager
                self.entity_manager.add_entity(projectile)
    
    def should_process(self, entity):
        """Check if this system should process the given entity.
        
        Args:
            entity (Entity): The entity to check.
            
        Returns:
            bool: True if the entity should be processed, False otherwise.
        """
        return (entity.active and
                entity.has_component("position") and
                entity.has_component("targeting"))
