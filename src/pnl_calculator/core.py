from collections import deque, defaultdict
from decimal import Decimal, getcontext
from dataclasses import dataclass

getcontext().prec = 28

@dataclass
class Lot:
    side: str
    price: Decimal
    qty: int

class PnLCalculator:
    def __init__(self, mode:str):
        m = mode.lower()
        if m not in ("fifo","lifo"):
            raise ValueError("mode must be 'fifo' or 'lifo'")
        self.mode = m
        self.open_buys = defaultdict(deque)
        self.open_sells = defaultdict(deque)

    def process_trade(self, ts: str, symbol: str, side: str, price: Decimal, qty: int):
        realized = Decimal("0")
        remain = qty

        if side == "B":
            opp = self.open_sells[symbol]
            while remain > 0 and opp:
                lot = opp.pop() if self.mode == "lifo" else opp.popleft()
                matched = min(remain, lot.qty)
                realized += Decimal(matched) * (lot.price - price)
                lot.qty -= matched
                remain -= matched
                if lot.qty > 0:
                    (opp.append if self.mode == "lifo" else opp.appendleft)(lot)
            if remain > 0:
                self.open_buys[symbol].append(Lot("B", price, remain))
        else:
            opp = self.open_buys[symbol]
            while remain > 0 and opp:
                lot = opp.pop() if self.mode == "lifo" else opp.popleft()
                matched = min(remain, lot.qty)
                realized += Decimal(matched) * (price - lot.price)
                lot.qty -= matched
                remain -= matched
                if lot.qty > 0:
                    (opp.append if self.mode == "lifo" else opp.appendleft)(lot)
            if remain > 0:
                self.open_sells[symbol].append(Lot("S", price, remain))

        return realized
