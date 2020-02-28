import requests, datetime, pytz, time, weakref
from django.utils.timezone import make_aware
from bs4 import BeautifulSoup
from time import sleep
from .scraper_functions import *
from .scraper_data import STATIC_OBJECTS, TABLE_LINKS
from . import models


class CollectLive:
    instances = []

    def get_tabs(self):
        global driver
        tabs = driver.window_handles[::-1]
        return tabs

    def __init__(self, key, value):
        self.__class__.instances.append(weakref.proxy(self))
        self.title = key
        self.object_ = value['object']
        self.type_ = value['type']
        self.link = value['link']
        self.table_class = value['table class']
        self.before_fields = value['before live fields']
        self.live_fields = value['live fields']
        self.after_fields = value['after live fields']
        self.no = list(STATIC_OBJECTS.keys()).index(self.title)
        tabs = CollectLive.get_tabs(self)
        self.tab = tabs[self.no]
        CollectLive.init_tab(self)

    def init_tab(self):
        driver.switch_to.window(self.tab)
        print(f'{self.title}: Initializating the Table')
        print(f'{self.title}: Waiting the page to load')
        driver.get(self.link) # visit the link
        if 'Stock' in self.title:
            print('Executing JS scripts')
            driver.execute_script('$("#stocksFilter").val("#all");')
            driver.execute_script("doStocksFilter('select',this)")
            print('Executed JS scripts')
        if 'Crypto' in self.title:
            desired_quanity = BeautifulSoup(driver.page_source, 'html.parser')
            desired_quanity = desired_quanity.find('span', text='Number of Currencies')
            desired_quanity = int(desired_quanity.find_next_sibling().get_text().replace(',', ''))
        else:
            desired_quanity = self.object_.objects.count()
        while True:
            try:
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                table = soup.find('table', class_=self.table_class)
                if len(table.find_all('tr')) < desired_quanity:
                    print(f'{self.title}: Waiting more...')
                    sleep(1)
                    continue
                break
            except AttributeError:
                sleep(1)

        print(f'{self.title}: Tab is initializated!')
    

        
# from scraper_app import live_scraper
# Logic of current module
# 1. init selenium tabs
# 2. loop and collect live data
# 3. Check condition
# 4. Call appropriate function
# 5. Repeat

#  Create driver and tabs
driver = vps_selenium_setup()
print('Driver is ready!')
for _ in range(len(STATIC_OBJECTS)-1): # -1 because 1 is creted automatically
    driver.execute_script("window.open('', '_blank')")
print(f'x{len(STATIC_OBJECTS)} blank tabs are ready!')

# Main program
try:
    for key, value in STATIC_OBJECTS.items():
        CollectLive(key=key, value=value)
finally:
    # for instance in CollectLive.instances:
    #     del instance
    # print('Instances are removed!')
    driver.quit()
    print('Driver is closed!')









#             print('Commodities: waiting...')
#             soup = BeautifulSoup(driver.page_source, 'html.parser')
#             table = soup.find('table', class_='genTbl closedTbl crossRatesTbl').tbody
#             print(f'Commodities: table is updated ({datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")})')
#             for tr in table.find_all('tr'):
#                 tds = []
#                 for td in tr.find_all('td')[1:-1]:
#                     tds.append(td.get_text())
#                 if not tds[0] in c_list:
#                     print(f'SKIPED ROW: {tds[0]}')
#                     continue # skip row 
#                 link = 'https://www.investing.com' + tr.find_all('td')[1].a['href']
#                 time_icon = tr.find_all('td')[-1].span['class'][0]
#                 now = make_aware(datetime.datetime.now())
#                 if time_icon == 'greenClockIcon':
#                     month = tds[1].strip()
#                     # Update Live Data
#                     if month in '  ':
#                         month = None
#                     else:
#                         month = datetime.datetime.strptime(month, '%b %y')

#                     AllAssetsLive.objects.filter(link=link).delete()
#                     AllAssetsLive(
#                         short_name=tds[0], link=link, 
#                         month=month,
#                         last_price=tds[2], last_price_time=tds[7],
#                         high=tds[3], low=tds[4],
#                         change=tds[5], change_perc=[tds[6]],
#                         Type='cmdty'
#                     ).save()
#                     print('Commodities: saved LIVE')

#                     def collectBeforeLive():
#                         header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'}
#                         request = requests.get(link, headers=header)
#                         print(link)
#                         while True:
#                             try:
#                                 soup = BeautifulSoup(request.text, 'html.parser')
#                                 prev_close = soup.find('span', text='Prev. Close:').find_next_sibling('span').get_text()
#                                 Open = soup.find('span', text='Open:').find_next_sibling('span').get_text()
#                                 break
#                             except Exception as e:
#                                 print_exception(e)
#                                 sleep(3)
                        
#                         AllAssetsBeforeLive(
#                             short_name=tds[0], link=link,
#                             date=now.date(),
#                             prev_close=prev_close, Open=Open,
#                             Type='cmdty'
#                         ).save()
#                         print('Commodities: saved BEFORELIVE')

#                     last_obj_before_count = AllAssetsBeforeLive.objects.filter(link=link).count()
#                     if last_obj_before_count > 0:
#                         last_obj_before = AllAssetsBeforeLive.objects.filter(link=link).order_by('-id')[0]
                    
#                     if last_obj_before_count == 0:
#                         collectBeforeLive()
#                     elif (now.date() - last_obj_before.date).days >= 1:
#                         collectBeforeLive()
                
#                     # Send data to AllAssetsHistorical1D once a minute, ...Historical5D once 5 minutes
#                     last_obj_1d_count = AllAssetsHistorical1D.objects.filter(link=link).count()
#                     if last_obj_1d_count > 0:
#                         last_obj_1d = AllAssetsHistorical1D.objects.filter(link=link).order_by('-id')[0]
                    
#                     last_obj_5d_count = AllAssetsHistorical5D.objects.filter(link=link).count()
#                     if last_obj_5d_count > 0:
#                         last_obj_5d = AllAssetsHistorical5D.objects.filter(link=link).order_by('-id')[0]
                    
#                     if last_obj_1d_count == 0 or last_obj_1d.date.minute<now.minute:
#                         # if there's no data at all or latest data is already outdated
#                         # send (Save) data
#                         AllAssetsHistorical1D(
#                             short_name=tds[0], link=link,
#                             date=now,
#                             price=tds[2],
#                             Type='cmdty'
#                         ).save()
#                         print('Commodities: saved HISTORICAL1D')

#                         if last_obj_1d_count:
#                             data1 = last_obj_1d.date
#                             data2 = now
#                             diff = data2 - data1
#                             days, seconds = diff.days, diff.seconds
#                             hours = days * 24 + seconds // 3600
#                             if hours > 24:
#                                 AllAssetsHistorical1D.objects.filter(link=link).order_by('id')[0].delete()
#                     if (last_obj_5d_count == 0 or now.minute - last_obj_5d.date.minute>=5) and now.minute % 5 == 0:
#                         # if there's no data at all or latest data is already outdated also divisible by 5
#                         # send (Save) data
#                         AllAssetsHistorical5D(
#                             short_name=tds[0], link=link,
#                             date=now,
#                             price=tds[2],
#                             Type='cmdty'
#                         ).save()
#                         print('Commodities: saved HISTORICAL5D')
                        
#                         if last_obj_5d_count:
#                             data1 = last_obj_5d.date
#                             data2 = now
#                             diff = data2 - data1
#                             days, seconds = diff.days, diff.seconds
#                             hours = days * 24 + seconds // 3600
#                             if hours > 24*5:
#                                 AllAssetsHistorical5D.objects.filter(link=link).order_by('id')[0].delete()
#                 elif time_icon == 'redClockIcon':
#                     # check whether "after live data" for today is available
#                     last_obj_after_count = AllAssetsAfterLive.objects.filter(link=link).count()
#                     if last_obj_after_count > 0:
#                         last_obj_after = AllAssetsAfterLive.objects.filter(link=link).order_by('-id')[0]

#                     def collectAfterLive():
#                         header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'}
#                         request = requests.get(link, headers=header)
#                         print(f'Visited: {link}')
#                         while True:
#                             try:
#                                 soup = BeautifulSoup(request.text, 'html.parser')
#                                 one_year_rng = soup.find('span', text='52 wk Range').find_next_sibling('span').get_text()
#                                 one_year_chg = soup.find('span', text='1-Year Change').find_next_sibling('span').get_text()
#                                 months = soup.find('span', text='Months').find_next_sibling('span').get_text()
#                                 settlement_day = soup.find('span', text='Settlement Day').find_next_sibling('span').get_text()
#                                 try:
#                                     settlement_day = datetime.datetime.strptime(settlement_day, '%m/%d/%Y')
#                                 except:
#                                     settlement_day = None
#                                 last_roll_day = soup.find('span', text='Last Rollover Day').find_next_sibling('span').get_text()
#                                 try:
#                                     last_roll_day = datetime.datetime.strptime(last_roll_day, '%m/%d/%Y')
#                                 except:
#                                     last_roll_day = None
#                                 break
#                             except Exception as e:
#                                 print_exception(e)
#                                 sleep(3)

#                         AllAssetsAfterLive(
#                             short_name=tds[0], link=link,
#                             date=now.date(),
#                             one_year_rng=one_year_rng, one_year_chg=one_year_chg.strip(),
#                             months=months, 
#                             settlement_day=settlement_day, last_roll_day=last_roll_day,
#                             Type='cmdty'
#                         ).save()
#                         print(f'Commodities: saved AFTERLIVE for {tds[0]}')

#                     if last_obj_after_count == 0:
#                         collectAfterLive()
#                     elif (now.date() - last_obj_after.date).days >= 1:
#                         # if last after live data is outdated
#                         collectAfterLive()
#                 else:
#                     print('Time Icon is not found/recognized')
#     finally:
#         driver.quit()
        

            
