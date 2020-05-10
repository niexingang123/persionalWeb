import time,json
from django.shortcuts import render,HttpResponse
from . import models
from . import utils

def index(request):
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'index.html', context)

def gupiao(request):
    return render(request, 'gupiao.html')

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
        models.Klins.objects.filter(flag='hangye').delete()
        url = 'http://q.10jqka.com.cn/thshy/index/field/199112/order/desc/page/{}/ajax/1/'
        num = 3
        pattern = r'href="http://q.10jqka.com.cn/thshy/detail/code/(.*?)/".*?target="_blank"'
        stock_codes=utils.get_stocks(url,num,pattern)
        url = 'http://d.10jqka.com.cn/v4/line/bk_{}/01/last.js'
        pattern1 = '"name":"(.*?)","data"'
        pattern2 = '"data":"(.*?)","marketType'
        klins=utils.get_klins(stock_codes, url, pattern1, pattern2)
        nid = 0
        for klin in klins:
            models.Klins.objects.create(fid=nid, code=klin["code"], name=klin["name"], data=klin["data"], flag='hangye')
            nid += 1
    ret = {'status': True, 'data': None}
    image_list = models.Klins.objects.filter(fid__gt=nid, fid__lt=position_id, flag='hangye').values('fid', 'code', 'name', 'data')
    image_list = list(image_list)
    ret['data'] = image_list
    return HttpResponse(json.dumps(ret))

def gainian(request):
    return render(request, 'gupiao.html')

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
        models.Klins.objects.filter(flag='gainian').delete()
        url = 'http://q.10jqka.com.cn/gn/'
        num = None
        pattern = r'"platecode":"(.*?)","platename":"'
        stock_codes=utils.get_stocks(url,num,pattern)
        url = 'http://d.10jqka.com.cn/v4/line/bk_{}/01/last.js'
        pattern1 = '"name":"(.*?)","data"'
        pattern2 = '"data":"(.*?)","marketType'
        klins=utils.get_klins(stock_codes, url, pattern1, pattern2)
        nid = 0
        for klin in klins:
            models.Klins.objects.create(fid=nid, code=klin["code"], name=klin["name"], data=klin["data"], flag='gainian')
            nid += 1
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
