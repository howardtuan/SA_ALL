from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

# Create your views here.
user_name="Howard"
user_point=3000
user_barcode="/WHAT87"
def main(request):
    return render(request, 'index.html', {
        'user_name':user_name,
        'user_point':user_point,
        'user_barcode':user_barcode,
    } )
    
def index_view(request):
    return render(request, 'index.html', {
        'user_name':user_name,
        'user_point':user_point,
        'user_barcode':user_barcode,
    } )
def apps_view(request):
    return render(request, 'orthers_app.html', {
    } )
def exchange_view(request):
    return render(request, 'exchange.html', {
    } )
def fix_view(request):
    return render(request, 'fix.html', {
    } )
def history_view(request):
    return render(request, 'history.html', {
    } )
def login_view(request):
    return render(request, 'login.html', {
    } )
def member_view(request):
    return render(request, 'member.html', {
    } )
def myself_view(request):
    return render(request, 'myself.html', {
    } )
def question_view(request):
    return render(request, 'question.html', {
    } )
def signup_view(request):
    return render(request, 'signup.html', {
    } )
