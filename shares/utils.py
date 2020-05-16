import requests,re,os
from selenium import webdriver
import threading
import tushare as ts
import pandas as pd
import numpy as np
from . import models

# 获取动态cookies
cookies=[]
def get_cookie():
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=options)
        url = "http://q.10jqka.com.cn/thshy/"
        driver.get(url)
        # 获取cookie列表
        cookie = driver.get_cookies()
        driver.close()
        cookies.append(cookie[0]['value'])
        return cookie[0]['value']

def get_more(num):
    print('开始获取cookie')
    thread_list=[]
    for i in range(num):
        thread = threading.Thread(target=get_cookie)
        thread_list.append(thread)
    for t in thread_list:
        t.setDaemon(True)
        t.start()
    for t in thread_list:
        t.join()
    print(cookies)

#获取页面代码
def get_page_detail(url,cookie):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Referer': 'http://q.10jqka.com.cn/thshy/detail',
        'Cookie': 'v={}'.format(cookie)
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return str(response.text)
        return None
    except Exception:
        print('请求页面失败', url)
        return None

#获取股票代码
def get_stocks(url,num,pattern):
    cookie=get_cookie()
    print('cookie:'+cookie)
    stock_codes = []
    if num:
        for i in range (1,num):
            url1 = url.format(str(i))
            html = get_page_detail(url1,cookie)
            for stock_code in re.findall(pattern, html):
                stock_codes.append(stock_code)
    else:
        html = get_page_detail(url, cookie)
        for stock_code in re.findall(pattern, html):
            stock_codes.append(stock_code)
    return stock_codes

# 获取k线数据
def get_klins(stock_codes,url,pattern1,pattern2):
    stocks_klin=[]
    num=0
    get_more(20)
    for stock_code in stock_codes:
        cookie = cookies[-1]
        num += 1
        if num%5 == 0:
            cookie = cookies[-1]
            print('cookie:' + cookie)
            if len(cookies) == 1:
                print(cookies)
                get_more(20)
                cookie = cookies[-1]
            cookies.pop()
        k_lins = {}
        url2 = url.format(str(stock_code))
        html = get_page_detail(url2,cookie)
        re_name = re.search(pattern1, html)
        re_data = re.search(pattern2, html)
        while not re_name:
            print('重新获取')
            cookie=get_cookie()
            html = get_page_detail(url2, cookie)
            re_name = re.search(pattern1, html)
            re_data = re.search(pattern2, html)
        name = re_name.group(1).encode('utf-8').decode('unicode_escape')
        datas = re_data.group(1).split(';')
        k_data = []
        for data in datas:
            lins = []
            lins.append(int(data.split(',')[0].lstrip()))
            if not data.split(',')[1]:
                break
            lins.append(float(data.split(',')[1].lstrip()))
            lins.append(float(data.split(',')[4].lstrip()))
            lins.append(float(data.split(',')[3].lstrip()))
            lins.append(float(data.split(',')[2].lstrip()))
            k_data.append(lins)
        k_lins["code"] = stock_code
        k_lins["name"] = name
        k_lins["data"] = k_data
        stocks_klin.append(k_lins)
        print(k_lins)
    return stocks_klin

def get_morestock():
    print('开始获取单个股票历时数据')
    thread_list=[]
    for i in range(10):
        thread = threading.Thread(target=getstocksdata)
        thread_list.append(thread)
    for t in thread_list:
        t.setDaemon(True)
        t.start()
    for t in thread_list:
        t.join()

def getcodes():
    # filebasic = 'D:\Python\workspeace\persionalweb\static\csvfile\stockbasic.csv'
    # dfstockbasic = pd.read_csv(filebasic, encoding="utf-8")
    dfstockbasic = ts.get_stock_basics()
    dfstockbasic['tomarket'] = pd.to_numeric(dfstockbasic.timeToMarket)
    dfstock = dfstockbasic[(dfstockbasic.tomarket <= 20151001)]
    dfstock['totals'] = pd.to_numeric(dfstock.totals)   #总股本(亿)
    dfstocks = dfstock[(dfstock.totals >= 30)]
    codes = []
    for index, row in dfstocks.iterrows():
        every={}
        every['code']=index
        every['name']=row['name']
        every['totals'] = row['totals']
        every['industry'] = row['industry']
        every['area'] = row['area']
        codes.append(every)
    return codes

def getstocksdata():
    datas=getcodes()
    stocksdata=[]
    for stockdata in datas:
        stocks={}
        shyha = ts.get_hist_data(stockdata['code'])
        minclose=np.nanmin(shyha.iloc[:200, 1].values)
        nowprice=shyha.iloc[0]['close']
        pricediff=round(minclose/nowprice,2)
        price_change=round(np.sum(shyha.iloc[:5]['price_change']),2)
        data=[]
        shyh=shyha.sort_index()
        for row in shyh.index:
            oneday = []
            oneday.append(row)
            oneday.append(shyh.loc[row, 'open'])
            oneday.append(shyh.loc[row, 'close'])
            oneday.append(shyh.loc[row, 'low'])
            oneday.append(shyh.loc[row, 'high'])
            data.append(oneday)
        stocks["code"] = stockdata['code']
        stocks["name"] = stockdata['name']
        stocks["industry"] = stockdata['industry']
        stocks["area"] = stockdata['area']
        stocks["totals"] = stockdata['totals']
        stocks["price_change"] = price_change
        stocks["pricediff"] = pricediff
        stocks["data"] = data
        if 10>price_change>0:
            stocksdata.append(stocks)
            print(minclose)
            print(nowprice)
            print(stocks)
    stocksdata.sort(key=lambda x: x["pricediff"])
    return stocksdata
