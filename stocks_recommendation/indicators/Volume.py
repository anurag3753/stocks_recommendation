""" Understanding Price and Volume Together
    1. Price Up and Volume Up      :- Bullish (Trade)
    2. Price Down and Volume Up    :- Bearish (Trade)
    3. Price Neutral and Volume Up :- Block Deal (Don't Trade)
    4. Always make sure you compare real-time volume with previous day volume to get bigger picture
    5. Comparison Price could be yetserday also OR last 10 days SMA
"""

from generic.stock_utils import *

class Volume:
    def __init__(self, o, h, l, c, v, stock_name, days=10, avg = -1, previous_day=[]):
        self.o = o
        self.h = h
        self.l = l
        self.c = c
        self.v = v
        self.stock_name = stock_name
        self.days = days
        self.avg = avg
        self.previous_day = previous_day

    def run(self):
        if (not self.previous_day) and self.avg < 0:
            date = get_latest_date_for_stock(self.stock_name)
            avg_volume = last_n_days_avg(self.stock_name, self.days, date=date)
            po, ph, pl, pc, pv = get_previous_day_stats(self.stock_name, date=date)
        else:
            avg_volume = self.avg
            po, ph, pl, pc, pv = self.previous_day

        if self.c > pc and self.v > avg_volume: # Smart money is bullish
            return "bullish"
        elif self.c < pc and self.v > avg_volume: # Smart money is bearish
            return "bearish"
        return "trap"