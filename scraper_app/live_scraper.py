import requests, datetime, pytz, time
from django.utils.timezone import make_aware
from bs4 import BeautifulSoup
from time import sleep
from .scraper_functions import *
from .scraper_data import STATIC_OBJECTS, TABLE_LINKS
from . import models


def init_selenium_tabs(driver, selenium_dct):
    # Opening a new driver
    def load_tab(driver, title, object_, type_, link, table_class):
        print(f'{title}: Visiting the Table')
        print(f'{title}: Waiting the page to load')
        driver.get(link) # visit the link
        if 'Stock' in title:
            print('Executing JS scripts')
            driver.execute_script('$("#stocksFilter").val("#all");')
            driver.execute_script("doStocksFilter('select',this)")
            print('Executed JS scripts')
        while True:
            try:
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                table = soup.find('table', class_=table_class)
                if len(table.find_all('tr')) < object_.objects.count():
                    continue
                break
            except Exception as e: 
                print_exception(e)
                sleep(1)

    start = time.time()
    for _ in range(len(selenium_dct)-1):
        driver.execute_script("window.open('', '_blank')")
    for key, value in selenium_dct.items():
        i = list(selenium_dct.keys()).index(key)
        driver.switch_to.window(driver.window_handles[i])
        load_tab(driver, key, value['object'], value['type'], value['link'], value['table class'])
    
    print('Selenium Tabs are ready!')
    print(f'Init Selenium Tabs: {time.time() - start}')

def loop_selenium_tabs(driver):
    start = time.time()
    for tab in driver.window_handles:
        driver.switch_to.window(tab)
        print(driver.current_url)
        title = [key for key, value in TABLE_LINKS.items() if value == driver.current_url][0]
        table_class = STATIC_OBJECTS[title]['table class']
        while True:
            try:
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                table = soup.find('table', class_=table_class)
                print(len(table.find_all('tr')))
                break
            except Exception as e: 
                print_exception(e)
                sleep(1)
    print(f'Loop Selnium Tabs: {time.time()-start}')

# from scraper_app import live_scraper
# Logic of current module
# init selenium tabs
# loop and collect live data

# 1. Visit the link
# 2. Check condition
# 3. Call appropriate function
# 4. Repeat
driver = vps_selenium_setup()
print('Driver is ready!')
try:
    results = []
    start = time.time()
    
    init_selenium_tabs(driver, STATIC_OBJECTS)
    results.append(time.time() - start)
    
    for _ in range(3):
        start = time.time()
        loop_selenium_tabs(driver)
        results.append(time.time()-start)
    print(results)
finally:
    driver.quit()
    print('Driver is closed!')


    
     
# short_names = object_.objects.values_list('short_name') # [(,), (.)]
# short_names = [item[0] for item in short_names] # [, , ,]
# while True:
#     try:
#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         table = soup.find_all('table', class_=table_class)
#         print(f'{title}: {table.find_all('tr')[-1]}')
#         for tr in table.find_all('tr')[0]:
#             for td in tr.find_all('td'):
#                 td.get_text()
#                 print(td)
#             tds = []
#             for td in tr.find_all('td')[1:-1]:
#                 tds.append(td.get_text())
#             if not tds[0] in short_names:
#                 print(f'SKIPED ROW: {tds[0]}')
#                 continue # skip row 
#             link = 'https://www.investing.com' + tr.find_all('td')[1].a['href']
#             time_icon = tr.find_all('td')[-1].span['class'][0]
#             now = make_aware(datetime.datetime.now())
#             time_icons.append(time_icon)
#         print(f'{title}: table is updated ({datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")})')
#         break
#     except Exception as e:
#         print_exception(e)
#         print(f'{title}: Waiting more')
#         sleep(1)



# def commodities():
#     """  
#     If the market is closed (redClockIcon) then collect "after live"
    
#     If the market is open (greenClockIcon) then collect "live data" and every 1 minutes pass 
#     it to "historical 1D", every 5m to "historical 5D",  then check whether "before live data" for
#     the last "live data" day is collected
#     """
#     #----------------- ---VPS------------------
#     driver = vps_selenium_setup()
#     #-----------------------------------------
#     print('Commodities: driver is ready')
#     url = 'link': TABLE_LINKS['Commodities']
#     driver.get(url)
#     print('Commodities: table\'s link is visited')
#     c_list = models.CommodityStaticInfo.objects.values_list('short_name') # [(,), (.)]
#     c_list = [item[0] for item in c_list] # [, , ,]
#     try:
#         while True:
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
        

            
