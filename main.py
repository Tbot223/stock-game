#!/usr/bin/env python3
"""
Stock Game - Main Entry Point

A Python-based stock trading simulation game.
Run this file to start the game.
"""

import sys
import os

# Add the stock_game package to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from stock_game import Game


def main():
    """Main entry point for the stock game."""
    try:
        game = Game()
        game.start_game()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please check your installation and try again.")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())