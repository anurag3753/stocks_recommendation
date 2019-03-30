'''Candle Template Class

Returns:
    Candle Object -- Template Class for Candles
'''

from generic.stock_utils import trade_setting_template

class Candle( object ):

    # Constructor
    def __init__(self, o, h, l, c, stock_name):
        self.o          = o
        self.h          = h
        self.l          = l
        self.c          = c
        self.stock_name = stock_name
        self.candle     = False
        self.trade_setting = trade_setting_template()

    def is_bullish(self):
        return (self.c - self.o) > 0

    def is_bearish(self):
        return (not self.is_bullish())

    def true_body(self):
        return abs(self.c - self.o)

    def get_shadow_length(self):
        if self.is_bullish():
            upper_shadow = self.h - self.c
            lower_shadow = self.o - self.l
        if self.is_bearish():
            upper_shadow = self.h - self.o
            lower_shadow = self.c - self.l
        return upper_shadow, lower_shadow