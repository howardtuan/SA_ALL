"""sa2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from myapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main),
    path('index/', views.index_view),
    path('orthers_app/', views.apps_view),
    path('exchange/', views.exchange_view),
    path('exchange_proccess/', views.exchange),
    path('fix/', views.fix_view),
    path('fix_proccess/', views.fix),
    path('fix2/', views.fix2_view),
    path('fix_proccess2/', views.fix2),
    path('history/', views.history_view),
    path('history_otherAPP/', views.history_otherAPP_view),
    path('login/', views.login_view),
    path('login2/', views.login2_view),
    path('member/', views.member_view),
    path('myself/', views.myself_view),
    path("tickets/", views.tickets_view),
    path('use_ticket/', views.use_ticket),
    path('drive/', views.drive),
    path('drive_over/', views.drive_over),
    path('question/', views.question_view),
    path('signup/', views.signup_view),
    path('signup2/', views.signup2_view),
    path('sign/', views.signup),
    path('sign2/', views.signup2),
    path('login_process/', views.login),
    path('login_process2/', views.login2),
    path("logout/", views.logout),
    path("SA_ALL/news/", include("news.urls")),
    path("api2/",views.api2),
    path('passbook/', views.passbook_view)
    # path(r'^admin/', admin.site.urls),
    # path(r'^$', sayhello),
]