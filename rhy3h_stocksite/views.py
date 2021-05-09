from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm

def index(request):
    return render(request, 'index.html', locals())

def HelloWorld(request):
    return HttpResponse('Hello World')

def page_not_found(request, exception=None):
    title = '404'
    return render(request, '404.html', locals())

def internal_server_error(request, exception=None):
    title = '500'
    return render(request, '500.html', locals())

def register(request):
    return render(request, '500.html', locals())

def logout(request):
    auth.logout(request)
    return redirect('/accounts/login')