import os,sys
from data_crawler.crawlStock import crawlDailyStock
import pandas as pd
import numpy as np
import mysql.connector
from collections import Counter
from itertools import chain
from datetime import datetime, timedelta

# Get SQL Password
sql_password = os.environ.get("SQL_PASSWORD")

#--------- Link to Database ---------
stockSelectorDB = mysql.connector.connect(
    host = "us-cdbr-east-04.cleardb.com",
    user = "b8aabaa725cfb0",
    password = sql_password,
    database = "heroku_cec98989109bf67"
)
mycursor = stockSelectorDB.cursor()


#---------- Select Function ---------
# 回傳連續 N日排名前30次數最多的股票10筆
# Condition:
# 1. 成交金額在前25%
# 2. 連續上漲
# 3. 本益比前30名

def selectStock(dfStock, datelist):
    
    dfStock["證券名稱"] = dfStock["證券代號"] + " " + dfStock["證券名稱"]
    selectRes = []
    
    for index in range(len(datelist)):
        df = dfStock[dfStock["Date"] == datelist[index]]
        qVolume = np.quantile(df["成交金額"], 0.75)
        qNumber = 10000
        dfFilter = df[(df["漲跌(+/-)"] == "+") & (df["成交金額"] > qVolume) & (df["成交筆數"] > qNumber)]
        dfFilter = dfFilter.sort_values(by = "本益比", ascending = True)
        selectRes.append(dfFilter.iloc[0:29]["證券名稱"].values.tolist())
        resList = list(dict(Counter(list(chain(*selectRes))).most_common(10)).keys())
        sql = "INSERT INTO dailyselectresult(Date, SelectResult) VALUES (%s, %s)"
        for ele in resList:
            val = ((datetime.today() + timedelta(days=1)).strftime(format="%Y%m%d"), ele)
            mycursor.execute(sql, val)
            stockSelectorDB.commit()
        
    return resList


# --------- Return Format -----------
# [('東森', 2),
# ('台驊投控', 2),
# ('中鋼', 2),
# ('燁輝', 2),
# ('群創', 2),
# ('燁興', 2),
# ('華航', 1),
# ('長榮', 1),
# ('榮運', 1),
# ('菱生', 1)]

