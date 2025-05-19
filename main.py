"""
Main entry point for the tower defense game.
"""
import pygame
from src.core.game import Game
from src.scenes.game_scene import GameScene


def main():
    """Main function that initializes and runs the game."""
    # Create the game
    game = Game()
    
    # Create and add scenes
    game_scene = GameScene(game)
    game.scene_manager.add_scene("game", game_scene)
    
    # Set the initial scene
    game.scene_manager.set_scene("game")
    
    # Run the game
    game.run()


if __name__ == "__main__":
    main()
