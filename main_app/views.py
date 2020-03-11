from django.shortcuts import render
from django.forms.models import model_to_dict
from scraper_app.models import Types, AllAssetsLive, AllAssetsAfterLive
from django.http import HttpResponse, JsonResponse
from scraper_app.scraper_data import STATIC_OBJECTS

# Create your views here.
def ajax_search(request):
    search = request.GET['search']
    results = []
    
    # First finding elements which are equal to search
    # for examle when you type T resut should be T - AT&T
    # insetead of random results starting with T
    for value in STATIC_OBJECTS.values():
        if value['type'] == 'crptcrncy':
            for sn, t, pk in value['object'].objects.values_list('short_name', 'Type', 'pk'):
                if sn.upper() == search.upper():
                    results.append([value['object'], sn, t, pk])
        elif value['type'] == 'cmdty':
            for sn, l, t, pk in value['object'].objects.values_list('short_name', 'link', 'Type', 'pk'):
                print(sn, search)
                if sn.upper() == search.upper():
                    results.append([value['object'], l, t, pk])
        else:
            for sn, l, t, pk in value['object'].objects.values_list('short_name', 'link', 'Type', 'pk'):
                print(sn, search)
                if sn.upper() == search.upper():
                    results.append([value['object'], l, t, pk])
    
    for value in STATIC_OBJECTS.values():
        if value['type'] == 'crptcrncy':
            for sn, t, pk in value['object'].objects.values_list('short_name', 'Type', 'pk'):
                if sn.upper().find(search.upper()) == 0:
                    if not [value['object'], sn, t, pk] in results:
                        results.append([value['object'], sn, t, pk])
                if len(results)>=50:
                    break 
        elif value['type'] == 'cmdty':
            for sn, l, t, pk in value['object'].objects.values_list('short_name', 'link', 'Type', 'pk'):
                if sn.upper().find(search.upper()) == 0:
                    if not [value['object'], l, t, pk] in results:
                        results.append([value['object'], l, t, pk])
                if len(results)>=50:
                    break 
        else:
            for sn, ln, l, t, pk in value['object'].objects.values_list('short_name', 'long_name', 'link', 'Type', 'pk'):
                if sn.upper().find(search.upper()) == 0 or any([True if word.upper().find(search.upper()) == 0 else False for word in ln.split(' ')]):
                    if not [value['object'], l, t, pk] in results:
                        results.append([value['object'], l, t, pk])
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
            'pk': result[-1],
        }
        data['results'].append(result)
    return JsonResponse(data)

def asset_details(request, type_, pk):
    type_ = Types[Types.index(type_.capitalize())-1]
    for value in STATIC_OBJECTS.values():
        if value['type'] == type_:
            obj = value['object']
            break
    asset = obj.objects.get(pk=pk)
    data = {}
    if type_ == 'crptcrncy':
        for model in AllAssetsLive.objects.filter(type_='crptcrncy', short_name=asset.short_name):
            dct = model_to_dict(model)
            for key, value in dct.items():
                if key != 'id' and value:
                    data[key] = value
        for model in AllAssetsAfterLive.objects.filter(type_='crptcrncy', short_name=asset.short_name):
            dct = model_to_dict(model)
            for key, value in dct.items():
                if key != 'id' and value:
                    data[key] = value
    else:
        for model in AllAssetsLive.objects.filter(link=asset.link):
            dct = model_to_dict(model)
            for key, value in dct.items():
                if key != 'id' and value:
                    data[key] = value
        for model in AllAssetsAfterLive.objects.filter(link=asset.link):
            dct = model_to_dict(model)
            for key, value in dct.items():
                if key != 'id' and value:
                    data[key] = value

    return JsonResponse(data)
    # return render(request, 'main_app/asset_details.html')

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