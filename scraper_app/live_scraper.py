import requests, datetime, pytz, time
from django.utils import timezone
from bs4 import BeautifulSoup
from time import sleep
from .scraper_functions import *
from .scraper_data import STATIC_OBJECTS, TABLE_LINKS, live_fields, after_live_fields
from . import models


class CollectLive:

    def get_tabs(self):
        global driver
        global driver2
        tabs = driver.window_handles[::-1]
        return tabs

    def __init__(self, key, value):
        self.title = key
        self.object_ = value['object']
        self.type_ = value['type']
        self.link = value['link']
        self.table_class = value['table class']
        self.before_fields = value['before live fields']
        self.live_fields = value['live fields']
        self.after_fields = value['after live fields']
        self.no = list(STATIC_OBJECTS.keys()).index(self.title)
        tabs = self.__class__.get_tabs(self)
        self.tab = tabs[self.no]
        self.__class__.init_tab(self)

    def init_tab(self):
        driver.switch_to.window(self.tab)
        # print(f'{self.title}: Initializating the Table')
        print(f'{self.title}: Waiting the page to load')
        driver.get(self.link) # visit the link
        if 'Stock' in self.title:
            # print('Executing JS scripts')
            driver.execute_script('$("#stocksFilter").val("#all");')
            driver.execute_script("doStocksFilter('select',this)")
            # print('Executed JS scripts')
        if 'Crypto' in self.title:
            desired_quanity = BeautifulSoup(driver.page_source, 'html.parser')
            desired_quanity = desired_quanity.find('span', text='Number of Currencies')
            desired_quanity = int(desired_quanity.find_next_sibling().get_text().replace(',', ''))
        else:
            desired_quanity = self.object_.objects.count()
        while True:
            try:
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                table = soup.find('table', class_=self.table_class)
                len_table = int(len(table.find_all('tr'))*1.1)
                if len_table < desired_quanity:
                    print(f'{self.title}: Waiting more... {len_table}/{desired_quanity}')
                    sleep(1)
                    continue
                break
            except AttributeError:
                sleep(1)
        
        # removing unnecessary elements
        classes_to_remove = [
            'sideNotificationZone', 'breakingNews', 'floatingAlertWrapper',
            'generalOverlay js-general-overlay displayNone',
            'earAdv left js-floaty-flyer',
            'genPopup signupPromotionPopup js-promotion-popup displayNone'
        ]
        
        driver.execute_script(f"$('header').empty()")
        for cl in classes_to_remove:
            driver.execute_script(f"$('.{cl}').empty()")
        
        for el in soup.find('div', class_='wrapper').findChildren(recursive=False):
            if el.name != 'section':
                if el.has_attr('class') and len(el['class']) > 0:
                    driver.execute_script(f"$('.{el['class'][0]}').empty()")
                elif el.has_attr('id'):
                    driver.execute_script(f"$('#{el['id']}').empty()")

        print(f'{self.title}: Tab is initializated!')

    def live_on(self):
        driver.switch_to.window(self.tab)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        table = soup.find('table', class_=self.table_class)
        
        if 'Crypto' in self.title:
            desired_quanity = BeautifulSoup(driver.page_source, 'html.parser')
            desired_quanity = desired_quanity.find('span', text='Number of Currencies')
            desired_quanity = int(desired_quanity.find_next_sibling().get_text().replace(',', ''))
        else:
            desired_quanity = self.object_.objects.count()
        while True:
            try:
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                table = soup.find('table', class_=self.table_class)
                len_table = int(len(table.find_all('tr'))*1.1)
                if len_table < desired_quanity:
                    print(f'{self.title}: Waiting more... {len_table}/{desired_quanity}')
                    sleep(1)
                    continue
                break
            except AttributeError:
                sleep(1)
        
        link_list = [i[0] for i in self.object_.objects.values_list('link')]
        for tr in table.find_all('tr')[1:]:
            if tr.find('a') is None:
                continue
            link = 'https://www.investing.com' + tr.find('a')['href']
            if not link in link_list:
                continue
            tds = []
            
            if self.type_ == 'crncy':
                for td in tr.find_all('td')[2:]:
                    tds.append(td.get_text().strip())
            elif self.type_ == 'crptcrncy':
                for td in tr.find_all('td')[4:]:
                    tds.append(td.get_text().strip())
            else:
                for td in tr.find_all('td')[2:-1]:
                    tds.append(td.get_text().strip())
            
            now = timezone.now()
            is_closed = 0
            
            if self.type_ == 'crncy' and len(tr.find_all('td')[-1].get_text()) <=5:
                is_closed = True
            elif self.type_ == 'crncy':
                is_closed = False
            elif self.type_ == 'crptcrncy':
                is_closed = True
            elif 'redClockIcon' in tr.find_all('td')[-1].span['class']:
                is_closed = True
            else:
                is_closed = False

            if not is_closed:
                # if the market is open collect the live data
                live_data = {}
                l = []
                for key, value in live_fields.items():
                    l += value
                all_live_fields = list(set(l))

                for field in all_live_fields:
                    live_data[field] = None

                # Overiding neccessary fields
                for key, value in zip(self.live_fields, tds):
                    if value in '  -N/A':
                        live_data[key] = None
                    else:
                        live_data[key] = value
                
                if self.type_ != 'bnd':
                    live_data['Prev. Close'] = float(live_data['Last'].replace(',','')) + float(live_data['Chg. %'][:-1]) / 100
                
                models.AllAssetsLive.objects.filter(link=link).delete()
                if self.type_ == 'crptcrncy':
                    time = now
                elif len(live_data['Time']) <=5:
                    time = datetime.datetime.strptime(str(now.year)+str(live_data['Time']), '%Y%d/%m')
                else:
                    time = datetime.datetime.strptime(
                            timezone.now().date().strftime('%Y:%m:%d:')+str(live_data['Time']), '%Y:%m:%d:%H:%M:%S')
                    time = timezone.make_aware(time)
                if self.type_ == 'cmdty':
                    if live_data['Month'] is None:
                        pass
                    elif live_data['Month'] in '  ':
                        live_data['Month'] = None
                    else:
                        live_data['Month'] = datetime.datetime.strptime(live_data['Month'], '%b %y')
                models.AllAssetsLive(
                    Type=self.type_,
                    link=link,

                    prev_close=validate_price(live_data['Prev. Close']),

                    last_price=validate_price(live_data['Last']),
                    month=validate_price(live_data['Month']),
                    Open=validate_price(live_data['Open']),
                    high=validate_price(live_data['High']),
                    low=validate_price(live_data['Low']),
                    change=validate_price(live_data['Chg.']),
                    change_7d=validate_price(live_data['Chg. (7D)']),
                    change_perc=validate_price(live_data['Chg. %']),
                    volume=validate_price(live_data['Vol.']),
                    market_cap=validate_price(live_data['Market Cap']),
                    Yield=validate_price(live_data['Yield']),
                    total_vol=validate_price(live_data['Total Vol.']),
                    total_assets=validate_price(live_data['Total Assets']),
                
                    time=time
                ).save()

                last_obj_1d_count = models.AllAssetsHistorical1D.objects.filter(link=link).count()
                if last_obj_1d_count > 0:
                    last_obj_1d = models.AllAssetsHistorical1D.objects.filter(link=link).order_by('-id')[0]
                
                last_obj_5d_count = models.AllAssetsHistorical5D.objects.filter(link=link).count()
                if last_obj_5d_count > 0:
                    last_obj_5d = models.AllAssetsHistorical5D.objects.filter(link=link).order_by('-id')[0]
                
                if last_obj_1d_count == 0 or last_obj_1d.date.minute<now.minute:
                    # if there's no data at all or latest data is already outdated
                    # send (Save) data
                    models.AllAssetsHistorical1D(
                        Type=self.type_,
                        link=link,

                        date=now,
                        price=validate_price(live_data['Last']),
                        Open=validate_price(live_data['Open']),
                        high=validate_price(live_data['High']),
                        low=validate_price(live_data['Low']),
                        volume=validate_price(live_data['Vol.']),
                    ).save()
                    print(f'{self.title}: saved HISTORICAL1D')

                    if last_obj_1d_count:
                        data1 = last_obj_1d.date
                        data2 = now
                        diff = data2 - data1
                        days, seconds = diff.days, diff.seconds
                        hours = days * 24 + seconds // 3600
                        if hours > 24:
                            models.AllAssetsHistorical1D.objects.filter(link=link).order_by('id')[0].delete()
                
                if (last_obj_5d_count == 0 or now.minute - last_obj_5d.date.minute>=5):
                    # if there's no data at all or latest data is already outdated also divisible by 5
                    # send (Save) data
                    models.AllAssetsHistorical5D(
                        Type=self.type_,
                        link=link,

                        date=now,
                        price=validate_price(live_data['Last']),
                        Open=validate_price(live_data['Open']),
                        high=validate_price(live_data['High']),
                        low=validate_price(live_data['Low']),
                        volume=validate_price(live_data['Vol.']),
                    ).save()
                    print(f'{self.title}: saved HISTORICAL5D')
                    
                    if last_obj_5d_count:
                        data1 = last_obj_5d.date
                        data2 = now
                        diff = data2 - data1
                        days, seconds = diff.days, diff.seconds
                        hours = days * 24 + seconds // 3600
                        if hours > 24*5:
                            models.AllAssetsHistorical5D.objects.filter(link=link).order_by('id')[0].delete()
            elif is_closed:
                # check whether "after live data" for today is available
                last_obj_after_count = models.AllAssetsAfterLive.objects.filter(link=link).count()
                if last_obj_after_count > 0:
                    last_obj_after = models.AllAssetsAfterLive.objects.filter(link=link).order_by('-id')[0]

                after_values = {}
                driver2.get(link)
                soup = BeautifulSoup(driver2.page_source, 'html.parser')
                
                if self.type_ == 'crptcrncy':
                    panel = soup.find('div', class_='cryptoGlobalData')
                    panel_values = []
                    for d in panel.find_all('div', class_='dataItem'):
                        panel_values.append(d.find_all('span')[-1].get_text())

                    after_values['Circulating Supply'] = panel_values[1]
                    after_values['Max Supply'] = panel_values[2]
                    after_values['Day\'s Range'] = panel_values[4]
                else:
                    after_table = soup.find('div', class_='overviewDataTable')
                    raw_after_values = {}
                    for d in after_table.find_all('div', class_='inlineblock'):
                        raw_after_values[d.find('span').get_text()] = d.find_all('span')[-1].get_text()

                    for key, value in raw_after_values.items():
                        if key in self.after_fields:
                            after_values[key] = value

                after_live_data = {}
                l = []
                for value in after_live_fields.values():
                    l += value
                all_live_fields = list(set(l))

                for field in all_live_fields:
                    after_live_data[field] = None

                # Overiding neccessary fields
                for key, value in after_values.items():
                    if value in ' -N/A':
                        after_live_data[key] = None
                    else:
                        after_live_data[key] = value
                
                if validate_price(after_live_data['Next Earnings Date']) is None:
                    next_earn_date = None
                else:
                    next_earn_date = datetime.datetime.strptime(validate_price(after_live_data['Next Earnings Date']), '%b %d, %Y')

                if validate_price(after_live_data['Maturity Date']) is None:
                    maturity_date = None
                else:
                    maturity_date = datetime.datetime.strptime(validate_price(after_live_data['Maturity Date']), '%d %b %Y')

                if validate_price(after_live_data['Last Rollover Day']) is None:
                    last_roll_day = None
                else:
                    last_roll_day = datetime.datetime.strptime(validate_price(after_live_data['Last Rollover Day']), '%m/%d/%Y')

                if validate_price(after_live_data['Settlement Day']) is None:
                    settlement_day = None
                else:
                    settlement_day = datetime.datetime.strptime(validate_price(after_live_data['Settlement Day']), '%m/%d/%Y')

                if last_obj_after_count == 0 or ((now.date() - last_obj_after.date).days >= 1):
                    models.AllAssetsAfterLive(
                        Type=self.type_,
                        link=link,

                        date=now,

                        pe_ratio=validate_price(after_live_data['P/E Ratio']),
                        coupon=validate_price(after_live_data['Coupon']),
                        div_yield=validate_price(after_live_data['Dividend Yield']),
                        shrs_outstndng=validate_price(after_live_data['Shares Outstanding']),
                        avg_vol_3m=validate_price(after_live_data['Average Vol. (3m)']),
                        beta=validate_price(after_live_data['Beta']),
                        next_earn_date=next_earn_date,
                        max_supply=validate_price(after_live_data['Max Supply']),
                        volume=validate_price(after_live_data['Volume']),
                        div_ttm=validate_price(after_live_data['Dividends (TTM)']),
                        price_rng=validate_price(after_live_data['Price Range']),
                        roe=validate_price(after_live_data['ROE']),
                        market_cap=validate_price(after_live_data['Market Cap']),
                        rating=validate_price(after_live_data['Rating']),
                        maturity_date=maturity_date,
                        total_assets=validate_price(after_live_data['Total Assets']),
                        ttm_yield=validate_price(after_live_data['TTM Yield']),
                        rng_52_wk=validate_price(after_live_data['52 wk Range']),
                        revenue=validate_price(after_live_data['Revenue']),
                        div_and_yield=validate_price(after_live_data['Dividend (Yield)']),
                        one_year_chg=validate_price(after_live_data['1-Year Change']),
                        price_opn=validate_price(after_live_data['Price Open']),
                        roa=validate_price(after_live_data['ROA']),
                        price=validate_price(after_live_data['Price']),
                        turnover=validate_price(after_live_data['Turnover']),
                        days_rng=validate_price(after_live_data['Day\'s Range']),
                        expenses=validate_price(after_live_data['Expenses']),
                        roi_ttm=validate_price(after_live_data['ROI (TTM)']),
                        circ_supply=validate_price(after_live_data['Circulating Supply']),
                        risk_rating=validate_price(after_live_data['Rating']),
                        last_roll_day=last_roll_day,
                        months=validate_price(after_live_data['Months']),
                        settlement_day=settlement_day,
                        asset_class=validate_price(after_live_data['Asset Class']),
                        eps=validate_price(after_live_data['EPS']),
                    ).save()
                    print(f'Commodities: saved AFTERLIVE for {tr.find_all('td')[0]}')

                
            else:
                print('Time Icon is not found/recognized')

    def __repr__(self):
        return self.title

    def __str__(self):
        return self.title

    
    

        
# from scraper_app import live_scraper
# Logic of current module
# 1. init selenium tabs
# 2. loop and collect live data
# 3. Check condition
# 4. Call appropriate function
# 5. Repeat

try:
    #  Create driver and tabs
    driver = vps_selenium_setup()
    driver2 = vps_selenium_setup()
    print('Driver is ready!')
    for _ in range(len(STATIC_OBJECTS)-1): # -1 because 1 is creted automatically
        driver.execute_script("window.open('', '_blank')")
    print(f'x{len(STATIC_OBJECTS)} blank tabs are ready!')

    # init
    results = []
    start = time.time()
    instances = []
    for key, value in STATIC_OBJECTS.items():
        instances.append(CollectLive(key=key, value=value))
    results.append(round(time.time()-start, 2))

    # # launch live
    while True:    
        start = time.time()
        for instance in instances:
            instance.live_on()
        results.append(round(time.time()-start, 2))

finally:
    driver.quit()
    driver2.quit()
    print('Driver is closed!')
    print(f'Init took: {results[0]} seconds')
    if len(results[1:]) == 1:
        print(f'Average loop took: {results[1:]} seconds') 
    else:
        print(f'Average loop took: {sum(results[1:])/len(results[1:])} seconds')        

            
