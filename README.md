# 📈 Stock Game

A Python-based stock trading simulation game where players can buy and sell stocks, manage their portfolio, and experience realistic market dynamics.

## 🎮 Features

- **Interactive Trading**: Buy and sell stocks with real-time price updates
- **Portfolio Management**: Track your holdings and cash balance
- **Market Simulation**: Dynamic stock prices with volatility and trends
- **Market Events**: News events that affect stock prices
- **Market Sentiment**: Bull, bear, and neutral market conditions
- **Auto Trading Mode**: Watch the AI trade automatically
- **Performance Tracking**: Monitor your profits and losses

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- No external dependencies required (uses only standard library)

### Installation
1. Clone the repository:
```bash
git clone https://github.com/Tbot223/stock-game.git
cd stock-game
```

2. Run the game:
```bash
python main.py
```

## 🎯 How to Play

1. **Start the Game**: Enter your name and starting cash amount
2. **View Market**: Use `market` command to see current market conditions
3. **Check Stocks**: Use `stocks` command to see all available stocks
4. **Buy Stocks**: Use `buy <symbol> <quantity>` (e.g., `buy AAPL 10`)
5. **Sell Stocks**: Use `sell <symbol> <quantity>` (e.g., `sell AAPL 5`)
6. **Advance Time**: Use `next` command to go to the next trading day
7. **Check Portfolio**: Use `portfolio` command to see your holdings

### Available Commands
- `help` - Show all available commands
- `market` - Show market overview and news
- `stocks` - Show all available stocks with prices
- `portfolio` - Show your portfolio and performance
- `buy <symbol> <quantity>` - Buy stocks
- `sell <symbol> <quantity>` - Sell stocks
- `next` - Advance to next trading day
- `auto` - Toggle automatic trading mode
- `quit` - Exit the game

## 🏢 Available Stocks

The game includes several major stocks:
- **AAPL** - Apple Inc.
- **GOOGL** - Alphabet Inc.
- **MSFT** - Microsoft Corporation
- **TSLA** - Tesla Inc.
- **AMZN** - Amazon.com Inc.
- **META** - Meta Platforms Inc.
- **NFLX** - Netflix Inc.
- **NVDA** - NVIDIA Corporation

## 📊 Game Mechanics

### Stock Prices
- Prices fluctuate based on volatility settings
- Market sentiment affects all stocks
- News events can impact individual stock prices
- Price history is tracked for trend analysis

### Market Events
- Earnings reports affect individual stocks
- Economic indicators influence market sentiment
- Company news creates price movements
- Market sentiment cycles between bull, bear, and neutral

### Scoring
- Track your portfolio value over time
- See percentage gains/losses from starting amount
- Compare performance across different market conditions

## 🛠️ Project Structure

```
stock-game/
├── stock_game/
│   ├── __init__.py      # Package initialization
│   ├── game.py          # Main game controller
│   ├── player.py        # Player and portfolio management
│   ├── stock.py         # Stock price simulation
│   └── market.py        # Market dynamics and events
├── tests/               # Test files (future)
├── main.py             # Game entry point
├── requirements.txt    # Dependencies
└── README.md          # This file
```

## 🎮 Example Gameplay

```
📈 Welcome to Stock Game! 📈
Enter your name: Trader Joe
Enter starting cash (default $10,000): 15000

Welcome Trader Joe! You start with $15,000.00
Type 'help' for available commands.

=== Market Day 1 ===
Market Sentiment: NEUTRAL

> stocks
=== Available Stocks ===
AAPL: $150.00 (+0.00%) [STABLE]
GOOGL: $2500.00 (+0.00%) [STABLE]
MSFT: $300.00 (+0.00%) [STABLE]
...

> buy AAPL 10
✅ Bought 10 shares of AAPL at $150.00 each
💰 Total cost: $1,500.00
💵 Remaining cash: $13,500.00

> next
⏰ Advancing to next trading day...
📊 Day 2
📰 Breaking News:
  • Apple Inc. reports better than expected earnings
```

## 🧪 Future Enhancements

- Real stock data integration via APIs
- Stock price charts and technical indicators
- More complex trading strategies
- Multiplayer competition mode
- Save/load game functionality
- Options and futures trading
- Dividend payments

## 📝 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.
