"""
Collision system for the Entity Component System.
"""
from src.systems.system import System


class CollisionSystem(System):
    """System that handles collisions between entities."""
    
    def __init__(self, entity_manager):
        """Initialize a new CollisionSystem.
        
        Args:
            entity_manager: The entity manager to use for removing entities.
        """
        super().__init__()
        self.entity_manager = entity_manager
        self.projectiles = []
        self.enemies = []
    
    def set_projectiles(self, projectiles):
        """Set the list of projectiles to check for collisions.
        
        Args:
            projectiles (list): The list of projectile entities.
        """
        self.projectiles = projectiles
    
    def set_enemies(self, enemies):
        """Set the list of enemies to check for collisions.
        
        Args:
            enemies (list): The list of enemy entities.
        """
        self.enemies = enemies
    
    def process(self, dt):
        """Check for collisions between projectiles and enemies.
        
        Args:
            dt (float): The time delta since the last update in seconds.
        """
        # Check each projectile against each enemy
        for projectile in self.projectiles:
            if not projectile.active:
                continue
                
            projectile_pos = projectile.get_component("position")
            projectile_render = projectile.get_component("render")
            
            if not projectile_pos or not projectile_render:
                continue
            
            projectile_rect = projectile_render.get_rect(projectile_pos.position)
            
            # Check if the projectile has hit its target
            target_entity = projectile.target_entity
            if target_entity and target_entity.active:
                target_pos = target_entity.get_component("position")
                target_render = target_entity.get_component("render")
                
                if target_pos and target_render:
                    target_rect = target_render.get_rect(target_pos.position)
                    
                    # Check for collision
                    if projectile_rect.colliderect(target_rect):
                        # Apply damage to the target
                        health_component = target_entity.get_component("health")
                        if health_component:
                            is_alive = health_component.take_damage(projectile.damage)
                            if not is_alive:
                                # Target is dead, remove it
                                self.entity_manager.remove_entity(target_entity)
                        
                        # Remove the projectile
                        self.entity_manager.remove_entity(projectile)
                        break
            
            # Check for collisions with other enemies if the target is gone
            if not target_entity or not target_entity.active:
                for enemy in self.enemies:
                    if not enemy.active:
                        continue
                        
                    enemy_pos = enemy.get_component("position")
                    enemy_render = enemy.get_component("render")
                    
                    if not enemy_pos or not enemy_render:
                        continue
                    
                    enemy_rect = enemy_render.get_rect(enemy_pos.position)
                    
                    # Check for collision
                    if projectile_rect.colliderect(enemy_rect):
                        # Apply damage to the enemy
                        health_component = enemy.get_component("health")
                        if health_component:
                            is_alive = health_component.take_damage(projectile.damage)
                            if not is_alive:
                                # Enemy is dead, remove it
                                self.entity_manager.remove_entity(enemy)
                        
                        # Remove the projectile
                        self.entity_manager.remove_entity(projectile)
                        break
