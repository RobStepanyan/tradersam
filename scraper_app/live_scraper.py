import requests, datetime, pytz, time
from django.utils import timezone
from bs4 import BeautifulSoup
from time import sleep
from .scraper_functions import *
from .scraper_data import STATIC_OBJECTS, TABLE_LINKS, live_fields, after_live_fields
from . import models


class CollectLive:
    # this function is also used to fetch global variables to the class
    def get_tabs(self):
        global driver
        global driver2
        global after_live_threads
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
        print(f'{self.title}: Waiting the page to load')
        driver.get(self.link) # visit the link
        if 'Stock' in self.title:
            driver.execute_script('$("#stocksFilter").val("#all");')
            driver.execute_script("doStocksFilter('select',this)")
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
            # for skipping TimeoutException: Message: script timeout
            try:
                driver.execute_script(f"$('.{cl}').empty()")
            except:
                pass
        
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
            elif self.type_ == 'etf' or self.type_ == 'fnd':
                for td in tr.find_all('td')[3:-1]:
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
                is_closed = False
            elif 'redClockIcon' in tr.find_all('td')[-1].span['class'][0]:
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
                
                if not self.type_ in ['bnd', 'crptcrncy']:
                    try:
                        live_data['Prev. Close'] = round(float(live_data['Last'].replace(',','')) + float(live_data['Chg.']), 2)
                    except:
                        pass
                models.AllAssetsLive.objects.filter(link=link).delete()
                try:
                    if self.type_ == 'crptcrncy':
                        time = now
                    elif len(live_data['Time']) <=5:
                        time = datetime.datetime.strptime(str(now.year)+str(live_data['Time']), '%Y%d/%m')
                    else:
                        time = datetime.datetime.strptime(
                                timezone.now().date().strftime('%Y:%m:%d:')+str(live_data['Time']), '%Y:%m:%d:%H:%M:%S')
                        time = timezone.make_aware(time)
                except:
                    time = None
                try:
                    if self.type_ == 'cmdty':
                        if live_data['Month'] is None:
                            pass
                        elif live_data['Month'] in '  ':
                            live_data['Month'] = None
                        else:
                            live_data['Month'] = datetime.datetime.strptime(live_data['Month'], '%b %y')
                except:
                    live_data['Month'] = None
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
                print(f'{self.title}: saved Live')

                last_obj_count = {}
                last_obj = {}
                hist_objects = {
                '1D': models.AllAssetsHistorical1D, '5D': models.AllAssetsHistorical5D, '6M1M': models.AllAssetsHistorical6M1M, 
                '1Y': models.AllAssetsHistorical1Y, '5Y': models.AllAssetsHistorical5Y, 'Max': models.AllAssetsHistoricalMax
                }
                hours_ = {
                    '1D': 24, '5D': 24*5, '6M1M': 24*30, 
                    '1Y': 24*365, '5Y': 24*365*5
                }
                minutes_ = {
                    '1D': 1, '5D': 5, '6M1M': 1, 
                    '1Y': 1, '5Y': 5, 'Max':30 # minutes of every element except 1D 5D are used as hours
                }
                for k, v in hist_objects.items():
                    last_obj_count[k] = v.objects.filter(link=link).count()
                    if last_obj_count[k] > 0:
                        last_obj[k] = v.objects.filter(link=link).order_by('-id').first()

                for time_frame, hist_model in hist_objects.items():
                    if time_frame[-1] == 'D':
                        if last_obj_count[time_frame] == 0 or now.minute - last_obj[time_frame].date.minute >= minutes_[time_frame]:
                            # if there's no data at all or latest data is already outdated
                            # send (Save) data
                            hist_model(
                            Type=self.type_,
                                link=link,

                                date=now,
                                price=validate_price(live_data['Last']),
                                Open=validate_price(live_data['Open']),
                                high=validate_price(live_data['High']),
                                low=validate_price(live_data['Low']),
                                volume=validate_price(live_data['Vol.']),
                            ).save() 
                            print(f'{self.title}: saved HISTORICAL{time_frame}')
                    else:
                        if last_obj_count[time_frame] == 0 or now.day - last_obj[time_frame].date.day >= minutes_[time_frame]:
                            # if there's no data at all or latest data is already outdated
                            # send (Save) data
                            hist_model(
                            Type=self.type_,
                                link=link,

                                date=now,
                                price=validate_price(live_data['Last']),
                                Open=validate_price(live_data['Open']),
                                high=validate_price(live_data['High']),
                                low=validate_price(live_data['Low']),
                                volume=validate_price(live_data['Vol.']),
                            ).save() 
                            print(f'{self.title}: saved HISTORICAL{time_frame}')

                    if time_frame != 'Max':
                        if last_obj_count[time_frame]:
                            data1 = last_obj[time_frame].date
                            if time_frame[-1] == 'D': 
                                data2 = now
                            else:
                                data2 = now.date()
                            diff = data2 - data1
                            days, seconds = diff.days, diff.seconds
                            hours = days * 24 + seconds // 3600
                            if hours > hours_[time_frame]:
                                hist_model.objects.filter(link=link).order_by('id')[0].delete()

            elif is_closed:
                # check whether "after live data" for today is available
                last_obj_after_count = models.AllAssetsAfterLive.objects.filter(link=link).count()
                if last_obj_after_count > 0:
                    last_obj_after = models.AllAssetsAfterLive.objects.filter(link=link).order_by('-id')[0]

                if last_obj_after_count == 0 or ((now.date() - last_obj_after.date).days >= 1):
                    after_live_threads.append(
                        {'link': link, 'type': self.type_, 'after fields': self.after_fields,'title': self.title}
                        )
            else:
                print('Time Icon is not found/recognized')

    def __repr__(self):
        return self.title

    def __str__(self):
        return self.title

def run_after_live(link, type_, after_fields, title):
    after_values = {}
    driver2.get(link)
    now = timezone.now()
    soup = BeautifulSoup(driver2.page_source, 'html.parser')
    
    if type_ == 'crptcrncy':
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
            if key in after_fields:
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
    
    if after_live_data['Next Earnings Date']: # if not None
        next_earn_date = datetime.datetime.strptime(after_live_data['Next Earnings Date'], '%b %d, %Y')
    else:
        next_earn_date = None

    if after_live_data['Maturity Date']: # if not None
        maturity_date = datetime.datetime.strptime(after_live_data['Maturity Date'], '%d %b %Y')
    else:
        maturity_date = None

    if after_live_data['Last Rollover Day']: # if not None
        last_roll_day = datetime.datetime.strptime(after_live_data['Last Rollover Day'], '%m/%d/%Y')
    else:
        last_roll_day = None

    if after_live_data['Settlement Day']: # if not None
        settlement_day = datetime.datetime.strptime(after_live_data['Settlement Day'], '%m/%d/%Y')
    else:
        settlement_day = None

    
    models.AllAssetsAfterLive(
        Type=type_,
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
    
    print(f'{title}: saved AFTERLIVE')
    global after_live_thread_alive
    after_live_thread_alive = False
    

        
# from scraper_app import live_scraper
# Logic of current module
# 1. init selenium tabs
# 2. loop and collect live data
# 3. Check condition
# 4. Call appropriate function
# 5. Repeat
def run_after_live_thread():
    global after_live_thread_alive, after_live_threads

    if not after_live_thread_alive and after_live_threads:
        after_live_thread_alive = True
        args = after_live_threads.pop()
        Thread(target=run_after_live, 
        args=(args['link'], args['type'], args['after fields'], args['title'])).start()

try:
    after_live_threads = []
    after_live_thread_alive = False
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
    print('Init finished')

    Thread(target=run_after_live_thread).start()
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
    if len(results[1:]) != 0:
        print(f'Average loop took: {sum(results[1:])/len(results[1:])} seconds')        

            
