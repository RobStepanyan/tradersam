import requests, datetime, pytz, time
from django.utils.timezone import make_aware
from bs4 import BeautifulSoup
from time import sleep
from .scraper_functions import *
from .scraper_data import STATIC_OBJECTS, TABLE_LINKS
from . import models


class CollectLive:

    def get_tabs(self):
        global driver
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
            link = 'https://www.investing.com' + tr.find('a')['href']
            if not link in link_list:
                continue
            tds = []
            
            if self.type_ == 'crncy:':
                for td in tr.find_all('td')[2:]:
                    tds.append(td.get_text().strip())
                print(tds)
            else:
                for td in tr.find_all('td')[2:-1]:
                    tds.append(td.get_text().strip())

            now = make_aware(datetime.datetime.now())
            is_closed = 0
            if self.type_ == 'crncy' and len(tr.find_all('td')[-1].get_text()) <=5:
                is_closed = True
            elif 'redClockIcon' in tr.find_all('td')[-1].span['class']:
                is_closed = True
            else:
                is_closed = False

            if is_closed:
                # if the market is open collect the live data
                live_data = {}
                for key, value in zip(self.live_fields, tds):
                    live_data[key] = value
                if self.type_ != 'bnd':
                    live_data['Prev. Close'] = float(live_data['Last'].replace(',','')) + float(live_data['Chg. %'][:-1]) / 100
                print(live_data)
                models.AllAssetsLive.objects.filter(link=link).delete()
                if len(live_data['Time']) <=5:
                    time = datetime.datetime.strptime(str(now.year)+str(live_data['Time']), '%Y%d/%m')
                else:
                    time = datetime.datetime.strptime(
                            datetime.datetime.today().strftime('%Y:%m:%d:')+str(live_data['Time']), '%Y:%m:%d:%H:%M:%S')
                if self.type_ == 'cmdty':
                    if live_data['Month'] in '  ':
                        live_data['Month'] = None
                    else:
                        live_data['Month'] = datetime.datetime.strptime(live_data['Month'], '%b %y')
                    models.AllAssetsLive(
                        Type=self.type_,
                        link=link,

                        prev_close=validate_price(live_data['Prev. Close']),

                        month=validate_price(live_data['Month']),
                        last_price=validate_price(live_data['Last']),
                        high=validate_price(live_data['High']),
                        low=validate_price(live_data['Low']),
                        change=validate_price(live_data['Chg.']),
                        change_perc=validate_price(live_data['Chg. %']),
                    
                        time=time
                    ).save()
                    print(f'{self.title}: Live is updated')
                elif self.type_ == 'crncy':
                    models.AllAssetsLive(
                        Type=self.type_,
                        link=link,

                        prev_close=validate_price(live_data['Prev. Close']),

                        last_price=validate_price(live_data['Last']),
                        Open=validate_price(live_data['Open']),
                        high=validate_price(live_data['High']),
                        low=validate_price(live_data['Low']),
                        change=validate_price(live_data['Chg.']),
                        change_perc=validate_price(live_data['Chg. %']),
                        time=time
                    ).save()

                elif self.type_ == 'crptcrncy':
                    models.AllAssetsLive(
                        Type=self.type_,
                        link=link,

                        prev_close=validate_price(live_data['Prev. Close']),

                        last_price=validate_price(live_data['Last']),
                        market_cap=validate_price(live_data['Market Cap']),
                        volume=validate_price(live_data['Vol.']),
                        total_vol=validate_price(live_data['Total Vol.']),
                        change_perc=validate_price(live_data['Chg. %']),
                        change_7d=validate_price(live_data['Chg (7D)'])
                    ).save()
                elif self.type_ == 'stck':
                    models.AllAssetsLive(
                        Type=self.type_,
                        link=link,

                        prev_close=validate_price(live_data['Prev. Close']),

                        last_price=validate_price(live_data['Last']),
                        high=validate_price(live_data['High']),
                        low=validate_price(live_data['Low']),
                        change=validate_price(live_data['Chg.']),
                        change_perc=validate_price(live_data['Chg. %']),
                        volume=validate_price(live_data['Vol.']),
                        time=time
                    ).save()
                elif self.type_ == 'indx':
                    models.AllAssetsLive(
                        Type=self.type_,
                        link=link,

                        prev_close=validate_price(live_data['Prev. Close']),

                        last_price=validate_price(live_data['Last']),
                        high=validate_price(live_data['High']),
                        low=validate_price(live_data['Low']),
                        change=validate_price(live_data['Chg.']),
                        change_perc=validate_price(live_data['Chg. %']),
                        time=time
                    ).save()
                elif self.type_ == 'etf':
                    models.AllAssetsLive(
                        Type=self.type_,
                        link=link,

                        prev_close=validate_price(live_data['Prev. Close']),

                        last_price=validate_price(live_data['Last']),
                        change_perc=validate_price(live_data['Chg. %']),
                        volume=validate_price(live_data['Vol.']),
                        time=time
                    ).save()
                elif self.type_ == 'bnd':
                    models.AllAssetsLive(
                        Type=self.type_,
                        link=link,

                        prev_close=validate_price(live_data['Prev. Close']),

                        Yield=validate_price(live_data['Yield']),
                        high=validate_price(live_data['High']),
                        low=validate_price(live_data['Low']),
                        change=validate_price(live_data['Chg.']),
                        change_perc=validate_price(live_data['Chg. %']),
                        time=time
                    ).save()
                elif self.type_ == 'crptcrncy':
                    models.AllAssetsLive(
                        Type=self.type_,
                        link=link,

                        prev_close=validate_price(live_data['Prev. Close']),

                        last_price=validate_price(live_data['Last']),
                        change_perc=validate_price(live_data['Chg. %']),
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
                        link=link,
                        date=now,
                        price=live_data['Last'],
                        Type=self.type_
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
                
                if (last_obj_5d_count == 0 or now.minute - last_obj_5d.date.minute>=5) and now.minute % 5 == 0:
                    # if there's no data at all or latest data is already outdated also divisible by 5
                    # send (Save) data
                    models.AllAssetsHistorical5D(
                        link=link,
                        date=now,
                        price=live_data['Last'],
                        Type=self.type_
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
            # elif 'redClockIcon' in tr[-1].span['class']:
            #     # check whether "after live data" for today is available
            #     last_obj_after_count = models.AllAssetsAfterLive.objects.filter(link=link).count()
            #     if last_obj_after_count > 0:
            #         last_obj_after = models.AllAssetsAfterLive.objects.filter(link=link).order_by('-id')[0]

            #     def collectAfterLive():
            #         header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'}
            #         request = requests.get(link, headers=header)
            #         print(f'Visited: {link}')
            #         while True:
            #             try:
            #                 soup = BeautifulSoup(request.text, 'html.parser')
            #                 one_year_rng = soup.find('span', text='52 wk Range').find_next_sibling('span').get_text()
            #                 one_year_chg = soup.find('span', text='1-Year Change').find_next_sibling('span').get_text()
            #                 months = soup.find('span', text='Months').find_next_sibling('span').get_text()
            #                 settlement_day = soup.find('span', text='Settlement Day').find_next_sibling('span').get_text()
            #                 try:
            #                     settlement_day = datetime.datetime.strptime(settlement_day, '%m/%d/%Y')
            #                 except:
            #                     settlement_day = None
            #                 last_roll_day = soup.find('span', text='Last Rollover Day').find_next_sibling('span').get_text()
            #                 try:
            #                     last_roll_day = datetime.datetime.strptime(last_roll_day, '%m/%d/%Y')
            #                 except:
            #                     last_roll_day = None
            #                 break
            #             except Exception as e:
            #                 print_exception(e)
            #                 sleep(3)

            #         models.AllAssetsAfterLive(
            #             short_name=tds[0], link=link,
            #             date=now.date(),
            #             one_year_rng=one_year_rng, one_year_chg=one_year_chg.strip(),
            #             months=months, 
            #             settlement_day=settlement_day, last_roll_day=last_roll_day,
            #             Type='cmdty'
            #         ).save()
            #         print(f'Commodities: saved AFTERLIVE for {tds[0]}')

            #     if last_obj_after_count == 0:
            #         collectAfterLive()
            #     elif (now.date() - last_obj_after.date).days >= 1:
            #         # if last after live data is outdated
            #         collectAfterLive()
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
    print('Driver is ready!')
    for _ in range(len(STATIC_OBJECTS)-1): # -1 because 1 is creted automatically
        driver.execute_script("window.open('', '_blank')")
    print(f'x{len(STATIC_OBJECTS)} blank tabs are ready!')

    # init
    start = time.time()
    instances = []
    for key, value in STATIC_OBJECTS.items():
        instances.append(CollectLive(key=key, value=value))
    print(f'Init took {time.time()-start} seconds')

    # launch live
    while True:    
        start = time.time()
        for instance in instances:
            instance.live_on()
        print(f'Loop took {time.time()-start} seconds')

finally:
    driver.quit()
    print('Driver is closed!')
        

            
