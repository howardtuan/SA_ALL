from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from datetime import datetime

from django.urls import reverse
from myapp.models import client
from django.http import Http404
from django.contrib import auth,messages
from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, get_list_or_404 # 快捷函数

# Create your views here.


def main(request):
    if request.user.is_authenticated:
        # account = "888"
        user_phone = request.user
        user = client.objects.get(PHONE_NUMBER = user_phone)
        user_name=user.NAME
        user_point=user.POINT
        user_barcode=user.PHONE_NUMBER
    return render(request, 'index.html', locals())

def index_view(request):
    if request.user.is_authenticated:
        # account = "888"
        account = request.user
        print(account)
        user = client.objects.get(PHONE_NUMBER = account)
        user_name=user.NAME
        user_point=user.POINT
        user_barcode=user.PHONE_NUMBER
    return render(request, 'index.html', locals())


def apps_view(request):
    return render(request, 'orthers_app.html', locals())

def exchange_view(request):
    return render(request, 'exchange.html', locals())

# 修改會員資料
def fix_view(request):
    if request.user.is_authenticated:
        user_phone = request.user
        user = client.objects.get(PHONE_NUMBER = user_phone)
        user_name = user.NAME
        user_point = user.POINT
        user_barcode = user.PHONE_NUMBER
        return render(request, 'fix.html', locals())
    else:
        messages.error(request, '您尚未登入，請先登入')
        return HttpResponseRedirect("/login/")

def fix(request):
    if(request.POST.get('password')!=request.POST.get('double_check')):
        messages.error(request, '密碼輸入不一致，請重新輸入')  
        return render(request, 'fix.html',locals())
    user_name = request.POST.get('username')
    user_phone = request.POST.get("phone_number")
    user_password = request.POST.get('password')
    client.objects.filter(PHONE_NUMBER = request.user).update(NAME = user_name, PASSWORD = user_password)
    
    # 驗證的資料庫（僅做密碼更新）
    user = User.objects.get(username = request.user)
    user.set_password(user_password)
    user.save()
    
    # auth.logout(request)
    # user = auth.authenticate(username = user_phone, password = user_password)
    # auth.login(request, user)
    messages.error(request, '會員資料已更新')
    return HttpResponseRedirect("/member/")

def history_view(request):
    if request.user.is_authenticated:
        return render(request, 'history.html', locals())
    else:
        messages.error(request, '您尚未登入，請先登入')
        return HttpResponseRedirect("/login/")

def login_view(request):
    return render(request, 'login.html', locals())

def member_view(request):
    if request.user.is_authenticated:
        user_phone = request.user
        user = client.objects.get(PHONE_NUMBER = user_phone)
        user_name=user.NAME
        user_point=user.POINT
        user_barcode=user.PHONE_NUMBER
        return render(request, 'member.html', locals())
    else:
        messages.error(request, '您尚未登入，請先登入')
        return HttpResponseRedirect("/login/")

def myself_view(request):
    return render(request, 'myself.html', locals())

def question_view(request):
    return render(request, 'question.html', locals())

def signup_view(request):
    return render(request, 'signup.html', locals())

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/index/')

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
    User.objects.create_user(username = request.POST.get('uphone'), password = request.POST.get('upwd')) # 驗證的資料庫
    client.objects.create(NAME = request.POST.get('uname'),PHONE_NUMBER=request.POST.get('uphone'),PASSWORD=request.POST.get('upwd'),POINT=0)
    return HttpResponseRedirect('/login/')

#登入
def login(request):
    if request.user.is_authenticated:
        print("is auth")
        return HttpResponseRedirect('/index/')
    count = client.objects.filter(PHONE_NUMBER = request.POST['uphone']).count()
    print("count",count)
    if count==0:
        messages.error(request, '帳號或密碼錯誤')  
        return render(request, 'login.html', locals())
    m = client.objects.get(PHONE_NUMBER = request.POST['uphone'])
    if m.PASSWORD != request.POST['upwd']:
        messages.error(request, '帳號或密碼錯誤')  
        return render(request, 'login.html', locals())
    username = request.POST.get('uphone', '')
    password = request.POST.get('upwd', '')
    user = auth.authenticate(username = username, password = password)
    if user is not None and user.is_active:
        print(user)
        print('user.is_active')
        auth.login(request, user)
        return HttpResponseRedirect('/index/')
    else:
        print(user)
        print('user.n_active')
        return render(request, 'login.html', locals())
