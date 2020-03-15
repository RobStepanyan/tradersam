from django.shortcuts import render
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.forms.models import model_to_dict
from scraper_app.models import Types, AllAssetsLive, AllAssetsAfterLive
from scraper_app import models
from django.http import HttpResponse, JsonResponse, Http404
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

def ajax_hist(request):
    time_frame = request.GET.get('time_frame', '1D')
    chart_type = request.GET.get('chart_type', False)

    # finding type and primary key(pk)
    link = request.GET['link'][::-1]
    pk = link[1:link[1:].index('/')+1][::-1]
    link = link[::-1]
    type_ = link[:link.index(pk)][::-1]
    type_ = type_[1:type_[1:].index('/')+1][::-1].capitalize()

    type_ = Types[Types.index(type_.capitalize())-1]
    for value in STATIC_OBJECTS.values():
        if value['type'] == type_:
            obj = value['object']
            break
    asset = obj.objects.get(pk=pk)

    hist_objects = {
    '1D': models.AllAssetsHistorical1D, '5D': models.AllAssetsHistorical5D,
    '1M': models.AllAssetsHistorical6M1M, '3M': models.AllAssetsHistorical6M1M, '6M': models.AllAssetsHistorical6M1M, 
    '1Y': models.AllAssetsHistorical1Y, '5Y': models.AllAssetsHistorical5Y, 'Max': models.AllAssetsHistoricalMax}

    # finding timeframe
    hist_data = []
    for model in hist_objects[time_frame].objects.filter(link=asset.link):
        if time_frame[-1] == 'M':
            months = int(time_frame[0])
            today = timezone.now()
            last_date = today - relativedelta(months=months)
            dct = model_to_dict(model)
            for v in dct.values():
                # for example if 1M is selected than any
                # data older is removed
                if v['date'] > last_date:
                    del dct[time_frame]
        else:
            dct = model_to_dict(model)
            hist_data.append(dct)
    
    # { time: '2018-10-25', value: 56.43 } - example of line chart price data
    # { time: '2018-10-19', open: 54.62, high: 55.50, low: 54.52, close: 54.90 } - line, candles
    # { time: '2018-10-19', value: 19103293.00, color: 'rgba(0, 150, 136, 0.8)' } - volume
    # preparing data
    hist_data_new = []
    volume_data = []
    last_volume = None
    for data in hist_data:
        # data['time'] = data['date'].strftime('%Y-%m-%d')
        data['time'] = int(data['date'].timestamp())
        volume = data['volume']
        if volume:
            if '$' in volume:
                volume = volume.replace('$', '')
            if 'B' in volume:
                volume = int(volume[:-1].replace('.', ''))* 10000000
            elif 'M' in volume:
                volume = int(volume[:-1].replace('.', ''))* 10000
            elif 'K' in volume:
                volume = int(volume[:-1].replace('.', ''))* 10
            if ',' in volume:
                volume = volume.replace(',', '')

            if not last_volume or data['volume'] > volume:
                color = 'rgba(0, 150, 136, 0.8)'
            else:
                color = 'rgba(255,82,82, 0.8)'
            volume_data.append({'time': data['time'], 'value': volume, 'color': color})
            last_volume = volume

        del data['date']
        
        if chart_type == 'line':
            data['value'] = data['price']
            data_copy = dict(data)
            for key in data_copy.keys():
                if not key in ['time', 'value']:
                    del data[key]
        
        elif chart_type == 'candle':
            data['close'] = data['price']
            data['open'] = data['Open']
            data_copy = dict(data)
            for key in data_copy.keys():
                if not key in ['open','high','low','close','time']:
                    del data[key]
        
        hist_data_new.append(data)

    data = {
        'hist_data': hist_data_new,
        'vol_data': volume_data
    }    
    print(chart_type, hist_data_new)
    print(volume_data)
    return JsonResponse(data)

def asset_details(request, type_, pk):
    if not type_.title() in Types:
        raise Http404("Type not found")
        
    type_ = Types[Types.index(type_.capitalize())-1]
    for value in STATIC_OBJECTS.values():
        if value['type'] == type_:
            obj = value['object']
            break
    
    if not str(pk) in [str(x[0]) for x in obj.objects.values_list('pk')]:
        raise Http404('PK not found')

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
        i1 = i1.title()
        if 'Perc' in str(i1):
            i1 = i1.replace('Perc', '%')
        # Circ supply: BTC18.25M -> Circ supply: 18.25M
        if 'supply' in i1:
            i = 0
            for char in i2:
                if char in '123456789':
                    break
                i += 1
            i2 = i2[i:]
        if i1 == 'Rng 52 Wk':
            i1 = '52-wk Range'
        if i1 == 'Div And YielD':
            i1 = 'Div (Yield)'
        if i1 == 'One Year Chg':
            i1 = '1-Year Change'
        if i1 in 'Epsroeroa':
            i1 = i1.upper()
        if i1 == 'Pe Ratio':
            i1 = 'P/E Ratio'
        if 'Rng' in i1:
            i1 = i1.replace('Rng', 'Range')
        if i1 == 'Shrs Outstndng':
            i1 = 'Shares Outstanding'
        if 'Avg' in i1:
            i1 = i1.replace('Avg', 'Average')
        if ' Vol ' in i1:
            i1 = i1.replace('Vol', 'Volume')
        if 'Ttm' in i1:
            i1 = i1.replace('Ttm', '(TTM)')

        data_pairs_new.append([i1, i2])

    data_pairs = data_pairs_new
    data_pairs1, data_pairs2 = data_pairs[:len(data_pairs)//2+1], data_pairs[len(data_pairs)//2+1:]
    
    if len(data_pairs2) < len(data_pairs1):
        data_pairs2.append(['',''])

    context = {
        'data': data,
        'asset': asset,
        'data_pairs': zip(data_pairs1, data_pairs2),
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