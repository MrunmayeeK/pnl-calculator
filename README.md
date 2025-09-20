**** PnL Calculator (FIFO / LIFO) ****
-This project implements a command-line tool to calculate realized PnL (Profit & Loss) from a sequence of trades using either FIFO (First In, First Out) or LIFO (Last In, First Out) accounting.

**** Project Structure ****
pnl-calculator/
  src/pnl_calculator/
    __init__.py
    core.py          # PnLCalculator implementation
    cli.py           # command line interface
  sample_data/
    trades.csv       # sample input trades
  expected_outputs/
    fifo.csv         # expected FIFO output for sample_data
    lifo.csv	     # expected LIFO output for sample_data
  tests/
    test_core.py     # pytest unit tests
README.md

**** Quick Run (From the project Root) ****
# FIFO mode
PYTHONPATH=src python -m pnl_calculator.cli sample_data/trades.csv fifo

# LIFO mode
PYTHONPATH=src python -m pnl_calculator.cli sample_data/trades.csv lifo


**** Expected output -FIFO ****
TIMESTAMP,SYMBOL,PNL
103,TFS,32.50
104,TFS,2.50

**** Expected output -LIFO ****
TIMESTAMP,SYMBOL,PNL
103,TFS,17.50
104,TFS,17.50

**** Run the Tests ****
- Create and activate a virtual environment (optional but recommended)

python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install pytest

- Run tests

pytest -q


- Results:

...

3 passed

