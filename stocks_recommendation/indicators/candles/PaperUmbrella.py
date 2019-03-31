from indicators.candles.CandleTemplate import Candle
from generic.stock_utils import general_info
from generic.stock_utils import is_uptrend
from generic.stock_utils import is_downtrend

class PaperUmbrella( Candle ):
    def __init__(self, o, h, l, c, stock_name, threshold = 1.5, uptrend = False, downtrend = False):
        # invoking the __init__ of the parent class
        Candle.__init__(self, o, h, l, c, stock_name)
        self.threshold = threshold
        self.uptrend = uptrend
        self.downtrend = downtrend

    def run(self):
        real_body = self.true_body()
        upper_shadow, lower_shadow = self.get_shadow_length()
        flag = False
        if (float(lower_shadow)/real_body >= 2) and ((float(upper_shadow) / self.h) * 100) <= self.threshold:
            flag = True
        
        if not self.uptrend and not self.downtrend:
            self.uptrend = is_uptrend(self.stock_name)
            self.downtrend = is_downtrend(self.stock_name)
        
        if flag:
            if self.uptrend:
                self.candle = True
                self.trade_setting["action"] = "sell"
                self.trade_setting["buy"] = self.c
                self.trade_setting["stoploss"] = self.h
                self.trade_setting["candle"] = "hangingman"
                self.trade_setting["target"] = ""
                self.trade_setting["info"] = general_info("hangingman")

            elif self.downtrend:
                self.candle = True
                self.trade_setting["action"] = "buy"
                self.trade_setting["buy"] = self.c
                self.trade_setting["stoploss"] = self.l
                self.trade_setting["candle"] = "hammer"
                self.trade_setting["target"] = ""
                self.trade_setting["info"] = general_info("hammer")
        
        return self.candle, self.trade_setting