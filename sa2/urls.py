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
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main),
    path('index/', views.index_view),
    path('orthers_app/',views.apps_view),
    path('exchange/',views.exchange_view),
    path('fix/',views.fix_view),
    path('history/',views.history_view),
    path('login/',views.login_view),
    path('member/',views.member_view),
    path('myself/',views.myself_view),
    path('question/',views.question_view),
    path('signup/',views.signup_view),
    path('sign/', views.signup),
    path('login_process/', views.login),
    # path(r'^admin/', admin.site.urls),
    # path(r'^$', sayhello),
]