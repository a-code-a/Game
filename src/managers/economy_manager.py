"""
Economy manager for handling resources in the tower defense game.
"""
from src.config import STARTING_RESOURCES, TOWER_COST, ENEMY_REWARD


class EconomyManager:
    """Manager for handling resources in the tower defense game."""
    
    def __init__(self):
        """Initialize a new EconomyManager."""
        self.resources = STARTING_RESOURCES
        self.tower_costs = {
            "basic": TOWER_COST,
            # Add more tower types and costs here
        }
    
    def get_resources(self):
        """Get the current amount of resources.
        
        Returns:
            int: The current amount of resources.
        """
        return self.resources
    
    def add_resources(self, amount):
        """Add resources to the player's total.
        
        Args:
            amount (int): The amount of resources to add.
            
        Returns:
            int: The new total amount of resources.
        """
        self.resources += amount
        return self.resources
    
    def can_afford(self, tower_type="basic"):
        """Check if the player can afford to build a tower.
        
        Args:
            tower_type (str): The type of tower to check.
            
        Returns:
            bool: True if the player can afford the tower, False otherwise.
        """
        cost = self.tower_costs.get(tower_type, TOWER_COST)
        return self.resources >= cost
    
    def purchase_tower(self, tower_type="basic"):
        """Attempt to purchase a tower.
        
        Args:
            tower_type (str): The type of tower to purchase.
            
        Returns:
            bool: True if the purchase was successful, False otherwise.
        """
        cost = self.tower_costs.get(tower_type, TOWER_COST)
        if self.resources >= cost:
            self.resources -= cost
            return True
        return False
    
    def reward_for_enemy(self, enemy_type="basic"):
        """Get the reward for defeating an enemy.
        
        Args:
            enemy_type (str): The type of enemy defeated.
            
        Returns:
            int: The reward amount.
        """
        # Can be extended for different enemy types
        return ENEMY_REWARD
