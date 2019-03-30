import sys
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from generic.utils import print_err_exit,print_warn,remove

def download_daily_report(filepath, download_location, browser, driver_location, webdriver_location):
    remove(filepath)
    try:
        if (browser == "chrome"):
            chromeOptions = webdriver.ChromeOptions()
            prefs = {"download.default_directory" : download_location}
            chromeOptions.add_experimental_option("prefs",prefs)
            driver = webdriver.Chrome(executable_path=webdriver_location, chrome_options=chromeOptions)
            driver.get('https://www.nseindia.com/live_market/dynaContent/live_watch/equities_stock_watch.htm')
            button = driver.find_element_by_link_text('Download in csv')
            button.click()

    except Exception as e:
        msg = "Daily Report Download Failed"
        print(str(e))
        print_err_exit(msg)
        driver.quit()

def download_historical_report(filepath, download_location, browser, driver_location, webdriver_location, stock_symbol):
    try :
        if (browser == "chrome"):
            chromeOptions = webdriver.ChromeOptions()
            prefs = {"download.default_directory" : download_location}
            chromeOptions.add_experimental_option("prefs",prefs)
            driver = webdriver.Chrome(executable_path=webdriver_location, chrome_options=chromeOptions)
            driver.get('https://www.nseindia.com/products/content/equities/equities/eq_security.htm')
            driver.find_element_by_id('rdPeriod').click()
            Select(driver.find_element_by_id('dateRange')).select_by_value('24month')
            driver.find_element_by_id('symbol').send_keys(stock_symbol)
            get_data = driver.find_element_by_id('get')
            get_data.click()
            download_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Download file in csv format"))
            )
            download_link.click()

    except Exception as e:
        print_warn(str(stock_symbol) + ": Download Historical Report Failed")
        print(str(e))
        driver.quit()

if __name__ == "__main__":
    pass