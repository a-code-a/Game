"""
Main entry point for the tower defense game.
"""
import pygame
from src.core.game import Game
from src.scenes.game_scene import GameScene
from src.scenes.menu_scene import MenuScene


def main():
    """Main function that initializes and runs the game."""
    # Create the game
    game = Game()

    # Create and add scenes
    menu_scene = MenuScene(game)
    game_scene = GameScene(game)

    game.scene_manager.add_scene("menu", menu_scene)
    game.scene_manager.add_scene("game", game_scene)

    # Set the initial scene
    game.scene_manager.set_scene("menu")

    # Run the game
    game.run()


if __name__ == "__main__":
    main()
