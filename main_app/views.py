from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def asset_details(request):
    return render(request, 'main_app/asset_details.html')

def news_details(request):
    return render(request, 'main_app/news_details.html')

def chart(request):
    return render(request, 'main_app/chart.html')

def csoon(request):
    return render(request, 'main_app/comingsoon.html')

def home(request):
    return render(request, 'main_app/home.html')

def error400(request):
    return render(request, 'main_app/400.html')

def error403(request):
    return render(request, 'main_app/403.html')

def error404(request):
    return render(request, 'main_app/404.html')