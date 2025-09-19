"""
Main game class that orchestrates the stock trading simulation.
"""

import sys
import time
from typing import Dict, Optional
from .player import Player
from .market import Market
from .stock import Stock


class Game:
    """Main game controller for the stock trading simulation."""
    
    def __init__(self):
        """Initialize the game."""
        self.player: Optional[Player] = None
        self.market = Market()
        self.running = False
        self.auto_mode = False
    
    def start_game(self):
        """Start the main game loop."""
        print("=" * 50)
        print("📈 Welcome to Stock Game! 📈")
        print("=" * 50)
        print("A Python-based stock trading simulation")
        print("Build your portfolio and become a trading master!")
        print()
        
        # Get player name and starting cash
        name = input("Enter your name: ").strip()
        if not name:
            name = "Player"
        
        try:
            cash_input = input("Enter starting cash (default $10,000): ").strip()
            starting_cash = float(cash_input) if cash_input else 10000.0
        except ValueError:
            starting_cash = 10000.0
        
        self.player = Player(name, starting_cash)
        self.running = True
        
        print(f"\nWelcome {name}! You start with ${starting_cash:,.2f}")
        print("Type 'help' for available commands.")
        
        # Show initial market state
        self._show_market_overview()
        
        # Main game loop
        while self.running:
            try:
                if not self.auto_mode:
                    command = input("\n> ").strip().lower()
                    self._handle_command(command)
                else:
                    time.sleep(2)  # Auto mode delay
                    self._auto_trade()
                    
            except KeyboardInterrupt:
                print("\n\nGame interrupted. Thanks for playing!")
                break
            except Exception as e:
                print(f"\nError: {e}")
                print("Type 'help' for available commands.")
    
    def _handle_command(self, command: str):
        """Handle user commands."""
        if not command:
            return
            
        parts = command.split()
        cmd = parts[0]
        
        if cmd == 'help' or cmd == 'h':
            self._show_help()
        elif cmd == 'market' or cmd == 'm':
            self._show_market_overview()
        elif cmd == 'stocks' or cmd == 's':
            self._show_stocks()
        elif cmd == 'portfolio' or cmd == 'p':
            self._show_portfolio()
        elif cmd == 'buy' or cmd == 'b':
            self._handle_buy(parts[1:] if len(parts) > 1 else [])
        elif cmd == 'sell':
            self._handle_sell(parts[1:] if len(parts) > 1 else [])
        elif cmd == 'next' or cmd == 'n':
            self._next_day()
        elif cmd == 'auto':
            self._toggle_auto_mode()
        elif cmd == 'quit' or cmd == 'q' or cmd == 'exit':
            self._quit_game()
        else:
            print(f"Unknown command: {cmd}. Type 'help' for available commands.")
    
    def _show_help(self):
        """Display help information."""
        print("\n=== Available Commands ===")
        print("help (h)           - Show this help message")
        print("market (m)         - Show market overview and news")
        print("stocks (s)         - Show all available stocks")
        print("portfolio (p)      - Show your portfolio")
        print("buy <symbol> <qty> - Buy stocks (e.g., 'buy AAPL 10')")
        print("sell <symbol> <qty>- Sell stocks (e.g., 'sell AAPL 5')")
        print("next (n)           - Advance to next trading day")
        print("auto               - Toggle automatic trading mode")
        print("quit (q)           - Exit the game")
        print("\nTip: You can use abbreviated commands (h, m, s, p, b, n, q)")
    
    def _show_market_overview(self):
        """Display market summary and recent news."""
        print(self.market.get_market_summary())
    
    def _show_stocks(self):
        """Display all available stocks."""
        print(self.market.get_stock_list())
    
    def _show_portfolio(self):
        """Display player's portfolio."""
        print(self.player.get_portfolio_summary(self.market.get_all_stocks()))
    
    def _handle_buy(self, args: list):
        """Handle buy command."""
        if len(args) != 2:
            print("Usage: buy <symbol> <quantity>")
            print("Example: buy AAPL 10")
            return
        
        symbol = args[0].upper()
        try:
            quantity = int(args[1])
        except ValueError:
            print("Quantity must be a number.")
            return
        
        if quantity <= 0:
            print("Quantity must be positive.")
            return
        
        stock = self.market.get_stock(symbol)
        if not stock:
            print(f"Stock {symbol} not found.")
            return
        
        total_cost = stock.current_price * quantity
        
        if not self.player.can_afford(stock, quantity):
            print(f"Insufficient funds. Need ${total_cost:,.2f}, have ${self.player.cash:,.2f}")
            return
        
        if self.player.buy_stock(stock, quantity):
            print(f"✅ Bought {quantity} shares of {symbol} at ${stock.current_price:.2f} each")
            print(f"💰 Total cost: ${total_cost:,.2f}")
            print(f"💵 Remaining cash: ${self.player.cash:,.2f}")
        else:
            print("❌ Purchase failed.")
    
    def _handle_sell(self, args: list):
        """Handle sell command."""
        if len(args) != 2:
            print("Usage: sell <symbol> <quantity>")
            print("Example: sell AAPL 5")
            return
        
        symbol = args[0].upper()
        try:
            quantity = int(args[1])
        except ValueError:
            print("Quantity must be a number.")
            return
        
        if quantity <= 0:
            print("Quantity must be positive.")
            return
        
        stock = self.market.get_stock(symbol)
        if not stock:
            print(f"Stock {symbol} not found.")
            return
        
        if not self.player.owns_stock(symbol, quantity):
            owned = self.player.portfolio.get(symbol, 0)
            print(f"Insufficient shares. You own {owned} shares of {symbol}.")
            return
        
        total_value = stock.current_price * quantity
        
        if self.player.sell_stock(stock, quantity):
            print(f"✅ Sold {quantity} shares of {symbol} at ${stock.current_price:.2f} each")
            print(f"💰 Total received: ${total_value:,.2f}")
            print(f"💵 Current cash: ${self.player.cash:,.2f}")
        else:
            print("❌ Sale failed.")
    
    def _next_day(self):
        """Advance to the next trading day."""
        print("\n⏰ Advancing to next trading day...")
        
        # Update market
        news = self.market.update_market()
        
        print(f"\n📊 Day {self.market.day}")
        
        # Show any news
        if news:
            print("📰 Breaking News:")
            for event in news:
                print(f"  • {event}")
        
        # Show portfolio performance
        change_abs, change_pct = self.player.get_net_worth_change(self.market.get_all_stocks())
        print(f"\n💼 Portfolio Performance:")
        print(f"Net Worth: ${self.player.get_portfolio_value(self.market.get_all_stocks()):,.2f}")
        print(f"Change: ${change_abs:+,.2f} ({change_pct:+.2f}%)")
    
    def _auto_trade(self):
        """Automatic trading for demo purposes."""
        print("\n🤖 Auto-trading mode...")
        
        # Simple random trading strategy
        import random
        
        # 50% chance to make a trade
        if random.random() < 0.5:
            stocks = list(self.market.stocks.values())
            stock = random.choice(stocks)
            
            # Decide to buy or sell
            if random.random() < 0.6 and self.player.cash > stock.current_price:
                # Try to buy
                max_quantity = int(self.player.cash / stock.current_price)
                if max_quantity > 0:
                    quantity = random.randint(1, min(5, max_quantity))
                    if self.player.buy_stock(stock, quantity):
                        print(f"🤖 Auto-bought {quantity} shares of {stock.symbol}")
            
            elif self.player.owns_stock(stock.symbol):
                # Try to sell
                owned = self.player.portfolio[stock.symbol]
                quantity = random.randint(1, min(3, owned))
                if self.player.sell_stock(stock, quantity):
                    print(f"🤖 Auto-sold {quantity} shares of {stock.symbol}")
        
        # Always advance day in auto mode
        self._next_day()
    
    def _toggle_auto_mode(self):
        """Toggle automatic trading mode."""
        self.auto_mode = not self.auto_mode
        if self.auto_mode:
            print("🤖 Auto mode enabled. The game will trade automatically.")
            print("Press Ctrl+C to stop.")
        else:
            print("🎮 Manual mode enabled.")
    
    def _quit_game(self):
        """Exit the game with final summary."""
        print("\n" + "=" * 50)
        print("📊 FINAL GAME SUMMARY")
        print("=" * 50)
        
        if self.player:
            final_value = self.player.get_portfolio_value(self.market.get_all_stocks())
            change_abs, change_pct = self.player.get_net_worth_change(self.market.get_all_stocks())
            
            print(f"Player: {self.player.name}")
            print(f"Days Played: {self.market.day - 1}")
            print(f"Starting Cash: ${self.player.starting_cash:,.2f}")
            print(f"Final Portfolio Value: ${final_value:,.2f}")
            print(f"Net Change: ${change_abs:+,.2f} ({change_pct:+.2f}%)")
            
            if change_pct > 0:
                print("🎉 Congratulations! You made a profit!")
            elif change_pct == 0:
                print("💼 You broke even. Not bad!")
            else:
                print("📉 You lost money, but gained experience!")
        
        print("\nThanks for playing Stock Game! 👋")
        self.running = False