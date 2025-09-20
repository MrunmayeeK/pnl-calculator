import sys
import csv
from decimal import Decimal, ROUND_HALF_UP
from pnl_calculator.core import PnLCalculator

def _fmt2(x: Decimal) -> str:
    return str(x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

def main(argv=None):
    argv = argv or sys.argv[1:]
    if len(argv) != 2:
        print("Usage: python -m pnl-calculator.cli <input_csv> <fifo|lifo>", file=sys.stderr)
        sys.exit(2)

    in_path, mode = argv
    calc = PnLCalculator(mode)
    out = csv.writer(sys.stdout, lineterminator="\n")
    out.writerow(["TIMESTAMP", "SYMBOL", "PNL"])
    with open(in_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ts = row["TIMESTAMP"]
            sym = row["SYMBOL"]
            side = row["BUY_OR_SELL"].strip().upper()
            price = Decimal(row["PRICE"])
            qty = int(row["QUANTITY"])
            pnl = calc.process_trade(ts, sym, side, price, qty)
            if pnl != 0:
                out.writerow([ts, sym, _fmt2(pnl)])

if __name__ == "__main__":
    main()

