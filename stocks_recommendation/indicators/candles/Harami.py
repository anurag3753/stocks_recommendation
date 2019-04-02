from indicators.candles.CandleTemplate import Candle
from generic.stock_utils import general_info
from generic.stock_utils import get_previous_day_stats, get_latest_date_for_stock
from generic.stock_utils import is_uptrend, is_downtrend
from generic.stock_utils import is_bearish, is_bullish

class Harami( Candle ):
    def __init__(self, o, h, l, c, stock_name, days = 5):
        # invoking the __init__ of the parent class
        Candle.__init__(self, o, h, l, c, stock_name)
        self.days = days

    def run(self):
        date = get_latest_date_for_stock(self.stock_name)
        po, ph, pl, pc, pv = get_previous_day_stats(self.stock_name, date=date)

        if is_downtrend(stock_name = self.stock_name, days=self.days) and (is_bearish(po, pc)) and (self.o > pc) and is_bullish(self.o, self.c) and (self.c < po):
            self.candle = True
            self.trade_setting["action"] = "buy"
            self.trade_setting["buy"] = self.c
            self.trade_setting["stoploss"] = min(self.l, pl)
            self.trade_setting["candle"] = "bullish_harami"
            self.trade_setting["target"] = ""
            self.trade_setting["info"]   = general_info("bullish_harami")
            return self.candle, self.trade_setting
        elif is_uptrend(stock_name = self.stock_name, days=self.days) and (is_bullish(po, pc)) and (self.o < pc) and is_bearish(self.o, self.c) and (self.c > po):
            self.candle = True
            self.trade_setting["action"] = "short"
            self.trade_setting["buy"] = self.c
            self.trade_setting["stoploss"] = max(self.h, ph)
            self.trade_setting["candle"] = "bearish_harami"
            self.trade_setting["target"] = ""
            self.trade_setting["info"]   = general_info("bearish_harami")
            return self.candle, self.trade_setting

        return self.candle, self.trade_setting