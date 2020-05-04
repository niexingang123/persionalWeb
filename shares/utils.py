import requests,re
from selenium import webdriver

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
    cookie=get_cookie()
    stocks_klin=[]
    num=0
    for stock_code in stock_codes:
        num += 1
        if num%10 == 0:
            cookie = get_cookie()
        k_lins = {}
        url2 = url.format(str(stock_code))
        html = get_page_detail(url2,cookie)
        re_name = re.search(pattern1, html)
        re_data = re.search(pattern2, html)
        if re_name:
            name = re_name.group(1).encode('utf-8').decode('unicode_escape')
            datas = re_data.group(1).split(';')
            k_data = []
            for data in datas:
                lins = []
                lins.append(int(data.split(',')[0].lstrip()))
                lins.append(float(data.split(',')[1].lstrip()))
                lins.append(float(data.split(',')[4].lstrip()))
                lins.append(float(data.split(',')[3].lstrip()))
                lins.append(float(data.split(',')[2].lstrip()))
                k_data.append(lins)
            k_lins["code"] = stock_code
            k_lins["name"] = name
            k_lins["data"] = k_data
            stocks_klin.append(k_lins)
        else:
            print("没匹配到值")
    return stocks_klin

