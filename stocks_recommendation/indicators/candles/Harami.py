from indicators.candles.CandleTemplate import Candle
from generic.stock_utils import general_info
from generic.stock_utils import get_previous_day_stats, get_latest_date_for_stock
from generic.stock_utils import is_uptrend, is_downtrend
from generic.stock_utils import is_bearish, is_bullish

class Harami( Candle ):
    def __init__(self, o, h, l, c, stock_name, days = 5, uptrend = False, downtrend = False, find_trend = True, previous_day = []):
        # invoking the __init__ of the parent class
        Candle.__init__(self, o, h, l, c, stock_name)
        self.days = days
        self.uptrend = uptrend
        self.downtrend = downtrend
        self.previous_day = previous_day
        self.find_trend = find_trend

    def run(self):
        if self.previous_day:
            po, ph, pl, pc, pv = self.previous_day
        else:
            date = get_latest_date_for_stock(self.stock_name)
            po, ph, pl, pc, pv = get_previous_day_stats(self.stock_name, date=date)

        if self.find_trend:
            if not self.uptrend and not self.downtrend:
                self.uptrend = is_uptrend(self.stock_name)
                self.downtrend = is_downtrend(self.stock_name)

        if self.downtrend and (is_bearish(po, pc)) and (self.o > pc) and is_bullish(self.o, self.c) and (self.c < po):
            self.candle = True
            self.trade_setting["action"] = "buy"
            self.trade_setting["buy"] = self.c
            self.trade_setting["stoploss"] = min(self.l, pl)
            self.trade_setting["candle"] = "bullish_harami"
            self.trade_setting["target"] = ""
            self.trade_setting["info"]   = general_info("bullish_harami")
            return self.candle, self.trade_setting

        elif self.uptrend and (is_bullish(po, pc)) and (self.o < pc) and is_bearish(self.o, self.c) and (self.c > po):
            self.candle = True
            self.trade_setting["action"] = "short"
            self.trade_setting["buy"] = self.c
            self.trade_setting["stoploss"] = max(self.h, ph)
            self.trade_setting["candle"] = "bearish_harami"
            self.trade_setting["target"] = ""
            self.trade_setting["info"]   = general_info("bearish_harami")
            return self.candle, self.trade_setting

        return self.candle, self.trade_setting