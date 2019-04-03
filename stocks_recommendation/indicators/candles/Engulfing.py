from indicators.candles.CandleTemplate import Candle
from generic.stock_utils import general_info
from generic.stock_utils import get_shadow_length
from generic.stock_utils import get_previous_day_stats
from generic.stock_utils import is_downtrend
from generic.stock_utils import is_bearish
from generic.stock_utils import is_bullish
from generic.stock_utils import is_uptrend

class Engulfing( Candle ):
    def __init__(self, o, h, l, c, stock_name, threshold = 0.2, days = 5):
        # invoking the __init__ of the parent class
        Candle.__init__(self, o, h, l, c, stock_name)
        self.threshold = threshold
        self.days = days

    def run(self):
        date = get_latest_date_for_stock(self.stock_name)
        po, ph, pl, pc, pv = get_previous_day_stats(self.stock_name, date=date)
        downtrend = is_downtrend(stock_name = self.stock_name, days=self.days)
        uptrend   = is_uptrend(stock_name = self.stock_name, days=self.days)
        day1_range  = abs(po - pc)
        day2_range  = abs(self.o - self.c)
        day1_middle = float(day1_range)/2

        if downtrend and (is_bearish(po, pc)) and (is_bullish(self.o, self.c)) and (self.c > po and self.o <= pc):
            self.candle = True
            self.trade_setting["action"] = "buy"
            self.trade_setting["buy"] = self.c
            self.trade_setting["stoploss"] = min(self.l, pl)
            self.trade_setting["candle"] = "bullish_engulfing"
            self.trade_setting["target"] = ""
            self.trade_setting["info"]   = general_info("bullish_engulfing")
            return self.candle, self.trade_setting
        
        elif uptrend and (is_bullish(po, pc)) and (is_bearish(self.o, self.c)) and (self.c < po and self.o > pc):
            self.candle = True
            self.trade_setting["action"] = "short"
            self.trade_setting["buy"] = self.c
            self.trade_setting["stoploss"] = max(self.h, ph)
            self.trade_setting["candle"] = "bearish_engulfing"
            self.trade_setting["target"] = ""
            self.trade_setting["info"]   = general_info("bearish_engulfing")
            return self.candle, self.trade_setting

        elif downtrend and (is_bearish(po, pc)) and (is_bullish(self.o, self.c)) and (day1_middle <= day2_range < day1_range):
            self.candle = True
            self.trade_setting["action"] = "buy"
            self.trade_setting["buy"] = self.c
            self.trade_setting["stoploss"] = max(self.l, pl)
            self.trade_setting["candle"] = "piercing_pattern"
            self.trade_setting["target"] = ""
            self.trade_setting["info"]   = general_info("piercing_pattern")
            return self.candle, self.trade_setting

        elif uptrend and (is_bullish(po, pc)) and (is_bearish(self.o, self.c)) and (day1_middle <= day2_range < day1_range):
            self.candle = True
            self.trade_setting["action"] = "short"
            self.trade_setting["buy"] = self.c
            self.trade_setting["stoploss"] = max(self.h, ph)
            self.trade_setting["candle"] = "dark_cloud_cover"
            self.trade_setting["target"] = ""
            self.trade_setting["info"]   = general_info("dark_cloud_cover")
            return self.candle, self.trade_setting       

        return self.candle, self.trade_setting
