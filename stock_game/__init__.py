"""
Stock Game - A Python-based stock trading simulation game.

This package provides a console-based stock market simulation where players
can buy and sell stocks, manage their portfolio, and experience market dynamics.
"""

__version__ = "1.0.0"
__author__ = "Stock Game Developer"

from .game import Game
from .player import Player
from .stock import Stock
from .market import Market

__all__ = ["Game", "Player", "Stock", "Market"]