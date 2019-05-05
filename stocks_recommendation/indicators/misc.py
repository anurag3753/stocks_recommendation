import pandas as pd

def moving_average(close, n=50):
    return close.rolling(window=n).mean()

def exponential_moving_average(close, n=50):
    return close.ewm(span=n, adjust=False).mean()

def bollinger_bands(close, n=20, std_dev=2):
    msd = close.rolling(window=n).std()
    ma  = close.rolling(window=n).mean()
    lb  = ma - (msd * std_dev)
    ub  = ma + (msd * std_dev)
    return lb, ub, ma

def rsi(close, period=14):
    delta = close.diff()
    up, down = delta.copy(), delta.copy()

    up[up < 0] = 0
    down[down > 0] = 0

    rUp = up.rolling(window=period).mean()
    rDown = down.rolling(window=period).mean().abs()

    return (100 - 100 / (1 + rUp / rDown))

def macd(close):
    ema_12 = close.ewm(span=12, adjust=False).mean()
    ema_26 = close.ewm(span=26, adjust=False).mean()
    # Compute MACD line
    macd_line = ema_12 - ema_26
    # Compute Signal line
    signal_line  = macd_line.ewm(span=9, adjust=False).mean()
    return macd_line, signal_line

def aroon_up(close, n=25, fillna=False):
    """Aroon Indicator (AI)
    Identify when trends are likely to change direction (uptrend).
    Aroon Up - ((N - Days Since N-day High) / N) x 100
    https://www.investopedia.com/terms/a/aroon.asp
    Args:
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
        fillna(bool): if True, fill nan values.
    Returns:
        pandas.Series: New feature generated.
    """
    aroon_up = close.rolling(n, min_periods=0).apply(lambda x: float(np.argmax(x) + 1) / n * 100, raw=True)
    if fillna:
        aroon_up = aroon_up.replace([np.inf, -np.inf], np.nan).fillna(0)
    # return pd.Series(aroon_up, name='aroon_up'+str(n))
    return aroon_up.iloc[-1]


def aroon_down(close, n=25, fillna=False):
    """Aroon Indicator (AI)
    Identify when trends are likely to change direction (downtrend).
    Aroon Down - ((N - Days Since N-day Low) / N) x 100
    https://www.investopedia.com/terms/a/aroon.asp
    Args:
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
        fillna(bool): if True, fill nan values.
    Returns:
        pandas.Series: New feature generated.
    """
    aroon_down = close.rolling(n, min_periods=0).apply(lambda x: float(np.argmin(x) + 1) / n * 100, raw=True)
    if fillna:
        aroon_down = aroon_down.replace([np.inf, -np.inf], np.nan).fillna(0)
    # return pd.Series(aroon_down, name='aroon_down'+str(n))
    return aroon_down.iloc[-1]

def aroon_trade(close):
    up   = aroon_up(close)
    down = aroon_down(close)
    if ((up > 50) and (down < 30)):
        return "buy"
    elif ((down > 50)  and (up < 30)):
        return "sell"
    return None

def alligator(df, curr_price):
    """Also check if 3 ma's are seperate
    
    Arguments:
        df {pandas.Dataframe} -- dataframe
        curr_price {float} -- current stock price
    
    Returns:
        signal -- Return's the trading signal
    """
    df['ma_5']  = df['close'].rolling(window=5).mean()
    df['ma_8']  = df['close'].rolling(window=8).mean()
    df['ma_13']  = df['close'].rolling(window=13).mean()
    lips  = df['ma_5'].iloc[-1]
    teeth = df['ma_8'].iloc[-1]
    jaw   = df['ma_13'].iloc[-1]

    if (curr_price > lips) and (lips > teeth) and (teeth > jaw):
        return "buy"
    elif (curr_price < lips) and (lips < teeth) and (teeth < jaw):
        return "sell"
    return None


