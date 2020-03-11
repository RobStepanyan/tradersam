from django.shortcuts import render
from scraper_app.models import Types
from django.http import HttpResponse, JsonResponse
from scraper_app.scraper_data import STATIC_OBJECTS

# Create your views here.
def ajax_search(request):
    search = request.GET['search']
    results = []
    for value in STATIC_OBJECTS.values():
        if value['type'] == 'crptcrncy':
            for sn, t in value['object'].objects.values_list('short_name', 'Type'):
                if sn.upper() == search.upper():
                    results.append([value['object'], sn, t])
        elif value['type'] == 'cmdty':
            for sn, l, t in value['object'].objects.values_list('short_name', 'link', 'Type'):
                print(sn, search)
                if sn.upper() == search.upper():
                    results.append([value['object'], l, t])
        else:
            for sn, l, t in value['object'].objects.values_list('short_name', 'link', 'Type'):
                print(sn, search)
                if sn.upper() == search.upper():
                    results.append([value['object'], l, t])
    
    for value in STATIC_OBJECTS.values():
        if value['type'] == 'crptcrncy':
            for sn, t in value['object'].objects.values_list('short_name', 'Type'):
                if sn.upper().find(search.upper()) == 0:
                    if not [value['object'], sn, t] in results:
                        results.append([value['object'], sn, t])
                if len(results)>=50:
                    break 
        elif value['type'] == 'cmdty':
            for sn, l, t in value['object'].objects.values_list('short_name', 'link', 'Type'):
                if sn.upper().find(search.upper()) == 0:
                    if not [value['object'], l, t] in results:
                        results.append([value['object'], l, t])
                if len(results)>=50:
                    break 
        else:
            for sn, ln, l, t in value['object'].objects.values_list('short_name', 'long_name', 'link', 'Type'):
                if sn.upper().find(search.upper()) == 0 or any([True if word.upper().find(search.upper()) == 0 else False for word in ln.split(' ')]):
                    if not [value['object'], l, t] in results:
                        results.append([value['object'], l, t])
                if len(results)>=50:
                    break 
    
    if not results:
        return JsonResponse({})

    data = {'results': []}
    for result in results:
        if result[2] == 'crptcrncy': # there are cryptos without link
            static_info = result[0].objects.filter(short_name=result[1]).first()
        else:
            static_info = result[0].objects.filter(link=result[1]).first() # .first() - in case of duplicates
        
        if static_info.Type == 'cmdty':
            long_name = static_info.short_name + ' Futures Contract'
        else:
            long_name = static_info.long_name
        
        Type = Types[Types.index(static_info.Type)+1]
        result = {
            'link': static_info.link,
            'type': Type,
            'country': static_info.country.lower(),
            'short_name': static_info.short_name,
            'long_name': long_name,
        }
        data['results'].append(result)
    return JsonResponse(data)

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