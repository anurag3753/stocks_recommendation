from indicators.candles.CandleTemplate import Candle
from generic.stock_utils import general_info

class Marubozu( Candle ):
    def __init__(self, o, h, l, c, stock_name, threshold = 0.3):
        # invoking the __init__ of the parent class
        Candle.__init__(self, o, h, l, c, stock_name)
        self.threshold = threshold

    def run(self):
        if (((abs(self.o-self.l)/self.l) * 100 <= self.threshold) and ((abs(self.h-self.c)/self.h) * 100 <= self.threshold)):
            self.candle = True
            self.trade_setting["action"] = "buy"
            self.trade_setting["buy"] = self.c
            self.trade_setting["stoploss"] = self.l # On a bullish marubozu, the day's low price defines the stoploss.
            self.trade_setting["candle"] = "bullish_marubozu"
            self.trade_setting["target"] = "" # There is no direct target defined on a marubozu
            self.trade_setting["info"]   = general_info("bullish_marubozu")

        elif (((abs(self.o-self.h)/self.h) * 100 <= self.threshold) and ((abs(self.c-self.l)/self.l) * 100 <= self.threshold)):
            self.candle = True
            self.trade_setting["action"] = "sell"
            self.trade_setting["buy"] = self.c
            self.trade_setting["stoploss"] = self.h # On a bearish marubozu, the day's open/high defines stoploss in case of intraday, high in case of F&O
            self.trade_setting["candle"] = "bearish_marubozu"
            self.trade_setting["target"] = ""
            self.trade_setting["info"] =  general_info("bearish_marubozu")

        return self.candle, self.trade_setting