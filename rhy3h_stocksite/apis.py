from django.http import JsonResponse

from bs4 import BeautifulSoup
import requests
from .models import Group
from .fubon import *

def fubon(request):
    User = request.user
    group_id = request.GET.get('group_id')
    select_begin_date = request.GET.get('begin_date')
    select_end_date = request.GET.get('end_date')
    
    group = Group.objects.get(id = group_id, Owner=User)
    group_brokers_list = group.Brokers.split(';')
    broker_branch = []

    for item in group_brokers_list:
        split_item = item.split(',')
        broker_id = split_item[0]
        branch_id = split_item[1]
        broker_branch.append([broker_id, branch_id])
    stock_list = fubon_get_list(broker_branch, select_begin_date, select_end_date)
    
    return JsonResponse(stock_list, safe=False)

def wantgoo(request):
    stock_id = request.GET.get('stock_id')
    data = []
    
    url = "https://www.wantgoo.com/stock/" + stock_id + "/institutional-investors/trend-data?topdays=10"

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    }

    resource_page = requests.get(url,headers = headers)
    resource_page.encoding = 'utf-8'
    
    for item in resource_page.json():
        temp = {}
        sumForeign = item['sumForeignWithDealer'] + item['sumForeignNoDealer']
        sumING = item['sumING']
        sumDealer = item['sumDealerBySelf'] + item['sumDealerHedging']
        
        temp['date'] = item['date'][5:10]
        temp['sumForeign'] = sumForeign
        temp['sumING'] = sumING
        temp['sumDealer'] = sumDealer
        data.append(temp)
        
    return JsonResponse(data, safe=False)