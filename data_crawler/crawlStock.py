import requests
from io import StringIO
import pandas as pd
import numpy as np
from datetime import datetime

# ------ Function Crawl Stock ------
# datelist: e.x. -> ["20210806", "20210807"]

def crawlDailyStock(datelist):
    dfStock = pd.DataFrame({})
    for index in range(len(datelist)):
        # Download
        r = requests.post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + datelist[index] + '&type=ALL')

        # Manipulate data
        df = pd.read_csv(StringIO(r.text.replace("=", "")), 
                         header=["證券代號" in l for l in r.text.split("\n")].index(True)-1)
        del df["Unnamed: 16"]
        df = df[df["證券代號"].str[0] != "0"] # Remove ETF
        df["Date"] = datelist[index]
        dfStock = dfStock.append(df).reset_index(drop = True)
    

    #---------- Data Processing ---------
    dfStock["成交金額"] = dfStock["成交金額"].str.replace(",","").astype(int)
    dfStock["成交筆數"] = dfStock["成交筆數"].str.replace(",","").astype(int)
    
    return dfStock
