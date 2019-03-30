from indicators.candles.CandleTemplate import Candle
from generic.stock_utils import general_info
from generic.stock_utils import get_shadow_length
from generic.stock_utils import is_uptrend
from generic.stock_utils import is_downtrend
from generic.stock_utils import print_stock_data

class ShootingStar( Candle ):
    def __init__(self, o, h, l, c, stock_name, threshold = 1.5, uptrend = False):
        # invoking the __init__ of the parent class
        Candle.__init__(self, o, h, l, c, stock_name)
        self.threshold = threshold
        self.uptrend = uptrend

    def run(self):
        flag = False
        real_body = self.true_body()
        upper_shadow, lower_shadow = self.get_shadow_length()

        try:
            if float(upper_shadow)/real_body >= 2 and ((float(lower_shadow) / self.l) * 100) <= self.threshold:
                flag = True
        except ZeroDivisionError as e:
            print_stock_data(self.stock_name, self.o, self.h, self.l, self.c)
            print (e)

        if not self.uptrend:
            self.uptrend = is_uptrend(self.stock_name)

        if flag:
            if self.uptrend:
                self.candle = True
                self.trade_setting["action"] = "sell"
                self.trade_setting["buy"] = self.c
                self.trade_setting["stoploss"] = self.h
                self.trade_setting["candle"] = "shooting_star"
                self.trade_setting["target"] = ""
                self.trade_setting["info"] = general_info("shooting_star")
        
        return self.candle, self.trade_setting
