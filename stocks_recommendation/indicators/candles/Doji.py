from indicators.candles.CandleTemplate import Candle
from generic.stock_utils import general_info
from generic.stock_utils import is_uptrend
from generic.stock_utils import is_downtrend
from generic.stock_utils import is_small_body

class Doji( Candle ):
    def __init__(self, o, h, l, c, stock_name, body_threshold = 5, uptrend = False, downtrend = False, find_trend = True):
        # invoking the __init__ of the parent class
        Candle.__init__(self, o, h, l, c, stock_name)
        self.body_threshold = body_threshold
        self.uptrend = uptrend
        self.downtrend = downtrend
        self.find_trend = find_trend

    def run(self):
        flag = False
        if is_small_body(self.o, self.h, self.l, self.c, self.body_threshold):
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
                self.trade_setting["stoploss"] = self.l
                self.trade_setting["candle"] = "doji_in_uptrend"
                self.trade_setting["target"] = ""
                self.trade_setting["info"] = general_info("doji_in_uptrend")

            elif self.downtrend:
                self.candle = True
                self.trade_setting["action"] = "buy"
                self.trade_setting["buy"] = self.c
                self.trade_setting["stoploss"] = self.h
                self.trade_setting["candle"] = "doji_in_downtrend"
                self.trade_setting["target"] = ""
                self.trade_setting["info"] = general_info("doji_in_downtrend")

        return self.candle, self.trade_setting