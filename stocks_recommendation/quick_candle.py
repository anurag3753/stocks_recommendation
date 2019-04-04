import time
import pickle
import pandas as pd
from setup import *
from generic.stock_utils import *
from generic.utils import *
from src.download_report import download_daily_report
from src.update_database import get_dataframe

cols_needed = {
                "Symbol":"symbol", 
                "Open":"open", 
                "High":"high", 
                "Low":"low", 
                "Last Traded Price":"close", 
                "Traded Volume(lacs)":"volume"
                }

def load_data():
    env = get_env(['pwd'])
    filepath = env['pwd'] + '/' + 'pre-built' + '/' + 'processed_data.pickle'
    prev_stats = load_pickle(filepath)
    return prev_stats

def load_current_data():
    data = load_yaml("config/config.yaml")
    env =  get_env(["pwd", "download_location"])
    download_location =  env['pwd'] + "/data/today"
    filepath = env['pwd'] + "/data/today/data.csv"

    # Download Daily Report
    download_daily_report(filepath, download_location, data['browser'], \
        data['driver_location'], data['webdriver_location'])

    # Sleep for sometime to download report
    time.sleep(10) # 10 sec sleep

    # Get the current data from file
    df = get_dataframe(filepath, cols_needed)
    df.drop('date', axis=1, inplace=True)
    # Get the dictionary from the dataframe
    stocks = dict()
    for index, row in df.iterrows():
        stocks[row['symbol']] = []
        stocks[row['symbol']].append(row['open'])
        stocks[row['symbol']].append(row['high'])
        stocks[row['symbol']].append(row['low'])
        stocks[row['symbol']].append(row['close'])
        stocks[row['symbol']].append(row['volume'])

    return stocks

def run_quick_candle():
    prev_stats = load_data()
    curr_data = load_current_data()
    # stocks = ['tatamotors', 'vedl']
    indicator = dict()
    stocks = list(stocks_underwatch())
    for stock in stocks:
        o, h, l, c, v = curr_data[stock]
        indicator[stock] = []

        # Run Marubozu
        from indicators.candles.Marubozu import Marubozu
        tr_st = Marubozu(o, h, l, c, stock)
        candle, trade_setting = tr_st.run()
        if candle:
            indicator[stock].append(trade_setting)

        # Run Spinning Top
        from indicators.candles.SpinningTop import SpinningTop
        tr_st = SpinningTop(o, h, l, c, stock, uptrend=prev_stats[stock]['uptrend'], \
            downtrend=prev_stats[stock]['downtrend'], find_trend = False)
        candle, trade_setting = tr_st.run()
        if candle:
            indicator[stock].append(trade_setting)

        # Run Paper Umbrella
        from indicators.candles.PaperUmbrella import PaperUmbrella
        tr_st = PaperUmbrella(o, h, l, c, stock, uptrend=prev_stats[stock]['uptrend'], \
        downtrend=prev_stats[stock]['downtrend'], find_trend = False)
        candle, trade_setting = tr_st.run()
        if candle:
            indicator[stock].append(trade_setting)

        # Run Shooting Star
        from indicators.candles.ShootingStar import ShootingStar
        tr_st = ShootingStar(o, h, l, c, stock, uptrend=prev_stats[stock]['uptrend'], find_trend = False)
        candle, trade_setting = tr_st.run()
        if candle:
            indicator[stock].append(trade_setting)

    # print only those stocks where a pattern is formed
    for k in indicator:
        if indicator[k]:
            print(k)
            print(indicator[k])

run_quick_candle()