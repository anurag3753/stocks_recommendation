import time
import pandas as pd
from setup import *
from generic.utils import *
from generic.stock_utils import get_db_connection, stocks_underwatch, list_files
from generic.connect_database import ConnectDatabase
from src.download_report import download_historical_report
from src.download_report import *

# CONSTANTS
LAC = 100000

# Valid Periods ["day", "week", "15days", "1month", "3month", "12month", "24month"]
PERIOD = "1month"

# Columns Needed
cols_needed = {
                "Date":"date",
                "Open Price":"open", 
                "High Price":"high", 
                "Low Price":"low", 
                "Last Price":"close", 
                "Total Traded Quantity":"volume"
                }

# Helper Functions
def process_date(date):
    import datetime
    s = datetime.datetime.strptime(date, '%d-%b-%Y')
    return (s.strftime("%Y-%m-%d"))

def process_volume(v):
    return float(v)/LAC

# Update Historical Prices in database
def update_historical_prices(folder_path, stock_list, truncate = True):
    # Connect to DB
    db_conn = get_db_connection()
    engine  = db_conn.create_db_engine()
    stock_list = ["adaniports"]
    for stock in stock_list:
        # Truncate Stock
        if truncate:
            query = ("TRUNCATE" + " " + surround_mysql_quotes(stock))
            db_conn.run(query, result_needed = False)

        df = pd.read_csv(folder_path + "/" + stock)
        df.rename(columns = cols_needed, inplace = True)
        df['date']   = df['date'].map(process_date)
        df['volume'] = df['volume'].map(process_volume)
        mydf = df[cols_needed.values()]
        # Update Historical Stock Prices
        try:
            mydf.to_sql(name=stock, con = engine, if_exists = 'append', index = False )
        except Exception as e:
            print(e)
            print(str(stock) + " " + "updation failed")

def process_file_names(folder_path, files_list):
    from os import rename
    try:
        for _file in files_list:
            # new file name
            new_file_name = _file.lower()
            new_file_name = new_file_name[24:-7]
            src  = folder_path + "/" + _file
            dest = folder_path + "/" + new_file_name
            rename(src, dest)
    except Exception as e:
        print (e)
        print ("Invalid file name {}".format(_file))

if __name__ == "__main__":
    data = load_yaml("config/config.yaml")
    env =  get_env(["pwd", "download_location", "data_csv_path"])
    download_location = env['download_location'] + "/" + "historical"

    # Empty the location where data needs to be downloaded
    remove(download_location)
    mkdir(download_location)

    # Download Historical Reports
    stocks = list(stocks_underwatch())
    for stock in stocks:
        download_historical_report(env['data_csv_path'], download_location, data['browser'], \
            data['driver_location'], data['webdriver_location'], stock, PERIOD)

    # Wait for some time to finish complete downloading
    time.sleep(20) # Sleep for 20 sec

    # Process the downloaded data
    file_list = list_files(download_location)
    process_file_names(download_location, file_list)

    # Update the Prices in Database
    update_historical_prices(download_location, file_list, truncate=True)