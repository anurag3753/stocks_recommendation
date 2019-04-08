def gap_up_opening(current_open, previous_day_close):
    return float(current_open) > float(previous_day_close)

def gap_down_opening(current_open, previous_day_close):
    return float(previous_day_close) > float(current_open)

def get_shadow_length(o, h, l, c):
    if is_bullish(o, c):
        upper_shadow = h - c
        lower_shadow = o - l
    if is_bearish(o, c):
        upper_shadow = h - o
        lower_shadow = c - l
    return upper_shadow, lower_shadow

def is_spinning_top(o, h, l, c, body_threshold, shadow_threshold):
    flag = False
    if is_small_body(o, c, body_threshold):
        upper_shadow, lower_shadow = get_shadow_length(o, h, l, c)
        if float(abs(upper_shadow - lower_shadow)) / max(upper_shadow, lower_shadow) * 100 <= shadow_threshold:
            flag = True
    return flag

def is_doji(o, c, l, c, body_threshold):
    return is_small_body(o, c, body_threshold)

class MorningStar( Candle ):
    def __init__(self, o, h, l, c, stock_name, days = 5, uptrend = False, downtrend = False, find_trend = True, \
        body_threshold = 4, shadow_threshold = 5, previous_day = [], pp = []):
        # invoking the __init__ of the parent class
        Candle.__init__(self, o, h, l, c, stock_name)
        self.days = days
        self.uptrend = uptrend
        self.downtrend = downtrend
        self.find_trend = find_trend
        self.body_threshold = body_threshold
        self.shadow_threshold = shadow_threshold
        self.previous_day = previous_day
        self.pp = pp

    def run():
        date = get_latest_date_for_stock(self.stock_name)
        previous_date = get_previous_date(self.stock_name)

        if self.previous_day:
            po, ph, pl, pc, pv = self.previous_day
        else:
            po, ph, pl, pc, pv = get_previous_day_stats(self.stock_name, date=date)

        if self.pp:
            ppo, pph, ppl, ppc, ppv = self.pp
        else:
            ppo, pph, ppl, ppc, ppv = get_previous_day_stats(self.stock_name, date=previous_date)

        if self.find_trend:
            if not self.uptrend and not self.downtrend:
                self.uptrend = is_uptrend(self.stock_name, previous_date)
                self.downtrend = is_downtrend(self.stock_name, previous_date)

        # Need to check if p2 is doji OR spinning top
        sp_top = is_spinning_top(self.o, self.h, self.l, self.c, self.body_threshold, self.shadow_threshold)
        doji   = is_doji((self.o, self.h, self.l, self.c, self.body_threshold)

        if self.downtrend and is_bearish(ppo, ppc) and gap_down_opening(po, ppc) and (sp_top or doji) \
            and gap_up_opening(self.o, pc) and (self.c > ppo) and is_bullish(self.o, self.c):
            self.candle = True
            self.trade_setting["action"] = "buy"
            self.trade_setting["buy"] = self.c
            self.trade_setting["stoploss"] = min(self.l, pl, ppl)
            self.trade_setting["candle"] = "morning_star"
            self.trade_setting["target"] = ""
            self.trade_setting["info"]   = general_info("morning_star")
            return self.candle, self.trade_setting

        return self.candle, self.trade_setting