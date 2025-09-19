"""
Player class for managing user portfolio and game state.
"""

from typing import Dict, List, Tuple
from .stock import Stock


class Player:
    """Represents a player in the stock game with portfolio management."""
    
    def __init__(self, name: str, starting_cash: float = 10000.0):
        """
        Initialize a player.
        
        Args:
            name: Player's name
            starting_cash: Initial cash amount
        """
        self.name = name
        self.cash = starting_cash
        self.starting_cash = starting_cash
        self.portfolio: Dict[str, int] = {}  # symbol -> quantity
        self.transaction_history: List[Dict] = []
        
    def buy_stock(self, stock: Stock, quantity: int) -> bool:
        """
        Buy stocks if player has enough cash.
        
        Args:
            stock: Stock object to buy
            quantity: Number of shares to buy
            
        Returns:
            True if purchase successful, False otherwise
        """
        total_cost = stock.current_price * quantity
        
        if total_cost > self.cash:
            return False
            
        self.cash -= total_cost
        self.cash = round(self.cash, 2)
        
        if stock.symbol in self.portfolio:
            self.portfolio[stock.symbol] += quantity
        else:
            self.portfolio[stock.symbol] = quantity
            
        # Record transaction
        self.transaction_history.append({
            'type': 'BUY',
            'symbol': stock.symbol,
            'quantity': quantity,
            'price': stock.current_price,
            'total': total_cost
        })
        
        return True
    
    def sell_stock(self, stock: Stock, quantity: int) -> bool:
        """
        Sell stocks if player owns enough shares.
        
        Args:
            stock: Stock object to sell
            quantity: Number of shares to sell
            
        Returns:
            True if sale successful, False otherwise
        """
        if stock.symbol not in self.portfolio or self.portfolio[stock.symbol] < quantity:
            return False
            
        total_value = stock.current_price * quantity
        self.cash += total_value
        self.cash = round(self.cash, 2)
        
        self.portfolio[stock.symbol] -= quantity
        
        # Remove from portfolio if no shares left
        if self.portfolio[stock.symbol] == 0:
            del self.portfolio[stock.symbol]
            
        # Record transaction
        self.transaction_history.append({
            'type': 'SELL',
            'symbol': stock.symbol,
            'quantity': quantity,
            'price': stock.current_price,
            'total': total_value
        })
        
        return True
    
    def get_portfolio_value(self, stocks: Dict[str, Stock]) -> float:
        """
        Calculate total portfolio value.
        
        Args:
            stocks: Dictionary of available stocks
            
        Returns:
            Total portfolio value including cash
        """
        portfolio_value = 0.0
        
        for symbol, quantity in self.portfolio.items():
            if symbol in stocks:
                portfolio_value += stocks[symbol].current_price * quantity
                
        return round(portfolio_value + self.cash, 2)
    
    def get_holdings_value(self, stocks: Dict[str, Stock]) -> float:
        """
        Calculate value of stock holdings only (excluding cash).
        
        Args:
            stocks: Dictionary of available stocks
            
        Returns:
            Total value of stock holdings
        """
        holdings_value = 0.0
        
        for symbol, quantity in self.portfolio.items():
            if symbol in stocks:
                holdings_value += stocks[symbol].current_price * quantity
                
        return round(holdings_value, 2)
    
    def get_net_worth_change(self, stocks: Dict[str, Stock]) -> Tuple[float, float]:
        """
        Calculate change in net worth from starting amount.
        
        Args:
            stocks: Dictionary of available stocks
            
        Returns:
            Tuple of (absolute_change, percentage_change)
        """
        current_value = self.get_portfolio_value(stocks)
        absolute_change = current_value - self.starting_cash
        percentage_change = (absolute_change / self.starting_cash) * 100
        
        return round(absolute_change, 2), round(percentage_change, 2)
    
    def get_portfolio_summary(self, stocks: Dict[str, Stock]) -> str:
        """
        Get a formatted summary of the portfolio.
        
        Args:
            stocks: Dictionary of available stocks
            
        Returns:
            Formatted portfolio summary string
        """
        lines = [f"\n=== {self.name}'s Portfolio ==="]
        lines.append(f"Cash: ${self.cash:,.2f}")
        
        if not self.portfolio:
            lines.append("No stock holdings")
        else:
            lines.append("\nStock Holdings:")
            total_holdings = 0
            
            for symbol, quantity in self.portfolio.items():
                if symbol in stocks:
                    stock = stocks[symbol]
                    value = stock.current_price * quantity
                    total_holdings += value
                    lines.append(f"  {symbol}: {quantity} shares @ ${stock.current_price:.2f} = ${value:,.2f}")
            
            lines.append(f"Total Holdings Value: ${total_holdings:,.2f}")
        
        total_value = self.get_portfolio_value(stocks)
        change_abs, change_pct = self.get_net_worth_change(stocks)
        
        lines.append(f"Total Portfolio Value: ${total_value:,.2f}")
        lines.append(f"Net Change: ${change_abs:+,.2f} ({change_pct:+.2f}%)")
        
        return "\n".join(lines)
    
    def can_afford(self, stock: Stock, quantity: int) -> bool:
        """Check if player can afford to buy specified quantity of stock."""
        return (stock.current_price * quantity) <= self.cash
    
    def owns_stock(self, symbol: str, quantity: int = 1) -> bool:
        """Check if player owns at least the specified quantity of stock."""
        return symbol in self.portfolio and self.portfolio[symbol] >= quantity