from indicators.candles.CandleTemplate import Candle
from generic.stock_utils import general_info
from generic.stock_utils import is_uptrend
from generic.stock_utils import is_downtrend
from generic.stock_utils import is_small_body

class SpinningTop( Candle ):
    def __init__(self, o, h, l, c, stock_name, body_threshold = 4, shadow_threshold = 5, uptrend = False, downtrend = False, find_trend = True):
        # invoking the __init__ of the parent class
        Candle.__init__(self, o, h, l, c, stock_name)
        self.body_threshold = body_threshold
        self.shadow_threshold = shadow_threshold
        self.uptrend = uptrend
        self.downtrend = downtrend
        self.find_trend = find_trend

    def run(self):
        flag = False
        if is_small_body(self.o, self.c, self.body_threshold):
            upper_shadow, lower_shadow = self.get_shadow_length()
            if float(abs(upper_shadow - lower_shadow)) / max(upper_shadow, lower_shadow) * 100 <= self.shadow_threshold:
                flag = True
    
        if self.find_trend:
            if not self.uptrend and not self.downtrend:
                self.uptrend = is_uptrend(self.stock_name)
                self.downtrend = is_downtrend(self.stock_name)

        if flag:
            if self.uptrend:
                self.candle = True
                self.trade_setting["action"] = "sell"
                self.trade_setting["buy"] = self.c
                self.trade_setting["stoploss"] = self.o
                self.trade_setting["candle"] = "spinning_top_in_uptrend"
                self.trade_setting["target"] = ""
                self.trade_setting["info"] = general_info("spinning_top_in_uptrend")

            elif self.downtrend:
                self.candle = True
                self.trade_setting["action"] = "buy"
                self.trade_setting["buy"] = self.c
                self.trade_setting["stoploss"] = self.o
                self.trade_setting["candle"] = "spinning_top_in_downtrend"
                self.trade_setting["target"] = ""
                self.trade_setting["info"] = general_info("spinning_top_in_downtrend")

        return self.candle, self.trade_setting