import time,json
from django.shortcuts import render,HttpResponse
from . import models
from . import utils
from threading import Thread

def index(request):
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'index.html', context)

def gupiao(request):
    return render(request, 'gupiao.html')

def async_call(fn):
    def wrapper(*args, **kwargs):
        Thread(target=fn, args=args, kwargs=kwargs).start()
    return wrapper

@async_call
def get_hangyenewdata():
    url = 'http://q.10jqka.com.cn/thshy/index/field/199112/order/desc/page/{}/ajax/1/'
    num = 3
    pattern = r'href="http://q.10jqka.com.cn/thshy/detail/code/(.*?)/".*?target="_blank"'
    stock_codes = utils.get_stocks(url, num, pattern)
    url = 'http://d.10jqka.com.cn/v4/line/bk_{}/01/last.js'
    pattern1 = '"name":"(.*?)","data"'
    pattern2 = '"data":"(.*?)","marketType'
    klins = utils.get_klins(stock_codes, url, pattern1, pattern2)
    models.Klins.objects.filter(flag='hangye').delete()
    nid = 0
    for klin in klins:
        models.Klins.objects.create(fid=nid, code=klin["code"], name=klin["name"], data=klin["data"], flag='hangye')
        nid += 1
    print('行业数据已存入数据库')

def gupiao_ajax(request):
    nid = request.GET.get('nid')
    last_position_id = int(nid) + 9
    position_id = str(last_position_id)
    add_time=''
    if models.Klins.objects.filter(flag='hangye'):
        add_time = models.Klins.objects.filter(flag='hangye').first().addtime
    add_date = str(add_time)[:10]
    new_date = str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
    if add_date != new_date:
        get_hangyenewdata()
    ret = {'status': True, 'data': None}
    image_list = models.Klins.objects.filter(fid__gt=nid, fid__lt=position_id, flag='hangye').values('fid', 'code', 'name', 'data')
    image_list = list(image_list)
    ret['data'] = image_list
    return HttpResponse(json.dumps(ret))

def gainian(request):
    return render(request, 'gupiao.html')

@async_call
def getgainiandata():
    url = 'http://q.10jqka.com.cn/gn/'
    num = None
    pattern = r'"platecode":"(.*?)","platename":"'
    stock_codes = utils.get_stocks(url, num, pattern)
    url = 'http://d.10jqka.com.cn/v4/line/bk_{}/01/last.js'
    pattern1 = '"name":"(.*?)","data"'
    pattern2 = '"data":"(.*?)","marketType'
    klins = utils.get_klins(stock_codes, url, pattern1, pattern2)
    models.Klins.objects.filter(flag='gainian').delete()
    nid = 0
    for klin in klins:
        models.Klins.objects.create(fid=nid, code=klin["code"], name=klin["name"], data=klin["data"], flag='gainian')
        nid += 1
    print('概念数据已存入数据库')

def gainian_ajax(request):
    nid = request.GET.get('nid')
    last_position_id = int(nid) + 9
    position_id = str(last_position_id)
    add_time=''
    if models.Klins.objects.filter(flag='gainian'):
        add_time = models.Klins.objects.filter(flag='gainian').first().addtime
    add_date = str(add_time)[:10]
    new_date = str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
    if add_date != new_date:
        getgainiandata()
    ret = {'status': True, 'data': None}
    image_list = models.Klins.objects.filter(fid__gt=nid, fid__lt=position_id, flag='gainian').values('fid', 'code','name', 'data')
    image_list = list(image_list)
    ret['data'] = image_list
    return HttpResponse(json.dumps(ret))

def seach_byname(request):
    name = request.POST.get('name', '')
    if name:
        Dict=models.Klins.objects.filter(name__contains=name)
    else:
        Dict = models.Klins.objects.filter(flag='hangye')
    return render(request, 'gupiao.html', {'Dict': Dict})

def hangye(request):
    return render(request, 'hangye.html')

def hangye_ajax (request):
    nid = request.GET.get('nid')
    last_position_id = int(nid) + 5
    position_id = str(last_position_id)
    print(nid,'>>>>>>position_id', position_id)

    ret = {'status': True, 'data': None}
    image_list = models.Klins.objects.filter(fid__gt=nid, fid__lt=position_id).values('fid', 'code', 'name', 'data')
    image_list = list(image_list)
    ret['data'] = image_list
    return HttpResponse(json.dumps(ret))

def getevery(request):
    return render(request, 'gupiao.html')

@async_call
def geteverystock():
    everydatas=utils.getstocksdata()
    nid = 0
    models.Stocks.objects.all().delete()
    for every in everydatas:
        nid += 1
        models.Stocks.objects.create(fid=nid, code=every["code"], name=every["name"], industry=every["industry"], area=every["area"], price_change=every["price_change"], pricediff=every["pricediff"], totals=every["totals"], data=every["data"])
    print('个股数据已存入数据库')

def getevery_ajax(request):
    nid = request.GET.get('nid')
    last_position_id = int(nid) + 9
    position_id = str(last_position_id)
    add_time=''
    if models.Stocks.objects.all():
        add_time = models.Stocks.objects.all().first().addtime
    add_date = str(add_time)[:10]
    new_date = str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
    if add_date != new_date:
        geteverystock()
    ret = {'status': True, 'data': None}
    image_list = models.Stocks.objects.filter(fid__gt=nid, fid__lt=position_id).values('fid', 'code','name', 'industry','area', 'data')
    image_list = list(image_list)
    ret['data'] = image_list
    return HttpResponse(json.dumps(ret))