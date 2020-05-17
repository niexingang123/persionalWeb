import tushare as ts
import pandas as pd
import numpy as np
import os,datetime
# from matplotlib.pylab import date2num
# pip install -i https://pypi.douban.com/simple tushare 豆瓣镜像安装python库

def getcodes():
    filebasic = '../static/csvfile/stockbasic.csv'
    dfstockbasic = pd.read_csv(filebasic, encoding="utf-8")
    # print(dfstockbasic)
    dfstockbasic = ts.get_stock_basics()
    print(dfstockbasic)
    dfstockbasic['tomarket'] = pd.to_numeric(dfstockbasic.timeToMarket)
    dflateststock = dfstockbasic[(dfstockbasic.tomarket <= 20151001)]
    codes = []
    for index, row in dflateststock.iterrows():
        every = {}
        # code='{:0>6}'.format(row['code'])
        every['code'] = index
        every['name'] = row['name']
        codes.append(every)
        # codes.append(code)
    print(codes)
    return codes

def getstocksdata():
    codes=getcodes()
    for code in codes:
        shyh = ts.get_hist_data(code['code'])
        print(shyh.sort_index())
        minclose=np.nanmin(shyh.iloc[:, 1].values)
        nowprice=shyh.iloc[0]['close']
        price_change=np.sum(shyh.iloc[:5]['close'])
        print(shyh.iloc)
        pricediff=round(minclose/nowprice,2)
        data=[]
        # for row in shyh.iloc:
        for row in shyh.index:
            oneday = []
            oneday.append(row)
            oneday.append(shyh.loc[row, 'open'])
            oneday.append(shyh.loc[row, 'close'])
            oneday.append(shyh.loc[row, 'low'])
            oneday.append(shyh.loc[row, 'high'])
            data.append(oneday)
        print(data)
        break
# def date_to_num(dates):
#     nums=[]
#     for date in dates:
#         date_time = datetime.datetime.strptime(str(date), '%Y-%m-%d')
#         num = date2num(date_time)
#         nums.append(num)
#     return  nums

if __name__ == "__main__":
    getstocksdata()