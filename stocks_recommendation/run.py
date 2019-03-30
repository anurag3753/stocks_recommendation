from setup import *
from generic.utils import *
from generic.stock_utils import *
from generic.connect_database import ConnectDatabase
from src.update_database import UpdateStockPrices
from src.download_report import download_daily_report, download_historical_report
from multiprocessing import Process

if __name__ == "__main__":
    data = load_yaml("config/config.yaml")
    env =  get_env(["pwd", "download_location", "data_csv_path"])

    # Download Daily Report
    # download_daily_report(env['data_csv_path'], env['download_location'], data['browser'], data['driver_location'], data['webdriver_location'])

    # Historical Data should get download parallely
    stocks = list(stocks_underwatch())
    for stock in stocks:
        args = [env['data_csv_path'], env['download_location'], data['browser'], data['driver_location'], data['webdriver_location'], stock]
        Process(target=download_historical_report, args=(args)).start()

    # Update into database
    # mystock = UpdateStockPrices(env['data_csv_path'])
    # mystock.update_stock_prices()

    # Run Technical Analysis
    # run_technical_analysis()