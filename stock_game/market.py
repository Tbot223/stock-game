"""
Market class for managing the stock market simulation.
"""

import random
from typing import Dict, List
from .stock import Stock


class Market:
    """Manages the stock market with multiple stocks and market events."""
    
    def __init__(self):
        """Initialize the market with default stocks."""
        self.stocks: Dict[str, Stock] = {}
        self.day = 1
        self.market_sentiment = 'NEUTRAL'  # BULL, BEAR, NEUTRAL
        self.news_events: List[str] = []
        
        # Initialize with some default stocks
        self._initialize_default_stocks()
    
    def _initialize_default_stocks(self):
        """Create default stocks for the market."""
        default_stocks = [
            ('AAPL', 'Apple Inc.', 150.00, 0.08),
            ('GOOGL', 'Alphabet Inc.', 2500.00, 0.10),
            ('MSFT', 'Microsoft Corporation', 300.00, 0.07),
            ('TSLA', 'Tesla Inc.', 800.00, 0.15),
            ('AMZN', 'Amazon.com Inc.', 3200.00, 0.09),
            ('META', 'Meta Platforms Inc.', 320.00, 0.12),
            ('NFLX', 'Netflix Inc.', 400.00, 0.11),
            ('NVDA', 'NVIDIA Corporation', 450.00, 0.13),
        ]
        
        for symbol, name, price, volatility in default_stocks:
            self.stocks[symbol] = Stock(symbol, name, price, volatility)
    
    def add_stock(self, symbol: str, name: str, initial_price: float, volatility: float = 0.05):
        """
        Add a new stock to the market.
        
        Args:
            symbol: Stock ticker symbol
            name: Company name
            initial_price: Starting price
            volatility: Price volatility factor
        """
        self.stocks[symbol] = Stock(symbol, name, initial_price, volatility)
    
    def update_market(self) -> List[str]:
        """
        Update all stock prices and generate market events.
        
        Returns:
            List of news events for this update
        """
        # Determine market sentiment influence
        sentiment_multiplier = self._get_sentiment_multiplier()
        
        # Update all stock prices
        for stock in self.stocks.values():
            # Apply market sentiment to volatility
            original_volatility = stock.volatility
            stock.volatility *= sentiment_multiplier
            stock.update_price()
            stock.volatility = original_volatility  # Reset to original
        
        # Generate random market events
        events = self._generate_market_events()
        self.news_events.extend(events)
        
        # Keep only recent news (last 5 events)
        if len(self.news_events) > 5:
            self.news_events = self.news_events[-5:]
        
        self.day += 1
        
        # Occasionally change market sentiment
        if random.random() < 0.1:  # 10% chance
            self._change_market_sentiment()
        
        return events
    
    def _get_sentiment_multiplier(self) -> float:
        """Get volatility multiplier based on market sentiment."""
        if self.market_sentiment == 'BULL':
            return 0.8  # Less volatility, generally upward trend
        elif self.market_sentiment == 'BEAR':
            return 1.3  # More volatility, generally downward trend
        else:
            return 1.0  # Normal volatility
    
    def _change_market_sentiment(self):
        """Randomly change market sentiment."""
        sentiments = ['BULL', 'BEAR', 'NEUTRAL']
        old_sentiment = self.market_sentiment
        
        # Slightly favor staying in current sentiment
        if random.random() < 0.4:
            return
        
        self.market_sentiment = random.choice(sentiments)
        
        if self.market_sentiment != old_sentiment:
            event = f"Market sentiment changed from {old_sentiment} to {self.market_sentiment}"
            self.news_events.append(event)
    
    def _generate_market_events(self) -> List[str]:
        """Generate random market events and news."""
        events = []
        
        # 30% chance of generating an event
        if random.random() < 0.3:
            event_types = [
                "earnings_report",
                "market_news",
                "economic_indicator",
                "company_news"
            ]
            
            event_type = random.choice(event_types)
            
            if event_type == "earnings_report":
                stock = random.choice(list(self.stocks.values()))
                if random.random() < 0.6:  # 60% chance positive
                    events.append(f"{stock.name} reports better than expected earnings")
                    # Boost this stock's price
                    stock.current_price *= random.uniform(1.02, 1.08)
                else:
                    events.append(f"{stock.name} misses earnings expectations")
                    # Lower this stock's price
                    stock.current_price *= random.uniform(0.92, 0.98)
                    
                stock.current_price = round(max(0.01, stock.current_price), 2)
            
            elif event_type == "market_news":
                news_events = [
                    "Federal Reserve announces interest rate decision",
                    "New trade agreements boost market confidence",
                    "Tech sector shows strong growth indicators",
                    "Consumer spending reports released",
                    "Global market volatility affects trading"
                ]
                events.append(random.choice(news_events))
            
            elif event_type == "economic_indicator":
                indicators = [
                    "Unemployment rate drops to new low",
                    "GDP growth exceeds expectations",
                    "Inflation concerns impact market",
                    "Consumer confidence index rises",
                    "Manufacturing data shows strong growth"
                ]
                events.append(random.choice(indicators))
            
            elif event_type == "company_news":
                stock = random.choice(list(self.stocks.values()))
                company_events = [
                    f"{stock.name} announces new product launch",
                    f"{stock.name} forms strategic partnership",
                    f"{stock.name} completes major acquisition",
                    f"{stock.name} faces regulatory investigation",
                    f"{stock.name} CEO announces retirement"
                ]
                events.append(random.choice(company_events))
        
        return events
    
    def get_market_summary(self) -> str:
        """
        Get a formatted summary of the current market state.
        
        Returns:
            Formatted market summary string
        """
        lines = [f"\n=== Market Day {self.day} ==="]
        lines.append(f"Market Sentiment: {self.market_sentiment}")
        
        # Market performance
        gainers = []
        losers = []
        
        for stock in self.stocks.values():
            change_abs, change_pct = stock.get_price_change()
            if change_pct > 0:
                gainers.append((stock.symbol, change_pct))
            elif change_pct < 0:
                losers.append((stock.symbol, change_pct))
        
        # Sort by percentage change
        gainers.sort(key=lambda x: x[1], reverse=True)
        losers.sort(key=lambda x: x[1])
        
        if gainers:
            lines.append(f"\nTop Gainers:")
            for symbol, pct in gainers[:3]:
                lines.append(f"  {symbol}: +{pct:.2f}%")
        
        if losers:
            lines.append(f"\nTop Losers:")
            for symbol, pct in losers[:3]:
                lines.append(f"  {symbol}: {pct:.2f}%")
        
        # Recent news
        if self.news_events:
            lines.append(f"\nRecent News:")
            for event in self.news_events[-3:]:  # Show last 3 events
                lines.append(f"  • {event}")
        
        return "\n".join(lines)
    
    def get_stock_list(self) -> str:
        """Get a formatted list of all available stocks."""
        lines = ["\n=== Available Stocks ==="]
        
        for stock in sorted(self.stocks.values(), key=lambda s: s.symbol):
            lines.append(str(stock))
        
        return "\n".join(lines)
    
    def get_stock(self, symbol: str) -> Stock:
        """Get a stock by its symbol."""
        return self.stocks.get(symbol.upper())
    
    def get_all_stocks(self) -> Dict[str, Stock]:
        """Get all stocks in the market."""
        return self.stocks.copy()