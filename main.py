"""
Main entry point for Tower Simulator
"""
import sys
import os

# Add the project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tower_simulator.game import TowerSimulatorGame


def main():
    """Run the Tower Simulator"""
    print("Starting Tower Simulator...")
    game = TowerSimulatorGame()
    game.run()


if __name__ == "__main__":
    main()
