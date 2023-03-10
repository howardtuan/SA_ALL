from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from datetime import datetime,timezone,timedelta
import time
from django.urls import reverse
from myapp.models import *
from django.http import Http404
from django.contrib import auth,messages
from django.contrib.auth.models import User
from django.db.models import Count
# from django.shortcuts import get_object_or_404, get_list_or_404 # 快捷函数
from sa2 import settings
from barcode import EAN13
from barcode.writer import ImageWriter 
# from django.utils.timezone import activate
# activate(settings.TIME_ZONE)
# Create your views here.


def main(request):
    if request.user.is_authenticated:
        # account = "888"
        user_phone = request.user
        user = client.objects.get(PHONE_NUMBER = user_phone)
        user_name=user.NAME
        user_point=user.POINT
        user_barcode=user.PHONE_NUMBER
        user_photo = user.PHOTO
    return render(request, 'index.html', locals())

def index_view(request):
    if request.user.is_authenticated:
        # account = "888"
        account = request.user
        user = client.objects.get(PHONE_NUMBER = account)
        user_name=user.NAME
        user_point=user.POINT
        user_barcode=user.PHONE_NUMBER
        user_photo = user.PHOTO
    return render(request, 'index.html', locals())


def apps_view(request):
    return render(request, 'orthers_app.html', locals())

def exchange_view(request):
    if request.user.is_authenticated:
        user_phone = request.user
        user = client.objects.get(PHONE_NUMBER = user_phone)
        user_point = user.POINT
        items = EXCHANGE_ITEM.objects.all()
        # for item in items:
        #     print(item.ID)

        return render(request, 'exchange.html', locals())
    else:
        messages.error(request, '您尚未登入，請先登入')
        return HttpResponseRedirect("/login/")

def exchange(request):
    if request.user.is_authenticated:
        user_phone = request.user
        user = client.objects.get(PHONE_NUMBER = user_phone)
        user_point = user.POINT
        item_id = request.POST.get("item_id")
        item_name = request.POST.get("item_name")
        item_cost = int(request.POST.get("item_cost"))
        if user_point < item_cost:
            messages.error(request, '您的點數需大於兌換點數！')
            return HttpResponseRedirect("/exchange/")
        
        client.objects.filter(PHONE_NUMBER = request.user).update(POINT = (user_point - item_cost))
        EXCHANGE.objects.create(USER_PHONE = user_phone, COST = item_cost, ITEM_ID = item_id, DATE = datetime.now(), ITEM_NAME = item_name, USED = False)
        messages.error(request, '兌換成功')
        return HttpResponseRedirect("/exchange/")
    else:
        messages.error(request, '您尚未登入，請先登入')
        return HttpResponseRedirect("/login/")

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
        exchange_list = EXCHANGE.objects.filter(USER_PHONE = request.user).order_by('-DATE').all()
        
        
        return render(request, 'history.html', locals())
    else:
        messages.error(request, '您尚未登入，請先登入')
        return HttpResponseRedirect("/login/")

def history_otherAPP_view(request):
    if request.user.is_authenticated:
        history_list = HISTORY.objects.filter(USER_PHONE = request.user).all()
        
        return render(request, 'history_otherAPP.html', locals())
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
        user_photo = user.PHOTO
        return render(request, 'member.html', locals())
    else:
        messages.error(request, '您尚未登入，請先登入')
        return HttpResponseRedirect("/login/")

def percentcheck(phone):
    #要select所有人的手機及點數分別匯入兩個陣列
    #這邊假設已經select完
    sum=0
    memberindex=0
    member = client.objects.all()
    AllPhone=[]
    AllPoint=[]
    for data in member:
        print(data.PHONE_NUMBER)
        AllPhone.append(data.PHONE_NUMBER)
        print(data.POINT)
        AllPoint.append(data.POINT)
    dict={}
    for i in range(len(AllPhone)):
        dict[AllPhone[i]] = AllPoint[i]
        sum+=1
    
    sorted_dict = sorted(dict.items(), key=lambda x:x[1])
    for i in range(len(sorted_dict)):
        if sorted_dict[i][0]==phone:
            memberindex=i
    print(sorted_dict)
    point=sorted_dict[memberindex][1]

    
    urank=len(sorted_dict)-sorted_dict.index(sorted_dict[memberindex])

    # PR計算：(100/N*贏過的人數)+(100/N/2)
    pr=int(round((100/len(sorted_dict)*(len(sorted_dict)-urank))+(100/len(sorted_dict)/2),0))
    
    return point,pr

def rankcheck(point_chenck,pr_check):
    rank=["銅牌","銀牌","金牌","白金","鑽石","菁英"]
    if point_chenck > 50000 or (point_chenck>30000 and pr_check>80):
        return rank[4],rank[5]
    elif point_chenck > 20000 or (point_chenck>15000 and pr_check>60):
        return rank[3],rank[4]
    elif point_chenck > 10000 or (point_chenck>7500 and pr_check>40):
        return rank[2],rank[3]
    elif point_chenck > 5000 or (point_chenck>2000 and pr_check>20):
        return rank[1],rank[2]
    else:
        return rank[0],rank[1]

def myself_view(request):
    if request.user.is_authenticated:
        user_phone = request.user
        user = client.objects.get(PHONE_NUMBER = user_phone)
        user_name=user.PHONE_NUMBER
        user_point=user.POINT
        member = client.objects.all()
        for data in member:
            print(data.PHONE_NUMBER)
            
            print(data.POINT)
        UserPoint=percentcheck(str(user_phone))[0]
        UserPR=percentcheck(str(user_phone))[1] 
        UserRank_Now=rankcheck(UserPoint,UserPR)[0]
        UserRank_Next=rankcheck(UserPoint,UserPR)[1]
        UserRankURL_Now="" 
        UserRankURL_Next=""
        print(UserPoint,UserPR,UserRank_Now)
        if UserRank_Now=="銅牌":
            UserRankURL_Now="rk1.png"
            UserRankURL_Next="rk2.png"
        elif UserRank_Now=="銀牌":
            UserRankURL_Now="rk2.png"
            UserRankURL_Next="rk3.png"
        elif UserRank_Now=="金牌":
            UserRankURL_Now="rk3.png"
            UserRankURL_Next="rk4.png"
        elif UserRank_Now=="白金":
            UserRankURL_Now="rk4.png"
            UserRankURL_Next="rk5.png"
        elif UserRank_Now=="鑽石":
            UserRankURL_Now="rk5.png"
            UserRankURL_Next="rk6.png"
        else:
            UserRankURL_Now="rk6.png"
            UserRankURL_Next="rk6.png"

        
        return render(request, 'myself.html', locals())
    else:
        messages.error(request, '您尚未登入，請先登入')
        return HttpResponseRedirect("/login/")

def tickets_view(request):
    if request.user.is_authenticated:
        tickets = EXCHANGE.objects.filter(USER_PHONE = request.user,  USED = False).all()
        total_tickets = tickets.count()
        tickets_group = tickets.values("ITEM_ID").annotate(Count("ITEM_ID"))
        items = []
        for item in tickets_group:
            ITEM_NAME = EXCHANGE_ITEM.objects.filter(ID = item["ITEM_ID"]).all()
            tmp = [item["ITEM_ID"], ITEM_NAME[0].NAME, item["ITEM_ID__count"]]
            items.append(tmp)

        
        user_phone = request.user
        user = client.objects.get(PHONE_NUMBER = user_phone)
        user_point=user.POINT
        #查詢此帳號是否insert過DRIVE 有的話就UPDATE `TIME`跟`USING` 沒有則CREATE
        #按下「開始使用」時，`TIME`設為now()，`USING`設為TRUE，並寫條件式：if `USING`==TRUE:要一直計算時間
        #按下「結束使用」前，要一直用now()去減掉`TIME`，並印出「分鐘」ex:目前使用：{{ spent_time }}分鐘
        #按下「結束使用」後，`USING`設為FALSE，計算使用時間所換算而得的花費，並將相關資料存入至歷史紀錄(另一個func)
        count = DRIVE.objects.filter(USER_PHONE = user_phone).count()
        
        if count==0:
            pass
        elif DRIVE.objects.get(USER_PHONE = user_phone).USING==True:
            use=DRIVE.objects.get(USER_PHONE = user_phone).USING
            t=DRIVE.objects.get(USER_PHONE = user_phone).TIME
            t2=DRIVE.objects.get(USER_PHONE = user_phone).TIME+timedelta(hours=8)     
            
            spent=driveTime(request.user,str(t2)[0:19])
            if spent <= 30:
                cost=2000
            else:
                i=1
                while spent>30*i:
                    i+=1
                cost=2000*i
            if user_point<cost:
                #強制結束
                DRIVE.objects.filter(USER_PHONE = user_phone).update(USING=False)
                # DRIVE.objects.get(USER_PHONE = user_phone).USING=False
                overtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                starttime=str(DRIVE.objects.get(USER_PHONE = user_phone).TIME+timedelta(hours=8))[0:19]
                start_timestruct = datetime.strptime(starttime, "%Y-%m-%d %H:%M:%S")
                overtime_timestruct = datetime.strptime(overtime, "%Y-%m-%d %H:%M:%S")
                total_seconds = (overtime_timestruct - start_timestruct).total_seconds()
                total_time = int(total_seconds / 60)
                print("spent time",total_time)
                #存入資料庫
                #存入資料庫
                client.objects.filter(PHONE_NUMBER = request.user).update(POINT = (user_point - cost))
                EXCHANGE.objects.create(USER_PHONE = user_phone, COST = cost, ITEM_ID = 87, DATE = datetime.now(), ITEM_NAME = '駕駛瑪莎拉蒂', USED = True)

        elif DRIVE.objects.get(USER_PHONE = user_phone).USING==False:
            use=DRIVE.objects.get(USER_PHONE = user_phone).USING
        return render(request, 'tickets.html', locals())
    else:
        messages.error(request, '您尚未登入，請先登入')
        return HttpResponseRedirect("/login/")

def use_ticket(request):
    if request.user.is_authenticated:
        item_id = request.POST.get("item_id")
        exchanges =  EXCHANGE.objects.filter(USER_PHONE = request.user, ITEM_ID = item_id)
        for exchange in exchanges:
            if exchange.USED == False:
                id = exchange.ID
                break
        tickets = EXCHANGE.objects.filter(ID = id).update(USED = True)
        messages.error(request, '您已使用' + EXCHANGE_ITEM.objects.filter(ID = item_id)[0].NAME + '的使用卷')
        return HttpResponseRedirect("/tickets/")
    else:
        messages.error(request, '您尚未登入，請先登入')
        return HttpResponseRedirect("/login/")

def driveTime(account,start):
    
    start_timestruct = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
    end=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    end_timestruct = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
    total_seconds = (end_timestruct - start_timestruct).total_seconds()
    min_sub = int(total_seconds / 60)
    return min_sub

def drive(request):
    user_phone = request.user
    user = client.objects.get(PHONE_NUMBER = user_phone)
    user_point=user.POINT
    count = DRIVE.objects.filter(USER_PHONE = user_phone).count()
    if count==0:
                #沒用過
        start=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        start_timestruct = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
        DRIVE.objects.create(USER_PHONE = user_phone, NAME = 'DriveCar', TIME=start_timestruct, USING=True)
        return HttpResponseRedirect("/tickets/")
    elif DRIVE.objects.get(USER_PHONE = user_phone).USING==False:
                #用過
        start=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        start_timestruct = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
        DRIVE.objects.filter(USER_PHONE = user_phone).update(TIME = start_timestruct, USING=True)
        return HttpResponseRedirect("/tickets/")
    return HttpResponseRedirect("/tickets/")

def drive_over(request):
    if request.user.is_authenticated:
        user_phone = request.user
        user = client.objects.get(PHONE_NUMBER = user_phone)
        user_point=user.POINT
        DRIVE.objects.filter(USER_PHONE = user_phone).update(USING=False)
        # DRIVE.objects.get(USER_PHONE = user_phone).USING=False
        overtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        starttime=str(DRIVE.objects.get(USER_PHONE = user_phone).TIME+timedelta(hours=8))[0:19]
        start_timestruct = datetime.strptime(starttime, "%Y-%m-%d %H:%M:%S")
        overtime_timestruct = datetime.strptime(overtime, "%Y-%m-%d %H:%M:%S")
        total_seconds = (overtime_timestruct - start_timestruct).total_seconds()
        total_time = int(total_seconds / 60)
        print("spent time",total_time)
        if total_time <= 30:
            cost=2000
        else:
            i=1
            while total_time>30*i:
                i+=1
            cost=2000*i
        #存入資料庫
        client.objects.filter(PHONE_NUMBER = request.user).update(POINT = (user_point - cost))
        EXCHANGE.objects.create(USER_PHONE = user_phone, COST = cost, ITEM_ID = 87, DATE = datetime.now(), ITEM_NAME = '駕駛瑪莎拉蒂', USED = True)
        return HttpResponseRedirect("/tickets/")
    else:
        messages.error(request, '您尚未登入，請先登入')
        return HttpResponseRedirect("/login/")

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
    phone_number = request.POST.get('uphone')
    # check_account = client.objects.filter(PHONE_NUMBER=newphone).first()
    # print(check_account)
    # print(type(check_account))
    # if(check_account!="None"):
    #     messages.error(request, '此組手機號碼已註冊過，請勿重複註冊')  
    #     return render(request, 'signup.html',locals())
    count = client.objects.filter(PHONE_NUMBER = phone_number).count()
    if count!=0:
        messages.error(request, '此組手機號碼已註冊過，請勿重複註冊')  
        return render(request, 'signup.html',locals())
    messages.error(request, '註冊成功！')
    
    # 轉換barcode
    my_code = EAN13(phone_number.zfill(13), writer=ImageWriter())
    
    client.objects.create(NAME = request.POST.get('uname'), PHONE_NUMBER = phone_number, PASSWORD=request.POST.get('upwd'), POINT=0, PHOTO = my_code.save("static/barcode/" + phone_number))
    User.objects.create_user(username = phone_number, password = request.POST.get('upwd')) # 驗證的資料庫
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
