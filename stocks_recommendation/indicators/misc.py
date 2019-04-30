import pandas as pd

def moving_average(df, n=50):
    """Returns dataframe with 50 day Moving Average 
    
    Arguments:
        df {pandas.Datafarme} -- Pandas dataframe having close prices
    
    Keyword Arguments:
        n {int} -- Default Time Period (default: {50})
    
    Returns:
        df -- Pandas Dataframe having Moving Average for n days
    """

    df['MA']  = df['Close'].rolling(window=n).mean()
    return df

def exponential_moving_average(df, n=50):
    """Returns dataframe with 50 day Exponential Moving Average
    
    Arguments:
        df {[type]} -- [description]
    
    Keyword Arguments:
        n {int} -- Default Time Period (default: {50})
    
    Returns:
        df -- Pandas Dataframe having Exponential Moving Average for n days
    """

    df['EMA']  = df['Close'].ewm(span=n).mean()
    return df

def bollinger_bands(df, n=20, std_dev=2):
    """Returns dataframe with Bollinger Band Upper, Lower and Moving Avg Values
    
    Arguments:
        df {pandas.Datafarme} -- Pandas dataframe having close prices
    
    Keyword Arguments:
        n {int} -- Default Time Period (default: {20})
        std_dev {int} -- Default Std Deviation (default: {2})
    
    Returns:
        df -- Pandas Dataframe having UB,LB,MV as upper bound, lower bound, moving average
    """

    df['MSD'] = df['Close'].rolling(window=n).std()
    df['MA']  = df['Close'].rolling(window=n).mean()
    df['LB']  = df['MA'] - (df['MSD'] * std_dev)
    df['UB']  = df['MA'] + (df['MSD'] * std_dev)
    return df

