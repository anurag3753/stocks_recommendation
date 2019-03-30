import pickle
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from generic.utils import get_env
from generic.utils import load_yaml
from generic.utils import print_err_exit
from generic.stock_utils import process_number
from generic.stock_utils import process_stock_name
from generic.stock_utils import stocks_underwatch

env = get_env(["download_location", "map"])
filepath = str(env["download_location"]) + "/" + "quaterly_result.csv"
filepath_required = str(env["download_location"]) + "/" + "quaterly_result_required.csv"
pklpath  = str(env["download_location"]) + "/" + "quarterly_results.pkl"
cols_needed = ["stock", "date"]

def quaterly_results():
    driver = webdriver.Chrome()
    driver.get('https://www.moneycontrol.com/markets/earnings/results-calendar/')
    cols = ["stock", "date", "live_price", "change(%)", "52w_high", "52w_low"]

    res = []
    pages_traversed = 0
    previous_data = ""
    while True:
        try:
            data = driver.find_element_by_id("tbl_box1").get_attribute('innerHTML')
            if (not (previous_data == data)):
                previous_data = data
                soup = BeautifulSoup(data, "lxml")
                table_rows = soup.find_all('tr')
                for tr in table_rows:
                    td = tr.find_all('td')
                    row = [tr.text.strip() for tr in td if tr.text.strip()]
                    if row:
                        res.append(row)
                pages_traversed += 1

                if driver.find_element_by_link_text('Next'):
                    next_button = driver.find_element_by_link_text('Next')
                    next_button.click()
            else:
                break

        except:
            print_err_exit("Quaterly Results Download Failed")

    print ("%s Pages Traversed" %pages_traversed)
    driver.quit()
    
    # Create the dataframe
    df = pd.DataFrame(res, columns=cols)
    
    # process the stock_name
    df['stock'] = df['stock'].map(process_stock_name)
    # df['date']  = df['date'].to_timestamp()

    # Stocks Underwatch
    stocks = (load_yaml(env["map"])).keys()

    # Subset the dataframe based on stocks of interest
    subsetDataFrame = df[df['stock'].isin(stocks)]
    subsetDataFrame = subsetDataFrame[cols_needed]
    
    # Save the original quaterly results data list
    df.to_csv(filepath, sep=',', index = False)

    # delete df
    del df

    # Save it to csv
    subsetDataFrame.to_csv(filepath_required, sep=',', index = False)

    # Save it to pickle
    subsetDataFrame.to_pickle(pklpath)

    # delete subsetDataFrame
    del subsetDataFrame

if __name__ == "__main__":
    pass