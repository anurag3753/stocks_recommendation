import datetime
import pandas as pd

from generic.utils import *
from generic.stock_utils import *

LAC = 100000

cols_needed = {
                "Symbol":"symbol", 
                "Open":"open", 
                "High":"high", 
                "Low":"low", 
                "Last Traded Price":"close", 
                "Traded Volume(lacs)":"volume"
                }

def process_volume(qty):
    qty = process_number(qty)
    return qty * LAC

def get_dataframe(filepath, cols_needed):
    df = pd.read_csv(filepath)
    df.rename(columns = cols_needed, inplace = True)
    df['symbol'] = df['symbol'].map(process_stock_name)
    df['open']   = df['open'].map(process_number)
    df['high']   = df['high'].map(process_number)
    df['low']    = df['low'].map(process_number)
    df['close']  = df['close'].map(process_number)
    df['volume'] = df['volume'].map(process_volume)
    mydf = df[cols_needed.values()]
    del df
    mydf['date'] = get_nth_date()
    return mydf

def get_stock_report(df, stock_name):
    try:
        new_df = df.loc[df['symbol'] == stock_name]
        return new_df[new_df.columns.difference(['symbol'])]
    except:
        return None

class UpdateStockPrices:
    def __init__(self, filepath):
        self.filepath   = filepath

    def update_stock_prices(self):
        # Connect to database
        db_conn = get_db_connection()
        engine  = db_conn.create_db_engine()

        # Get existing stocks
        underwatch_stocks = stocks_underwatch()

        # Read Filepath and get dataframe for the file
        df = get_dataframe(self.get_filepath(), cols_needed)

        # Below stocks will be updated
        print ("Following Stocks will be updated:")
        print (underwatch_stocks)

        # Update the stock prices in database
        for stock in underwatch_stocks:
            data = get_stock_report(df, stock)
            if data is not None:
                try:
                    data.to_sql(name=stock, con = engine, if_exists = 'append', index = False )
                except Exception as e:
                    msg = str(stock) + " " + "database updation failed"
                    print(msg)
                    print(e)
                    pass

    def get_filepath(self):
        return self.filepath

if __name__ == "__main__":
    pass