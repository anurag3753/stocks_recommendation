import pickle
import pandas as pd
from setup import *
from path import Path
from generic.stock_utils import *
from generic.utils import *

'''Dictionary of Stocks list such that

    stock[name]= {volume:[last_10_days], prev:[ohlcv]}

'''

def generate_preprocessed_data():
    stocks = list(stocks_underwatch())
    prev_stats = dict()
    result = dict()

    for stock in stocks:
        prev_stats[stock] = dict()

        # Collect last 10 days volume average
        prev_stats[stock]['avg_vol'] = last_n_days_avg(stock, days=10, date = get_nth_date())

        # Collect previous trend data
        prev_stats[stock]['uptrend']   = is_uptrend(stock, date=get_nth_date(), days=5)
        prev_stats[stock]['downtrend'] = is_downtrend(stock, date=get_nth_date(), days=5)

        # Since we are running it, before updating the today's data in db
        # So, techically previous day data, will be today's stats
        prev_stats[stock]['p_ohlcv'] = get_todays_stats(stock)

        # Save the pre-processed data inside pickle
        env = get_env(['pwd'])
        filepath = env['pwd'] + '/' + 'pre-built' + '/' + 'processed_data.pickle'
        save_to_pickle(prev_stats, filepath)

generate_preprocessed_data()
