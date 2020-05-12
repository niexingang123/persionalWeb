from selenium import webdriver
import threading

# 获取动态cookies
cookies=[]
def get_cookie():
    print('开始获取cookie')
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)
    url = "http://q.10jqka.com.cn/thshy/"
    driver.get(url)
    # 获取cookie列表
    cookie = driver.get_cookies()
    driver.close()
    cookies.append(cookie[0]['value'])
    print('获取结束')
    # return cookie[0]['value']

thread_list=[]
for i in range(20):
    thread = threading.Thread(target=get_cookie)
    thread_list.append(thread)
for t in thread_list:
    t.setDaemon(True)
    t.start()
for t in thread_list:
    t.join()
print(cookies)