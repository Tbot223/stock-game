"""
Stock class for representing individual stocks in the game.
"""

import random
from typing import List, Dict


class Stock:
    """Represents a single stock with price and historical data."""
    
    def __init__(self, symbol: str, name: str, initial_price: float, volatility: float = 0.05):
        """
        Initialize a stock.
        
        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL')
            name: Company name
            initial_price: Starting price of the stock
            volatility: Price volatility factor (0.0 to 1.0)
        """
        self.symbol = symbol
        self.name = name
        self.current_price = initial_price
        self.volatility = volatility
        self.price_history: List[float] = [initial_price]
        
    def update_price(self) -> float:
        """
        Update stock price based on market conditions and volatility.
        
        Returns:
            New stock price
        """
        # Generate random price change based on volatility
        change_percent = random.uniform(-self.volatility, self.volatility)
        price_change = self.current_price * change_percent
        
        # Ensure price doesn't go below $0.01
        new_price = max(0.01, self.current_price + price_change)
        
        self.current_price = round(new_price, 2)
        self.price_history.append(self.current_price)
        
        # Keep only last 50 price points for history
        if len(self.price_history) > 50:
            self.price_history.pop(0)
            
        return self.current_price
    
    def get_price_change(self) -> tuple[float, float]:
        """
        Get the price change from previous price.
        
        Returns:
            Tuple of (absolute_change, percentage_change)
        """
        if len(self.price_history) < 2:
            return 0.0, 0.0
            
        prev_price = self.price_history[-2]
        absolute_change = self.current_price - prev_price
        percentage_change = (absolute_change / prev_price) * 100
        
        return round(absolute_change, 2), round(percentage_change, 2)
    
    def get_trend(self, periods: int = 5) -> str:
        """
        Get the trend direction over the last few periods.
        
        Args:
            periods: Number of periods to analyze
            
        Returns:
            'UP', 'DOWN', or 'STABLE'
        """
        if len(self.price_history) < periods:
            return 'STABLE'
            
        recent_prices = self.price_history[-periods:]
        avg_early = sum(recent_prices[:periods//2]) / (periods//2)
        avg_late = sum(recent_prices[periods//2:]) / (periods - periods//2)
        
        if avg_late > avg_early * 1.02:  # 2% threshold
            return 'UP'
        elif avg_late < avg_early * 0.98:
            return 'DOWN'
        else:
            return 'STABLE'
    
    def __str__(self) -> str:
        """String representation of the stock."""
        change_abs, change_pct = self.get_price_change()
        trend = self.get_trend()
        
        return f"{self.symbol}: ${self.current_price:.2f} ({change_pct:+.2f}%) [{trend}]"
    
    def __repr__(self) -> str:
        """Detailed representation of the stock."""
        return f"Stock(symbol='{self.symbol}', name='{self.name}', price=${self.current_price:.2f})"