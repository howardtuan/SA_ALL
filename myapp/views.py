from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from datetime import datetime

from django.urls import reverse
from myapp.models import client
from django.http import Http404
from django.contrib import auth,messages
# from django.shortcuts import get_object_or_404, get_list_or_404 # 快捷函数

# Create your views here.


def main(request):
    return render(request, 'index.html', {
        'user_name':"none",
        'user_point':"none",
        'user_barcode':"none",
    } )
    
def index_view(request):
    account="888"
    user=client.objects.get(PHONE_NUMBER=account)
    user_name=user.NAME
    user_point=user.POINT
    user_barcode=user.PHONE_NUMBER
    return render(request, 'index.html', locals())
def apps_view(request):
    return render(request, 'orthers_app.html', locals())
def exchange_view(request):
    return render(request, 'exchange.html', locals())
def fix_view(request):
    return render(request, 'fix.html', locals())
def history_view(request):
    return render(request, 'history.html', locals())
def login_view(request):
    return render(request, 'login.html', locals())
def member_view(request):
    return render(request, 'member.html', locals())
def myself_view(request):
    return render(request, 'myself.html', locals())
def question_view(request):
    return render(request, 'question.html', locals())
def signup_view(request):
    return render(request, 'signup.html', locals())

#註冊
def signup(request):
    if(request.POST.get('upwd')!=request.POST.get('upwd2')):
        messages.error(request, '密碼輸入不一致，請重新輸入')  
        return render(request, 'signup.html',locals())
    newphone=request.POST.get('uphone')
    # check_account = client.objects.filter(PHONE_NUMBER=newphone).first()
    # print(check_account)
    # print(type(check_account))
    # if(check_account!="None"):
    #     messages.error(request, '此組手機號碼已註冊過，請勿重複註冊')  
    #     return render(request, 'signup.html',locals())
    count = client.objects.filter(PHONE_NUMBER=newphone).count()
    if count!=0:
        messages.error(request, '此組手機號碼已註冊過，請勿重複註冊')  
        return render(request, 'signup.html',locals())
    messages.error(request, '註冊成功！')  
    client.objects.create(NAME=request.POST.get('uname'),PHONE_NUMBER=request.POST.get('uphone'),PASSWORD=request.POST.get('upwd'),POINT=0)
    return render(request, 'login.html',locals())
#登入
def login(request):
    count = client.objects.filter(PHONE_NUMBER=request.POST['uphone']).count()
    if count==0:
        messages.error(request, '帳號或密碼錯誤')  
        return render(request, 'login.html', locals())
    m = client.objects.get(PHONE_NUMBER=request.POST['uphone'])
    if m.PASSWORD != request.POST['upwd']:
        messages.error(request, '帳號或密碼錯誤')  
        return render(request, 'login.html', locals())
    else: 
        return HttpResponseRedirect('/index/')
#登入帳號語法
def logintest(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/index/')
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('/index/')
    else:
        return render(request, 'login.html', locals())