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
        po, ph, pl, pc, pv = get_previous_day_stats(self.stock_name)

        if is_downtrend(stock_name = self.stock_name, days=self.days) and (is_bearish(po, pc)) and (self.c > po and self.o <= pc):
            self.candle = True
            self.trade_setting["action"] = "buy"
            self.trade_setting["buy"] = self.c
            self.trade_setting["stoploss"] = min(self.l, pl)
            self.trade_setting["candle"] = "bullish_engulfing"
            self.trade_setting["target"] = ""
            self.trade_setting["info"]   = general_info("bullish_engulfing")
            return self.candle, self.trade_setting
        
        elif is_uptrend(stock_name = self.stock_name, days=self.days) and (is_bullish(po, pc)) and (self.c < po and self.o > pc):
            self.candle = True
            self.trade_setting["action"] = "short"
            self.trade_setting["buy"] = self.c
            self.trade_setting["stoploss"] = max(self.h, ph)
            self.trade_setting["candle"] = "bearish_engulfing"
            self.trade_setting["target"] = ""
            self.trade_setting["info"]   = general_info("bearish_engulfing")
            return self.candle, self.trade_setting

        return self.candle, self.trade_setting
