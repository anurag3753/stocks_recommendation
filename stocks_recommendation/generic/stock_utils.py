import math
import string
import random
import datetime
import numpy as np
import pandas as pd
from generic.utils import *
from generic.connect_database import ConnectDatabase

# Global Params
DATE_INDEX   = 0
OPEN_INDEX   = 1
HIGH_INDEX   = 2
LOW_INDEX    = 3
CLOSE_INDEX  = 4
VOLUME_INDEX = 5

STOCK_INFO_DICT = load_yaml("docs/stock_info.yaml")

def compute_daily_return_mean_std(df, column_name):
    df['log_ret']    = np.log(df[column_name]/df[column_name].shift(1)) *100
    daily_avg        = round(df.loc[:,'log_ret'].mean(), 2)
    daily_volatility = round(df.loc[:,'log_ret'].std(), 2)
    return daily_avg, daily_volatility

def trading_range(stock_return_mean, stock_return_std, days=252, std=2):
    avg  = stock_return_mean*days
    sd   = stock_return_std*math.sqrt(days)
    return ( avg - std * sd , avg + std * sd)

def list_files(directory):
    '''Return all files in the directory
    
    Arguments:
        directory {str} -- Location of directory
    '''

    from os import listdir
    from os.path import isfile, join
    return [f for f in listdir(directory) if isfile(join(directory, f))]

def print_stock_data(stock_name, o, h, l, c):
    print ("stock_name: {}".format(stock_name))
    print ("open: {}".format(o))
    print ("high: {}".format(h))
    print ("low:{}".format(l))
    print ("close: {}".format(c))

def generate_random_alphanumeric_string(string_length):
    '''Generate random alphanumeric string, RFC2938 lowercase letters a-v and digits 0-9, length = (4, 1024)
    
    Arguments:
        string_length {int} -- tring length required
    
    Returns:
        str -- Random Alphanumeric String
    '''

    return ''.join(random.choice(string.ascii_lowercase[:-4] + string.digits) for _ in range(int(string_length)))

def get_nth_date(n = 0, ago = False, date= ""):
    """This function returns nth previous date from today 
    
    Keyword Arguments:
        n {int} -- Number of days (default: {0})
    
    Returns:
        string -- nth date from today
    """

    n           = int(n)
    if date:
        date    = datetime.datetime.strptime(date, '%Y-%m-%d')   
    else:
        date    = datetime.datetime.now()

    if ago:
        return (date - datetime.timedelta(days=n)).strftime("%Y-%m-%d")
    return (date + datetime.timedelta(days=n)).strftime("%Y-%m-%d")

def load_txt_into_list(filepath):
    '''Read the txt file line by line in a python list
    
    Arguments:
        filepath {str} -- txt file path
    
    Returns:
        list -- All the lines in the file
    '''

    try:
        with open(filepath, 'r') as f:
            content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        return [x.strip() for x in content]
    except Exception as e:
        msg = "File:" + str(filepath) + "reading failed"
        print(e)
        print_err_exit(msg)

def process_number(number):
    """This function processes integer/float given as string
    
    Arguments:
        number {str} -- integer/float in string format
    
    Returns:
        float -- Float equivalent of the string
    """

    number = str(number)
    return float(number.replace(',',''))

def process_stock_name(stock_name):
    """This function processes the stock names and does processing on the name of the stock
    
    Arguments:
        stock_name {str} -- Name of the stock
    
    Returns:
        str -- processed name of the stock
    """

    stock_name = str(stock_name)
    stock_name = stock_name.lower()
    stock_name = '_'.join(stock_name.split())
    return stock_name

def get_db_connection():
    """This function returns the database connection
    
    Returns:
        conn -- Database Connection
    """

    data = load_yaml("config/config.yaml")
    engine = ConnectDatabase(data['database'], data['uid'], data['pwd'])
    return engine

def get_historical_data(stock_name, date = get_nth_date(), days = 1):
    """This function returns the historical data for a stock. Default previous data is returned
    
    Arguments:
        stock_name {str} -- Stock Name
    
    Keyword Arguments:
        days {int} -- Number of previous days data (default: {1})
    
    Returns:
        sql_query_result -- Previous days data in terms of sql output
    """

    engine = get_db_connection()
    query = ("SELECT * FROM" + " " + surround_mysql_quotes(stock_name) + " " + "WHERE" + " " + \
              surround_mysql_quotes(stock_name) + ".date" + " " + "< DATE(" + surround_double_quotes(date) + ") order by" + " " 
              + surround_mysql_quotes(stock_name) + ".date" + " " + "DESC LIMIT" + " " + str(days))
    # print query
    return engine.run(query)

def stocks_underwatch():
    """This function computes all the stocks which are under tarder's watch list
    
    Returns:
        set -- Stock names underwatch
    """

    engine = get_db_connection()
    result = engine.run("SHOW TABLES")
    stocks = set()
    for each_row in result:
        stocks.add(each_row[0])
    
    return stocks

def get_values(sql_result):
    try:
        if sql_result:
            d = sql_result[0][0]
            o = sql_result[0][1]
            h = sql_result[0][2]
            l = sql_result[0][3]
            c = sql_result[0][4]
            v = sql_result[0][5]

            return o, h, l, c, v
    except:
        msg = "OHLCV extraction from sql query result failed"
        print_err_exit(msg)
    
    return None

def get_previous_day_stats(stock_name, date = get_nth_date()):
    """This function computes the previous day OHLCV for a stock
    
    Arguments:
        stock_name {str} -- Stock Name
        date {str} -- Reference Date
    
    Returns:
        MutipleValues -- OHLCV
    """

    sql_result = get_historical_data(stock_name, date)

    return get_values(sql_result)    

def get_stock_stats(stock_name, date):
    engine = get_db_connection()
    query = ("SELECT * FROM" + " " + surround_mysql_quotes(stock_name) + " " + "WHERE" + " " + \
              surround_mysql_quotes(stock_name) + ".date" + " " + "=" + " " + surround_double_quotes(date))
    # print query
    sql_result = engine.run(query)

    return get_values(sql_result) 

def get_latest_date_for_stock(stock_name):
    """Return latest date present for stock

    Arguments:
        stock_name {str} -- Stock Name
    """

    engine = get_db_connection()
    query = ("SELECT max(date) FROM" + " " + surround_mysql_quotes(stock_name))
    result = engine.run(query)
    # Get latest date for stock in database
    try:
        latest_date = (result[0][0].strftime("%Y-%m-%d"))
        return latest_date
    except Exception as e:
        print(e)
        return None

def get_todays_stats(stock_name):
    """Return today's stock stats
    
    Arguments:
        stock_name {str} -- Stock Name
    
    Returns:
        MutipleValues -- OHLCV
    """

    latest_date = get_latest_date_for_stock(stock_name)
    if latest_date:
        return get_stock_stats(stock_name, latest_date)

def is_small_body(o, h, l, c, threshold):
    """Check if it has small candle body
    
    Arguments:
        o {float} -- Open
        c {float} -- Close
        threshold {float} -- Percentage
    
    Returns:
        bool -- True, if body if lesser than threshold Else False
    """

    return (float(abs(o - c) / abs(h - l)) * 100 <= threshold)

def is_bullish(o, c):
    """Check if the day is Bullish
    
    Arguments:
        o {float} -- Open
        c {float} -- Close
    
    Returns:
        bool -- True, if Bullish Else False
    """

    return (c - o) > 0

def is_bearish(o, c):
    """Check if the day is Bearish
    
    Arguments:
        o {float} -- Open
        c {float} -- Close
    
    Returns:
        bool -- True, if Bearish Else False
    """

    return (c - o) < 0

def collect_closing_prices(sql_result):
    """Collect Closing Prices from the Query Result
    
    Arguments:
        sql_result {sql_query_result} -- It is SQL query result
    
    Returns:
        list -- Closing Prices obtained from sql_query result
    """

    closing_prices = []
    for each_row in sql_result:
        closing_prices.append(each_row[CLOSE_INDEX])   # At 4th index close prices are found
    return closing_prices

def is_descending(number_list):
    """Check if the number_list is in strict descending order
    
    Arguments:
        number_list {list} -- Number list
    
    Returns:
        bool -- True, if Strictly descending
    """

    if len(number_list) == 0 or len(number_list) == 1:
        return True

    for i in range(len(number_list)-1):
        if number_list[i] <= number_list[i+1]:
            return False
    return True

def is_downtrend(stock_name, date=get_nth_date(), days=5):
    """Check if the stock is in downtrend
    
    Arguments:
        stock_name {str} -- Stock Name
    
    Keyword Arguments:
        date {date} -- Date (default: {get_nth_date()})
        days {int} -- Number of days to consider for downtrend (default: {5})
    
    Returns:
        bool -- True if stock is in downtrend, Else False
    """

    sql_result = get_historical_data(stock_name, days=days, date=date)
    closing_prices = collect_closing_prices(sql_result)
    return is_ascending(closing_prices)

def is_ascending(number_list):
    """Check if the number_list is in strict ascending order
    
    Arguments:
        number_list {list} -- Number list
    
    Returns:
        bool -- True, if Strictly ascending
    """
    if len(number_list) == 0 or len(number_list) == 1:
        return True

    for i in range(len(number_list)-1):
        if number_list[i] >= number_list[i+1]:
            return False
    return True

def is_uptrend(stock_name, date=get_nth_date(), days=5):
    """Check if the stock is in uptrend
    
    Arguments:
        stock_name {str} -- Stock Name
    
    Keyword Arguments:
        date {date} -- Date (default: {get_nth_date()})
        days {int} -- Number of days to consider for uptrend (default: {5})
    
    Returns:
        bool -- True if stock is in uptrend, Else False
    """

    sql_result = get_historical_data(stock_name, days=days, date=date)
    closing_prices = collect_closing_prices(sql_result)
    return is_descending(closing_prices)

def get_shadow_length(o, h, l, c):
    """Get the upper and lower shadow length
    
    Arguments:
        o {float} -- Open
        h {float} -- High
        l {float} -- Low
        c {float} -- Close
    
    Returns:
        tuple -- upper shadow length and lower shadow length
    """

    if is_bullish(o, c):
        upper_shadow = h - c
        lower_shadow = o - l
    if is_bearish(o, c):
        upper_shadow = h - o
        lower_shadow = c - l
    return upper_shadow, lower_shadow

def trade_setting_template():
    """Return template for stock recommendation
    
    Returns:
        dict -- Template for trade setting
    """

    return {"candle":"", "action":"", "target":"", "stoploss":"", "buy":"", "info":""}

def general_info(pattern):
    """ Get the general information about the pattern
    
    Arguments:
        pattern {str} -- pattern name
    
    Returns:
        str -- General Information about pattern
    """

    return STOCK_INFO_DICT[pattern]

def last_n_days_volume(stock_name, days=10, date = get_nth_date()):
    '''Get last n days volume information

    Arguments:
        stock_name {str} -- Stock Name

    Keyword Arguments:
        days {int} -- Mumber of days (default: {10})

    Returns:
        list -- List of last n days volume information
    '''

    sql_result = get_historical_data(stock_name=stock_name, days=days, date=date)
    volume = []
    try:
        if sql_result:
            for rows in sql_result:
                volume.append(rows[VOLUME_INDEX])
    except:
        msg = "OHLCV extraction from sql query result failed"
        print_err_exit(msg)
    if volume:
        return volume
    else:
        print_warn("last_n_days_volume() failed")
        return None

def last_n_days_avg(stock_name, days=10, date = get_nth_date()):
    volume = last_n_days_volume(stock_name=stock_name, days=days, date=date)
    if volume:
        return float(sum(volume))/len(volume)
    else:
        return None

if __name__ == "__main__":
    pass