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
            for sn, l, t, pk in value['object'].objects.values_list('short_name', 'link', 'Type', 'pk'):
                if not l:
                    continue
                if sn.upper() == search.upper():
                    results.append([value['object'], sn, t, pk])
        elif value['type'] == 'cmdty':
            for sn, l, t, pk in value['object'].objects.values_list('short_name', 'link', 'Type', 'pk'):
                if sn.upper() == search.upper():
                    results.append([value['object'], l, t, pk])
        else:
            for sn, l, t, pk in value['object'].objects.values_list('short_name', 'link', 'Type', 'pk'):
                if sn.upper() == search.upper():
                    results.append([value['object'], l, t, pk])
    
    for value in STATIC_OBJECTS.values():
        if value['type'] == 'crptcrncy':
            for sn, l, t, pk in value['object'].objects.values_list('short_name', 'link', 'Type', 'pk'):
                if not l:
                    continue
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
    for model in AllAssetsLive.objects.filter(link=asset.link):
        if type_ == 'crptcrncy' and not asset.link:
            continue
        dct = model_to_dict(model)
        for key, value in dct.items():
            if key != 'id' and value:
                data[key] = value
    for model in AllAssetsAfterLive.objects.filter(link=asset.link):
        if type_ == 'crptcrncy' and not asset.link:
            continue
        dct = model_to_dict(model)
        for key, value in dct.items():
            if key != 'id' and value:
                data[key] = value
    
    live_data = {}
    for key, value in data.items():
        if not key in 'Typelinktimedate':
            live_data[key] = value
    
    data_pairs = list(live_data.items())
    data_pairs_new = []
    for i1, i2 in data_pairs:
        if '_' in i1:
            i1 = i1.replace('_', ' ')
        i1 = i1.capitalize()
        # Circ supply: BTC18.25M -> Circ supply: 18.25M
        if 'supply' in i1:
            i = 0
            for char in i2:
                if char in '123456789':
                    break
                i += 1
            i2 = i2[i:]

        data_pairs_new.append([i1, i2])
    data_pairs = data_pairs_new
    data_pairs1, data_pairs2 = [], []
    for i in range(0, len(data_pairs), 2):
        data_pairs1.append(data_pairs[i])
        if i < len(data_pairs)-1:
            data_pairs2.append(data_pairs[i+1])
    
    if len(data_pairs2) < len(data_pairs1):
        data_pairs2.append(['',''])

    context = {
        'data': data,
        'asset': asset,
        'data_pairs': zip(data_pairs1, data_pairs2)
    }
    return render(request, 'main_app/asset_details.html', context)

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