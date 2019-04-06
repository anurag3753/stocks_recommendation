from indicators.candles.CandleTemplate import Candle
from generic.stock_utils import general_info
from generic.stock_utils import get_shadow_length
from generic.stock_utils import get_previous_day_stats, get_latest_date_for_stock
from generic.stock_utils import is_downtrend
from generic.stock_utils import is_bearish
from generic.stock_utils import is_bullish
from generic.stock_utils import is_uptrend

class Engulfing( Candle ):
    def __init__(self, o, h, l, c, stock_name, threshold = 0.2, days = 5, uptrend=False, downtrend=False, \
        find_trend = True, previous_day = []):
        # invoking the __init__ of the parent class
        Candle.__init__(self, o, h, l, c, stock_name)
        self.threshold = threshold
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
        day1_range  = abs(po - pc)
        day2_range  = abs(self.o - self.c)
        day1_middle = float(day1_range)/2

        if self.downtrend and (is_bearish(po, pc)) and (is_bullish(self.o, self.c)):
            if (self.c > po and self.o <= pc):
                self.trade_setting["candle"] = "bullish_engulfing"
                self.trade_setting["info"]   = general_info("bullish_engulfing")
                self.candle = True
            elif (day1_middle <= day2_range < day1_range):
                self.trade_setting["candle"] = "piercing_pattern"
                self.trade_setting["info"]   = general_info("piercing_pattern")
                self.candle = True

            if self.candle:
                self.trade_setting["action"] = "buy"
                self.trade_setting["buy"] = self.c
                self.trade_setting["stoploss"] = min(self.l, pl)
                self.trade_setting["target"] = ""

        elif self.uptrend and (is_bullish(po, pc)) and (is_bearish(self.o, self.c)):
            if (self.c < po and self.o > pc):
                self.trade_setting["candle"] = "bearish_engulfing"
                self.trade_setting["info"]   = general_info("bearish_engulfing")
                self.candle = True
            elif (day1_middle <= day2_range < day1_range):
                self.trade_setting["candle"] = "dark_cloud_cover"
                self.trade_setting["info"]   = general_info("dark_cloud_cover")
                self.candle = True

            if self.candle:
                self.trade_setting["action"] = "short"
                self.trade_setting["buy"] = self.c
                self.trade_setting["stoploss"] = max(self.h, ph)
                self.trade_setting["target"] = ""

        return self.candle, self.trade_setting
