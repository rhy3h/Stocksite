from datetime import datetime, timedelta

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User

from .models import Group
from .fubon import *

from django.http import JsonResponse
import json

def update(request):
    User = request.user
    group_id = request.GET.get('group_id')
    group = Group.objects.get(id = group_id, Owner=User)
    group_brokers_list = group.Brokers.split(';')
    new_group_brokers_list = ""
    i = 0
    while request.GET.get(str(i)) != None:
        broker_id = request.GET.get(str(i))
        for item in group_brokers_list:
            if item.find(broker_id) >= 0:
                if len(new_group_brokers_list) == 0:
                    new_group_brokers_list = item
                else:
                    new_group_brokers_list += ";" + item
                break
        i = i + 1
    group.Brokers = new_group_brokers_list
    group.save()
    
    data = {}
    return JsonResponse(data)

@login_required
def index(request):
    title = '股票神器'

    User = request.user
    group_list = Group.objects.filter(Owner=User)
    select_begin_date = datetime.now().strftime('%Y-%m-%d')
    select_end_date = datetime.now().strftime('%Y-%m-%d')
    interval_month = {
        "假的"
        }
    if request.GET.get('group_id') != None:
        group_id = int(request.GET.get('group_id'))
        group = Group.objects.get(id = group_id)
        
        if request.GET.get('begin_date') != None:
            select_begin_date = request.GET.get('begin_date')
        if request.GET.get('end_date') != None:
            select_end_date = request.GET.get('end_date')
        if select_begin_date > select_end_date:
            select_begin_date, select_end_date = select_end_date, select_begin_date
        if request.GET.get('interval_month') != None:
            select_interval_month = int(request.GET.get('interval_month'))
            select_begin_date = count_begin_date(datetime.strptime(select_end_date, '%Y-%m-%d'), select_interval_month)

        if len(group.Brokers) != 0:
            group_brokers_list = group.Brokers.split(';')
            html_broker_list = []
            
            for item in group_brokers_list:
                split_item = item.split(',')
                branch_id = split_item[1]
                html_broker_list.append(get_id_name(branch_id))
    
    return render(request, 'dashboard.html', locals())

def count_begin_date(end_date, interval_index):
    begin_date = ''

    if interval_index == 0:
        begin_date = end_date
    elif interval_index == 1:
        begin_date = end_date - timedelta(days=7)
    elif interval_index == 2:
        begin_date = end_date - timedelta(days=14)
    elif interval_index == 3:
        begin_date = end_date - timedelta(days=30)
    elif interval_index == 4:
        begin_date = end_date - timedelta(days=90)
    elif interval_index == 5:
        begin_date = end_date - timedelta(days=180)
    elif interval_index == 6:
        begin_date = end_date - timedelta(days=360)
    
    return begin_date.strftime('%Y-%m-%d')

def export_list(request):
    if request.GET.get('group_id') != None:
        group_id = request.GET.get('group_id')
        print(group_id)
        group_brokers = Group.objects.get(id = group_id).Brokers
        
        filename = group_id + ".txt"
        content = group_brokers
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    
        return response

def import_list(request):
    if request.method == 'POST' and request.GET.get('group_id') != None:
        group_id = request.GET.get('group_id')
        try:
            doc = request.FILES['import_list_file']
            group = Group.objects.get(id = group_id)
            if len(group.Brokers) == 0:
                group.Brokers = doc.read().decode("utf-8")
            else:
                group.Brokers += ";" + doc.read().decode("utf-8")
            group.save()
        except:
            pass
    
        return redirect('/dashboard/query?group_id=' + group_id)

@login_required
def create_group(request):
    if request.method == "POST":
        new_group_name = request.POST['new_group_name']
        user = request.user
        Group.objects.get_or_create(Owner = user,
                                Groupname = new_group_name,
                                Brokers = "")
        new_group_id = str(Group.objects.last().id)
        return redirect('/dashboard/query?group_id=' + new_group_id)

@login_required
def del_group(request):
    if request.GET.get('group_id') != None:
        user = request.user
        group_id = request.GET.get('group_id')
        group = Group.objects.filter(Owner=user).get(id = group_id)
        group.delete()

        try:
            first_group_id = str(Group.objects.filter(Owner=user).first().id)
            return redirect('/dashboard/query?group_id=' + first_group_id)
        except:
            return redirect('/dashboard/')

@login_required
def add_broker(request):
    if request.method == "POST" and request.GET.get('group_id') != None:
        group_id = request.GET.get('group_id')
        group = Group.objects.filter(Owner=request.user).get(id = group_id)
        
        broker_id = str(request.POST['select_broker'])
        branch_id = str(request.POST['select_branch'])
        input_text = str(broker_id) + ',' + str(branch_id)
        
        try:
            group.Brokers.split(';').index(input_text)
        except:
            if len(group.Brokers) == 0:
                group.Brokers = input_text
                group.save()
            else:
                group.Brokers = group.Brokers + ";" + input_text
                group.save()

        return redirect('/dashboard/query?group_id=' + group_id)

@login_required
def del_broker(request):
    if request.GET.get('group_id') != None:
        user = request.user

        group_id = request.GET.get('group_id')
        
        broker_index = int(request.GET.get('broker_index'))
        
        group = Group.objects.filter(Owner=user).get(id = group_id)
        group_brokers = list(group.Brokers.split(";"))
        
        for i in range(len(group_brokers)):
            if broker_index == i:
                group_brokers.remove(group_brokers[i])
        
        if len(group_brokers) == 0:
            input_text = ''
        elif len(group_brokers) == 1:
            input_text = group_brokers[0]
        else:
            input_text = group_brokers[0]
            for i in range(1, len(group_brokers)):
                input_text = input_text + ';' + group_brokers[i]
        group.Brokers = input_text
        group.save()

        return redirect('/dashboard/query?group_id=' + group_id)