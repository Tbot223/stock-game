#!/usr/bin/env python3
"""
Basic tests for the Stock Game project.
"""

import sys
import os
import unittest

# Add the parent directory to the path to import stock_game
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stock_game import Stock, Player, Market, Game


class TestStock(unittest.TestCase):
    """Test the Stock class."""
    
    def setUp(self):
        """Set up test stock."""
        self.stock = Stock("AAPL", "Apple Inc.", 150.0, 0.05)
    
    def test_stock_creation(self):
        """Test stock creation."""
        self.assertEqual(self.stock.symbol, "AAPL")
        self.assertEqual(self.stock.name, "Apple Inc.")
        self.assertEqual(self.stock.current_price, 150.0)
        self.assertEqual(self.stock.volatility, 0.05)
        self.assertEqual(len(self.stock.price_history), 1)
    
    def test_price_update(self):
        """Test price update functionality."""
        original_price = self.stock.current_price
        new_price = self.stock.update_price()
        
        self.assertIsInstance(new_price, float)
        self.assertGreater(new_price, 0)
        self.assertEqual(len(self.stock.price_history), 2)
    
    def test_price_change_calculation(self):
        """Test price change calculation."""
        # Initial state should show no change
        abs_change, pct_change = self.stock.get_price_change()
        self.assertEqual(abs_change, 0.0)
        self.assertEqual(pct_change, 0.0)
        
        # After price update, should show change
        self.stock.update_price()
        abs_change, pct_change = self.stock.get_price_change()
        self.assertIsInstance(abs_change, float)
        self.assertIsInstance(pct_change, float)


class TestPlayer(unittest.TestCase):
    """Test the Player class."""
    
    def setUp(self):
        """Set up test player and stock."""
        self.player = Player("Test Player", 10000.0)
        self.stock = Stock("AAPL", "Apple Inc.", 100.0, 0.05)
    
    def test_player_creation(self):
        """Test player creation."""
        self.assertEqual(self.player.name, "Test Player")
        self.assertEqual(self.player.cash, 10000.0)
        self.assertEqual(self.player.starting_cash, 10000.0)
        self.assertEqual(len(self.player.portfolio), 0)
    
    def test_buy_stock_success(self):
        """Test successful stock purchase."""
        result = self.player.buy_stock(self.stock, 10)
        
        self.assertTrue(result)
        self.assertEqual(self.player.cash, 9000.0)
        self.assertEqual(self.player.portfolio["AAPL"], 10)
        self.assertEqual(len(self.player.transaction_history), 1)
    
    def test_buy_stock_insufficient_funds(self):
        """Test stock purchase with insufficient funds."""
        result = self.player.buy_stock(self.stock, 200)  # Would cost $20,000
        
        self.assertFalse(result)
        self.assertEqual(self.player.cash, 10000.0)
        self.assertEqual(len(self.player.portfolio), 0)
    
    def test_sell_stock_success(self):
        """Test successful stock sale."""
        # First buy some stock
        self.player.buy_stock(self.stock, 10)
        
        # Then sell some
        result = self.player.sell_stock(self.stock, 5)
        
        self.assertTrue(result)
        self.assertEqual(self.player.cash, 9500.0)  # 10000 - 1000 + 500
        self.assertEqual(self.player.portfolio["AAPL"], 5)
        self.assertEqual(len(self.player.transaction_history), 2)
    
    def test_sell_stock_insufficient_shares(self):
        """Test stock sale with insufficient shares."""
        result = self.player.sell_stock(self.stock, 5)
        
        self.assertFalse(result)
        self.assertEqual(self.player.cash, 10000.0)
        self.assertEqual(len(self.player.portfolio), 0)
    
    def test_portfolio_value_calculation(self):
        """Test portfolio value calculation."""
        stocks = {"AAPL": self.stock}
        
        # Initial value should be just cash
        initial_value = self.player.get_portfolio_value(stocks)
        self.assertEqual(initial_value, 10000.0)
        
        # After buying stock
        self.player.buy_stock(self.stock, 10)
        new_value = self.player.get_portfolio_value(stocks)
        self.assertEqual(new_value, 10000.0)  # $9000 cash + $1000 stock


class TestMarket(unittest.TestCase):
    """Test the Market class."""
    
    def setUp(self):
        """Set up test market."""
        self.market = Market()
    
    def test_market_creation(self):
        """Test market creation with default stocks."""
        self.assertGreater(len(self.market.stocks), 0)
        self.assertEqual(self.market.day, 1)
        self.assertEqual(self.market.market_sentiment, 'NEUTRAL')
    
    def test_stock_retrieval(self):
        """Test getting stocks from market."""
        stock = self.market.get_stock("AAPL")
        self.assertIsNotNone(stock)
        self.assertEqual(stock.symbol, "AAPL")
        
        # Test case insensitive
        stock = self.market.get_stock("aapl")
        self.assertIsNotNone(stock)
        
        # Test non-existent stock
        stock = self.market.get_stock("INVALID")
        self.assertIsNone(stock)
    
    def test_market_update(self):
        """Test market update functionality."""
        initial_day = self.market.day
        events = self.market.update_market()
        
        self.assertEqual(self.market.day, initial_day + 1)
        self.assertIsInstance(events, list)
    
    def test_add_stock(self):
        """Test adding new stock to market."""
        initial_count = len(self.market.stocks)
        self.market.add_stock("TEST", "Test Company", 50.0, 0.1)
        
        self.assertEqual(len(self.market.stocks), initial_count + 1)
        test_stock = self.market.get_stock("TEST")
        self.assertIsNotNone(test_stock)
        self.assertEqual(test_stock.name, "Test Company")


class TestGame(unittest.TestCase):
    """Test the Game class."""
    
    def test_game_creation(self):
        """Test game creation."""
        game = Game()
        
        self.assertIsNone(game.player)
        self.assertIsNotNone(game.market)
        self.assertFalse(game.running)
        self.assertFalse(game.auto_mode)


def run_tests():
    """Run all tests."""
    unittest.main(verbosity=2)


if __name__ == "__main__":
    run_tests()