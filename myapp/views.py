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