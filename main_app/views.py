import datetime
from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.forms.models import model_to_dict
from scraper_app.models import Types, Types_plural, Countries, AllAssetsLive, AllAssetsAfterLive
from scraper_app import models
from django.http import HttpResponse, JsonResponse, Http404
from scraper_app.scraper_data import STATIC_OBJECTS

# Create your views here.
def ajax_search(request):
    search = request.GET['search'].strip()
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
    time_frame = request.GET.get('time_frame')
    chart_type = request.GET.get('chart_type')
    
    # finding type and primary key(pk)
    link = request.GET['link'][::-1]
    pk = link[1:link[1:].index('/')+1][::-1]
    link = link[::-1]
    type_ = link[:link.index(pk)][::-1]
    type_ = type_[1:type_[1:].index('/')+1][::-1].capitalize()
    cntry = link[:link.index(type_.lower())][::-1]
    cntry = cntry[1:cntry[1:].index('/')+1][::-1]
    
    cntry = cntry.upper()
    cntry1 = Countries[Countries.index(cntry)+1]
    country = (cntry, cntry1)
    
    if type_.lower() != 'etf':
        type_ = Types[[x.lower() for x in Types].index(type_.lower())-1]
    
    for key, value in STATIC_OBJECTS.items():
        if type_.lower() == 'cmdty':
            obj = STATIC_OBJECTS['Commodities']['object']
            break
        elif cntry == 'G':
            if value['type'].lower() == type_.lower():
                obj = value['object']
                break
        else:    
            if value['type'].lower() == type_.lower() and (country[0] in key):
                obj = value['object']
                break

    asset = obj.objects.get(pk=pk)
    hist_objects = {
    '1D': models.AllAssetsHistorical1D, '5D': models.AllAssetsHistorical5D,
    '1M': models.AllAssetsHistorical6M1M, '3M': models.AllAssetsHistorical6M1M, '6M': models.AllAssetsHistorical6M1M, 
    '1Y': models.AllAssetsHistorical1Y, '5Y': models.AllAssetsHistorical5Y, 'Max': models.AllAssetsHistoricalMax}
    
    # finding timeframe
    hist_data = []
    if time_frame[-1] == 'D':
        filter_ = hist_objects[time_frame].objects.filter(link=asset.link)
    else:
        filter_ = hist_objects[time_frame].objects.filter(Type=asset.Type, short_name=asset.short_name)
    
    for model in filter_:
        if not asset.link in model.link:
            continue
        if time_frame[-1] == 'M':
            months = int(time_frame[0])
            today = timezone.now()
            last_date = today - relativedelta(months=months)
            dct = model_to_dict(model)
            # for example if 1M is selected than any
            # data older is removed
            if dct['date'] < last_date.date() or dct['date'] is None:
                continue
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
        if time_frame[-1] == 'D':
            data['time'] = int(data['date'].timestamp())
        else:
            data['time'] = data['date'].strftime('%Y-%m-%d')
        
        volume = data['volume']
        if volume:
            # volume example - 457.67K
            volume_int = volume
            if '$' in volume_int:
                volume_int = volume_int.replace('$', '')
            if ',' in volume_int:
                volume_int = volume_int.replace(',', '')
            if 'B' in volume_int:
                volume_int = int(volume_int[:-1].replace('.', ''))* 10000000
            elif 'M' in volume_int:
                volume_int = int(volume_int[:-1].replace('.', ''))* 10000
            elif 'K' in volume_int:
                volume_int = int(volume_int[:-1].replace('.', ''))* 10
                
            if not last_volume or volume > last_volume:
                color = 'rgba(0, 150, 136, 0.8)'
            else:
                color = 'rgba(255,82,82, 0.8)'
            volume_data.append({'time': data['time'], 'value': volume, 'color': color})
            last_volume = volume
        del data['date']
        if chart_type == 'line':
            if ',' in data['price']:
                data['price'] = data['price'].replace(',', '')
            
            data['value'] = float(data['price'])
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
            for k, v in data.items():
                if k != 'time':
                    if ',' in v:
                        v = v.replace(',','')
                    data[k] = float(v)

        hist_data_new.append(data)
    hist_data = []
    for dct in hist_data_new:
        if all(dct.values()):
            hist_data.append(dct)
    vol_data = []
    for dct in volume_data:
        if all(dct.values()):
            vol_data.append(dct)
    
    data = {
        'hist_data': hist_data,
        'vol_data': vol_data
    }    
    return JsonResponse(data)

def ajax_all(request):
    expanded = True if request.GET['expanded'] == 'true' else False
    link = request.GET['link']

    # finding country and type
    link = link[::-1]
    type_ = link[1:link[1:].index('/')+1][::-1]
    link = link[::-1]
    country = link[:link.index(type_)][::-1]
    country = country[1:country[1:].index('/')+1][::-1]

    if not type_.title() in Types_plural:
        raise Http404('Type is not found')

    if not country.upper() in Countries:
        raise Http404('Country is not found')

    plural_i = [i.upper() for i in Types_plural].index(type_.upper())
    type_ = Types_plural[plural_i-1]

    for key, value in STATIC_OBJECTS.items():
        if type_ == 'cmdty':
            obj = STATIC_OBJECTS['Commodities']['object']
            fields = STATIC_OBJECTS['Commodities']['live fields']
            break
        elif country == 'G':
            if value['type'] == type_:
                obj = value['object']
                fields = value['live fields']
                break
        else:    
            if value['type'] == type_ and (country[0] in key or country[1] in key):
                obj = value['object']
                fields = value['live fields']
                break
    
    if expanded:
        objects = obj.objects.all()
    else:
        objects = obj.objects.all()[:12]
    
    data_list = []
    data = {}
    for item in objects:
        objects_dct = {}
        for model in AllAssetsLive.objects.filter(link=item.link):
            if type_ == 'crptcrncy' and not item.link:
                continue
            dct = model_to_dict(model)
            for key, value in dct.items():
                if '_' in key:
                    key = key.replace('_', ' ')
                key = key.title()
                
                if 'Perc' in key:
                    key = key.replace('Perc', '%')
                if 'Prev' in key:
                    key = key.replace('Prev', 'Prev.')
                if 'Volume' in key:
                    key = key.replace('Volume', 'Vol.')
                if 'Change' in key:
                    key = key.replace('Change', 'Chg.')
                if 'Last Price' in key:
                    key = 'Last'

                if key == 'Time':
                    value = value.strftime('%I:%M:%S')
                if key.upper() in [field.upper() for field in fields]:
                    data[key] = value
                data['Symbol'] = item.short_name

        item = model_to_dict(item)
        if item['Type'] == 'cmdty':
            item['long_name'] = item['short_name'] + ' Futures Contract'

        objects_dct['live'] = list(data.values())
        item['Type'] = Types[Types.index(item['Type'])+1].lower()
        objects_dct['static'] = item

        data_list.append(objects_dct)
    data_list = sorted(data_list, key = lambda x: x['live'][0]) # sorted by short_name
    context = {
        'data_list': data_list,
        'fields': ['Symbol'] + fields
    }
    return JsonResponse(context)

def ajax_main_table(request):
    country = request.GET.get('country', 'US')
    type_ = request.GET.get('type_', 'Indices')

    if not type_.upper() in [x.upper() for x in Types_plural]:
        raise Http404('Type is not found')

    if not country.upper() in Countries:
        raise Http404('Country is not found')

    plural_i = [i.upper() for i in Types_plural].index(type_.upper())
    type_ = Types_plural[plural_i-1]

    for key, value in STATIC_OBJECTS.items():
        if type_ == 'cmdty':
            obj = STATIC_OBJECTS['Commodities']['object']
            fields = STATIC_OBJECTS['Commodities']['live fields']
            break
        elif country == 'G':
            if value['type'] == type_:
                obj = value['object']
                fields = value['live fields']
                break
        else:    
            if value['type'] == type_ and country.lower() in key.lower():
                obj = value['object']
                fields = value['live fields']
                break
    
    objects = obj.objects.all()[:10]
    
    data_list = []
    data = {}
    for item in objects:
        objects_dct = {}
        for model in AllAssetsLive.objects.filter(link=item.link):
            if type_ == 'crptcrncy' and not item.link:
                continue
            dct = model_to_dict(model)
            for key, value in dct.items():
                if '_' in key:
                    key = key.replace('_', ' ')
                key = key.title()
                if 'Volume' in key:
                    key = key.replace('Volume', 'Vol.')
                if 'Change' in key:
                    key = key.replace('Change', 'Chg.')
                if 'Perc' in key:
                    key = key.replace('Perc', '%')
                if 'Last Price' in key:
                    key = 'Last'
                
                if key.lower() in ['short name', 'last', 'chg.', 'chg. %', 'vol.'] and key.upper() in [field.upper() for field in fields]:
                    data[key] = value
                data['Symbol'] = item.short_name

        item = model_to_dict(item)
        if item['Type'] == 'cmdty':
            item['long_name'] = item['short_name'] + ' Futures Contract'

        objects_dct['live'] = list(data.values())
        item['Type'] = Types[Types.index(item['Type'])+1].lower()
        objects_dct['static'] = item

        data_list.append(objects_dct)
    data_list = sorted(data_list, key = lambda x: x['live'][0]) # sorted by short_name
    context = {
        'data_list': data_list,
        'fields': list(data.keys())
    }
    return JsonResponse(context)

def ajax_home_carousel(request):
    country = request.GET.get('country', 'US')
    if not country.upper() in Countries:
        raise Http404('Country is not found')

    for key, value in STATIC_OBJECTS.items():
        if value['type'] == 'indx' and country in key:
            obj = value['object']
            break
    
    objects = obj.objects.all()[:15]
    
    data_list = []
    for item in objects:
        objects_dct = {}
        for model in AllAssetsLive.objects.filter(link=item.link):
            chg = model.change_perc

        item = model_to_dict(item)
        plural_i = [i.upper() for i in Types_plural].index(item['Type'].upper())
        item['Type'] = Types_plural[plural_i-1]

        objects_dct['live'] = chg
        objects_dct['static'] = item

        data_list.append(objects_dct)
    
    context = {
        'data_list': data_list,
    }
    return JsonResponse(context)

def asset_details(request, cntry, type_, pk):
    if not type_.lower() in [x.lower() for x in Types]:
        raise Http404(f"Type not found: {type_}")
    
    cntry = cntry.upper()
    if type_.lower() != 'etf':
        type_ = Types[[x.lower() for x in Types].index(type_.lower())-1]
    cntry1 = Countries[Countries.index(cntry)+1]
    country = (cntry, cntry1) # US, United States
    
    for key, value in STATIC_OBJECTS.items():
        if type_.lower() == 'cmdty':
            obj = STATIC_OBJECTS['Commodities']['object']
            break
        elif cntry == 'G':
            if value['type'].lower() == type_.lower():
                obj = value['object']
                break
        else:    
            if value['type'].lower() == type_.lower() and (country[0] in key):
                obj = value['object']
                break
    
    if not str(pk) in [str(x[0]) for x in obj.objects.values_list('pk')]:
        raise Http404('PK not found')

    asset = obj.objects.get(pk=pk)
    data_ = {}
    for model in AllAssetsLive.objects.filter(link=asset.link):
        if type_ == 'crptcrncy' and not asset.link:
            continue
        dct = model_to_dict(model)
        for key, value in dct.items():
            if key != 'id' and value:
                data_[key] = value
    for model in AllAssetsAfterLive.objects.filter(link=asset.link):
        if type_ == 'crptcrncy' and not asset.link:
            continue
        dct = model_to_dict(model)
        for key, value in dct.items():
            if key != 'id' and value:
                data_[key] = value
    
    live_data_ = {}
    for key, value in data_.items():
        if not key in 'Typelinktimedate':
            live_data_[key] = value
    
    data_pairs = list(live_data_.items())
    data_pairs_new = []
    for i1, i2 in data_pairs:
        if '_' in i1:
            i1 = i1.replace('_', ' ')
        i1 = i1.title()
        if 'Perc' in str(i1):
            i1 = i1.replace('Perc', '%')
        # Circ supply: BTC18.25M -> Circ supply: 18.25M
        if 'Supply' in i1:
            i = 0
            for char in i2:
                if char in '1234567890':
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


    # finding similar assets to display in carousel
    similars = []
    if type_ == 'crncy':
        for item in obj.objects.all():
            similars.append(item)
            if len(similars) >= 15:
                break
    else:
        similars = obj.objects.filter(short_name__startswith=asset.short_name[0])[:15]
    
    
    similars_lst = []
    data = {}
    for item in similars:
        similars_dct = {}
        for model in AllAssetsLive.objects.filter(link=item.link):
            if type_ == 'crptcrncy' and not item.link:
                continue
            dct = model_to_dict(model)
            for key, value in dct.items():
                if key != 'id' and value:
                    data[key] = value
        
        live_data = {}
        for key, value in data.items():
            if key in ['change', 'change_perc']:
                live_data[key] = value

        item = model_to_dict(item)
        if item['Type'] == 'cmdty':
            item['long_name'] = item['short_name'] + ' Futures Contract'

        item['Type'] = Types[Types.index(item['Type'])+1].lower()
        similars_dct['live'] = live_data
        similars_dct['static'] = item
        
        if len(similars_dct['static']['long_name']) > 22:
            similars_dct['static']['long_name'] = similars_dct['static']['long_name'][:20] + '..'

        similars_lst.append(similars_dct)

    context = {
        'data': data_,
        'asset': asset,
        'similars': similars_lst,
        'data_pairs': zip(data_pairs1, data_pairs2),
    }
    return render(request, 'main_app/asset_details.html', context)

def news_details(request):
    return render(request, 'main_app/news_details.html')

def all_assets(request, cntry, type_):
    country = (Countries[Countries.index(cntry.upper())], Countries[Countries.index(cntry.upper())+1]) # ('US', 'United States')
    plural_i = [i.upper() for i in Types_plural].index(type_.upper())
    type_ = (Types_plural[plural_i-1], Types_plural[plural_i]) # ('cmdty', 'Commodities)
    time = timezone.now()

    if (type_[0] in ['cmdty', 'crncy', 'crptcrncy'] and country[0] != 'G') or (not type_[0] in ['cmdty', 'crncy', 'crptcrncy'] and country[0] == 'G'):
        return redirect(reverse('all-assets', args=('us', type_[1].lower())))
    context = {
        'country': country,
        'type': type_,
        'time': time
    }
    return render(request, 'main_app/all_assets.html', context)

def csoon(request):
    return render(request, 'main_app/comingsoon.html')

def home(request):
    return render(request, 'main_app/home.html')

def error400(request):
    return render(request, '400.html')

def error403(request):
    return render(request, '403.html')

def error404(request):
    return render(request, '404.html')