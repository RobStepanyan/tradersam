from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def asset_details(request):
    return render(request, 'main_app/asset_details.html')

def news_details(request):
    return render(request, 'main_app/news_details.html')

def all_assets(request, cntry, type_):
    context = {
        'country': cntry,
        'type': type_
    }
    return render(request, 'main_app/all_assets.html', context)

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