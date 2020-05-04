import time
from django.shortcuts import render
import requests,re
from selenium import webdriver
from shares import models

def index(request):
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'index.html', context)

# 获取动态cookies
def get_cookie():
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=options)
        url = "http://q.10jqka.com.cn/thshy/"
        driver.get(url)
        # 获取cookie列表
        cookie = driver.get_cookies()
        driver.close()
        return cookie[0]['value']

#获取页面
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

def get_new():
    num=0
    cookie=get_cookie()
    models.Klins.objects.all().delete()
    stock_codes = []
    for i in (1, 2):
        url = 'http://q.10jqka.com.cn/thshy/index/field/199112/order/desc/page/' + str(i) + '/ajax/1/'
        html = get_page_detail(url,cookie)
        pattern = r'href="http://q.10jqka.com.cn/thshy/detail/code/(.*?)/".*?target="_blank"'
        for stock_code in re.findall(pattern, html):
            stock_codes.append(stock_code)
    k_lins = {}
    for stock_code in stock_codes:
        num+=1
        if num%20 == 0:
            cookie = get_cookie()
        # time.sleep(2)
        url = 'http://d.10jqka.com.cn/v4/line/bk_' + str(stock_code) + '/01/last.js'
        html = get_page_detail(url,cookie)
        ret = re.search('"name":"(.*?)","data"', html)
        ret1 = re.search('"data":"(.*?)","marketType', html)
        if ret:
            name = ret.group(1).encode('utf-8').decode('unicode_escape')
            datas = ret1.group(1).split(';')
            stocks = []
            for data in datas:
                lins = []
                lins.append(int(data.split(',')[0].lstrip()))
                lins.append(float(data.split(',')[1].lstrip()))
                lins.append(float(data.split(',')[4].lstrip()))
                lins.append(float(data.split(',')[3].lstrip()))
                lins.append(float(data.split(',')[2].lstrip()))
                stocks.append(lins)
            k_lins[name] = stocks
            print(stock_code)
            print(name)
            print(stocks)
            models.Klins.objects.create(code=str(stock_code), name=name, data=str(stocks))
        else:
            print("没匹配到值")

def gupiao(request):
    add_time=''
    if models.Klins.objects.all():
        add_time = models.Klins.objects.all().first().addtime
    add_date = str(add_time)[:10]
    new_date = str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
    if add_date != new_date:
        get_new()
    Dict=models.Klins.objects.all()
    return render(request, 'gupiao.html', {'Dict': Dict})

def hangye(request):
    Dict=models.Klins.objects.all()
    return render(request, 'hangye.html', {'Dict': Dict})