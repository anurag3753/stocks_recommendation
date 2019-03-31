from setup import *
from generic.utils import get_env, load_yaml
from src.download_report import download_daily_report
from src.update_database import update_stock_prices

if __name__ == "__main__":
    data = load_yaml("config/config.yaml")
    env =  get_env(["pwd", "download_location", "data_csv_path"])

    # Download Daily Report
    download_daily_report(env['data_csv_path'], env['download_location'], data['browser'], \
        data['driver_location'], data['webdriver_location'])

    # Update into database
    update_stock_prices(env['data_csv_path'])
