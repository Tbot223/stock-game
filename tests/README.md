# Tests directory for Stock Game

This directory contains unit tests for the stock game project.

## Running Tests

To run all tests:
```bash
python -m unittest tests.test_stock_game -v
```

Or run the test file directly:
```bash
python tests/test_stock_game.py
```

## Test Coverage

Current tests cover:
- Stock class functionality (price updates, change calculations)
- Player class functionality (buying/selling stocks, portfolio management)
- Market class functionality (stock management, market updates)
- Basic Game class initialization

## Future Test Enhancements

- Integration tests for complete game workflows
- Market event simulation tests
- Performance and stress tests
- Mock data for deterministic testing