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
import requests
import json
from django.views.decorators.csrf import csrf_exempt
import random
from django.core.files.storage import FileSystemStorage

# from django.utils.timezone import activate
# activate(settings.TIME_ZONE)
# Create your views here.
SACCngrok="https://10eb-1-34-54-152.jp.ngrok.io"
serverngrok="https://315c-111-251-2-13.ngrok.io"

def access(request):
    results=client.objects.filter(PHONE_NUMBER = request.user)
    ac_code=''
    for result in results:
        ac_code = result.AC_CODE
    url2=SACCngrok+'/RESTapiApp/Access/?Raccess_code='+ac_code
    req2=requests.get(url2,headers = {'Authorization': 'Token fc350dd19927a48ed595b15586c7ea616c88a280','ngrok-skip-browser-warning': '7414'})
    
    req_read2 = req2.json()
    print(type(req2.status_code))
    if (req2.status_code!=200):
        print("================================")
        messages.error(request, '存取權已過期，請重新登入')
        logout(request)
    else:
    
        pic=req_read2["sPictureUrl"]
        print(pic)

        return pic

def main(request):
    if request.user.is_authenticated:
        # account = "888"
        user_phone = request.user
        user = client.objects.get(PHONE_NUMBER = user_phone)
        user_name=user.NAME
        user_point=user.POINT
        user_barcode=user.PHONE_NUMBER
        user_photo = user.PHOTO
        # user_myphoto = user.MYPHOTO
        user_tan=user.TANPI
        getpic=access(request)
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
        # user_myphoto = user.MYPHOTO
        user_tan=user.TANPI
        getpic=access(request)
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
        return HttpResponseRedirect("/login2/")

@csrf_exempt
def exchange(request):
    if request.user.is_authenticated:
        user_phone = request.user
        user = client.objects.get(PHONE_NUMBER = user_phone)
        user_point = user.POINT
        user_tanpi = user.TANPI
        item_id = request.POST.get("item_id")
        item_name = request.POST.get("item_name")
        item_cost = int(request.POST.get("item_cost"))
        item_tanpi = int(request.POST.get("item_tanpi"))
        if user_point < item_cost:
            messages.error(request, '您的點數需大於兌換點數！')
            return HttpResponseRedirect("/exchange/")
        
        client.objects.filter(PHONE_NUMBER = request.user).update(POINT = (user_point - item_cost),TANPI=(user_tanpi+item_tanpi))
        EXCHANGE.objects.create(USER_PHONE = user_phone, COST = item_cost, ITEM_ID = item_id, DATE = datetime.now(), ITEM_NAME = item_name, USED = False,TANPI=item_tanpi)
        messages.error(request, '兌換成功')
        return HttpResponseRedirect("/exchange/")
    else:
        messages.error(request, '您尚未登入，請先登入')
        return HttpResponseRedirect("/login2/")

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
        return HttpResponseRedirect("/login2/")

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

# 修改會員資料
def fix2_view(request):
    if request.user.is_authenticated:
        user_phone = request.user
        user = client.objects.get(PHONE_NUMBER = user_phone)
        user_name = user.NAME
        user_point = user.POINT
        user_barcode = user.PHONE_NUMBER
        return render(request, 'fix2.html', locals())
    else:
        messages.error(request, '您尚未登入，請先登入')
        return HttpResponseRedirect("/login2/")

@csrf_exempt
def fix2(request):
    user_name = request.POST.get('username')
    user_phone = request.POST.get("phone_number")
    client.objects.filter(PHONE_NUMBER = request.user).update(NAME = user_name)
    # if 'photo' in request.FILES:
    #     file = request.FILES['photo']
    #     fs = FileSystemStorage(location='static/pic')
    #     filename = fs.save(file.name, file)
    #     uploaded_file_url = fs.url(filename)
    #     print("1")
    #     # 更新模型的文件字段 my_code.save("static/barcode/" + phone_number)
    #     client.objects.filter(PHONE_NUMBER = user_phone).update(MYPHOTO = uploaded_file_url)

    messages.error(request, '會員資料已更新')
    return HttpResponseRedirect("/member/")

def history_view(request):
    if request.user.is_authenticated:
        exchange_list = EXCHANGE.objects.filter(USER_PHONE = request.user).order_by('-DATE').all()
        
        
        return render(request, 'history.html', locals())
    else:
        messages.error(request, '您尚未登入，請先登入')
        return HttpResponseRedirect("/login2/")

def history_otherAPP_view(request):
    if request.user.is_authenticated:
        history_list = HISTORY.objects.filter(USER_PHONE = request.user).all()
        
        return render(request, 'history_otherAPP.html', locals())
    else:
        messages.error(request, '您尚未登入，請先登入')
        return HttpResponseRedirect("/login2/")

def login_view(request):
    return render(request, 'login.html', locals())



def login2_view(request):
    sum=""
    rand=LOGIN.objects.create()
    # print(rand.FKcheck)
    # print(type(rand.FKcheck))
    url = SACCngrok+'/RESTapiApp/Line_1/?Rbackurl='+serverngrok+'/api2/?fk='+rand.FKcheck
    req=requests.get(url,headers = {'Authorization': 'Token fc350dd19927a48ed595b15586c7ea616c88a280','ngrok-skip-browser-warning': '7414'})
    print(req.json())
    req_read = req.json()
    print(req_read["Rstate"])
    LOGIN.objects.filter(FKcheck = rand.FKcheck).update(Rstate=req_read["Rstate"])
    firstLogin="https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id=1657781063&redirect_uri="+SACCngrok+"/LineLoginApp/callback&state="+req_read["Rstate"]+"&scope=profile%20openid%20email&promot=consent&ui_locales=zh-TW?http://example.com/?ngrok-skip-browser-warning=7414"

    return render(request, 'login2.html', locals())

def api2(request):
    if request.method == 'GET':
        fknum = request.GET.get('fk')
        nomatter=LOGIN.objects.filter(FKcheck = fknum)
        sum=''
        for i in nomatter:
            sum=i.Rstate
    url = SACCngrok+'/RESTapiApp/Line_2/?Rstate='+sum
    req=requests.get(url,headers = {'Authorization': 'Token fc350dd19927a48ed595b15586c7ea616c88a280','ngrok-skip-browser-warning': '7414'})
    req_read = req.json()
    print(req_read)
    userUID=req_read["RuserID"]
    access_code=req_read["Raccess_code"]
    print(req_read["Raccess_code"])

    return login2(request,userUID,access_code)
    

    
def member_view(request):
    if request.user.is_authenticated:
        user_phone = request.user
        user = client.objects.get(PHONE_NUMBER = user_phone)
        user_name=user.NAME
        user_point=user.POINT
        user_barcode=user.PHONE_NUMBER
        user_photo = user.PHOTO
        getpic=access(request)
        return render(request, 'member.html', locals())
    else:
        messages.error(request, '您尚未登入，請先登入')
        return HttpResponseRedirect("/login2/")

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
        return HttpResponseRedirect("/login2/")

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
        return HttpResponseRedirect("/login2/")
@csrf_exempt
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
        return HttpResponseRedirect("/login2/")

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
        DRIVE.objects.create(USER_PHONE = user_phone, NAME = 'DriveCar', TIME=start_timestruct, USING=True,TANPI=0)
        return HttpResponseRedirect("/tickets/")
    elif DRIVE.objects.get(USER_PHONE = user_phone).USING==False:
                #用過
        start=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        start_timestruct = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
        DRIVE.objects.filter(USER_PHONE = user_phone).update(TIME = start_timestruct, USING=True,TANPI=0)
        return HttpResponseRedirect("/tickets/")
    return HttpResponseRedirect("/tickets/")
@csrf_exempt
def drive_over(request):
    if request.user.is_authenticated:
        user_phone = request.user
        user = client.objects.get(PHONE_NUMBER = user_phone)
        user_point=user.POINT
        
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
        DRIVE.objects.filter(USER_PHONE = user_phone).update(USING=False,TANPI=total_time*100)
        #存入資料庫
        client.objects.filter(PHONE_NUMBER = request.user).update(POINT = (user_point - cost),TANPI=(user.TANPI+(total_time*100)))
        EXCHANGE.objects.create(USER_PHONE = user_phone, COST = cost, ITEM_ID = 87, DATE = datetime.now(), ITEM_NAME = '駕駛瑪莎拉蒂', USED = True,TANPI=total_time*100)
        return HttpResponseRedirect("/tickets/")
    else:
        messages.error(request, '您尚未登入，請先登入')
        return HttpResponseRedirect("/login2/")

def question_view(request):
    return render(request, 'question.html', locals())

def signup_view(request):
    return render(request, 'signup.html', locals())
def signup2_view(request):
    return render(request, 'signup2.html', locals())
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login2/')

#註冊
def signup(request):
    if(request.POST.get('upwd')!=request.POST.get('upwd2')):
        messages.error(request, '密碼輸入不一致，請重新輸入')  
        return render(request, 'signup.html',locals())
    phone_number = request.POST.get('uphone')
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

@csrf_exempt
def signup2(request):
    if request.user.is_authenticated:
        user_phone = request.user
        user = client.objects.get(PHONE_NUMBER = user_phone)
        user_name = request.POST.get('uname')
        client.objects.filter(PHONE_NUMBER = user_phone).update(NAME = user_name)
        return HttpResponseRedirect('/index/')
    else:
        messages.error(request, '您尚未登入，請先登入')
        return HttpResponseRedirect("/login2/")



def login2(request,uid,access_code):
    if request.user.is_authenticated:
        print("is auth")
        return HttpResponseRedirect('/index/')
    userphone=uid
    # requests.post('對方的api', data = {
    #     "phone": "userphone",
    # })
    count = client.objects.filter(PHONE_NUMBER = userphone).count()
    if count==0:
        codenum=""
        for i in range(10):
            codenum+=str(random.randint(0,9))
        my_code = EAN13(codenum.zfill(13), writer=ImageWriter())#code編碼要改
        client.objects.create(PHONE_NUMBER = userphone, PASSWORD='123', POINT=0,PHOTO = my_code.save("static/barcode/" + userphone),AC_CODE=access_code,TANPI=0)
        User.objects.create_user(username = userphone, password = '123') # 驗證的資料庫
        password = 123#(所有人都一樣)
        user = auth.authenticate(username = userphone, password = password)
        if user is not None and user.is_active:
            print(user)
            print('user.is_active')
            auth.login(request, user)
            return render(request, 'signup2.html', locals())
        else:
            print(user)
            print('user.n_active')
            return render(request, 'login2.html', locals())
            # 到新的註冊頁面註冊(密碼資料表欄位強制設為123)，輸入暱稱後直接登入
    
    # uid存在的話就直接登入就好
    password = 123#大家都一樣
    user = auth.authenticate(username = userphone, password = password)
    if user is not None and user.is_active:
        print(user)
        print('user.is_active')
        client.objects.filter(PHONE_NUMBER = userphone).update(AC_CODE = access_code)
        auth.login(request, user)
        return HttpResponseRedirect('/index/')
    else:
        print(user)
        print('user.n_active')
        return render(request, 'login2.html', locals())

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
def login_session(request):
    SA_CC_ID = request.GET.get('SA_CC_ID')
    if 'UserID' in request.session:
        try:
            del request.session['UserID']
        except:
            pass
    request.session['UserID'] = SA_CC_ID
    request.session.modified = True
    request.session.set_expiry(60*20) #存在20分鐘
    return HttpResponseRedirect('inside.html')
