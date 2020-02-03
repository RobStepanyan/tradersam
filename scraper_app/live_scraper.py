import requests, datetime, pytz, time
from django.utils.timezone import make_aware
from bs4 import BeautifulSoup
from time import sleep
from .scraper_functions import *
from . import models
from .models import (
    CommodityStaticInfo, CurrencyStaticInfo, CryptocurrencyStaticInfo, USStockStaticInfo, JapanStockStaticInfo,
    UKStockStaticInfo, HKStockStaticInfo, ChinaStockStaticInfo, CanadaStockStaticInfo, GermanyStockStaticInfo,
    AustraliaStockStaticInfo,
    # Indices 
    USIndexStaticInfo, JapanIndexStaticInfo, UKIndexStaticInfo, HKIndexStaticInfo, ChinaIndexStaticInfo,
    CanadaIndexStaticInfo, GermanyIndexStaticInfo, AustraliaIndexStaticInfo,
    # ETFs
    ETFIssuers, USETFStaticInfo, JapanETFStaticInfo, UKETFStaticInfo, HKETFStaticInfo, ChinaETFStaticInfo,
    CanadaETFStaticInfo, GermanyETFStaticInfo, AustraliaETFStaticInfo, ETF_ISSUERS_US, ETF_ISSUERS_JP, 
    ETF_ISSUERS_UK, ETF_ISSUERS_HK, ETF_ISSUERS_CH, ETF_ISSUERS_CA, ETF_ISSUERS_GE, ETF_ISSUERS_AU,
    # Bonds
    USBondStaticInfo, JapanBondStaticInfo, UKBondStaticInfo, HKBondStaticInfo, ChinaBondStaticInfo,
    CanadaBondStaticInfo, GermanyBondStaticInfo, AustraliaBondStaticInfo,
    # Markets
    MARKETS_US, MARKETS_JP, MARKETS_CH, MARKETS_CA, MARKETS_GE,
    # Funds
    FundIssuers, USFundStaticInfo, JapanFundStaticInfo, UKFundStaticInfo, HKFundStaticInfo, 
    ChinaFundStaticInfo, CanadaFundStaticInfo, GermanyFundStaticInfo, AustraliaFundStaticInfo,
    # Historical
    AllAssetsHistoricalMax, AllAssetsHistorical5Y, AllAssetsHistorical5D, AllAssetsHistorical1D,
    # Live
    AllAssetsBeforeLive, AllAssetsLive, AllAssetsAfterLive
)

TABLE_LINKS = {
    # JS Scripts are not used to access the table
    'Commodities': 'https://www.investing.com/commodities/real-time-futures',
    'Currencies': 'https://www.investing.com/currencies/',
    'Cryptocurrencies': 'https://www.investing.com/crypto/currencies',
    # Stocks - Same JS Scripts
    'US Stocks': 'https://www.investing.com/equities/united-states',
    'Japan Stocks': 'https://www.investing.com/equities/japan',
    'UK Stocks': 'https://www.investing.com/equities/united-kingdom',
    'HK Stocks': 'https://www.investing.com/equities/hong-kong',
    'China Stocks': 'https://www.investing.com/equities/china',
    'Canada Stocks': 'https://www.investing.com/equities/canada',
    'Germany Stocks': 'https://www.investing.com/equities/germany',
    'Australia Stocks': 'https://www.investing.com/equities/australia',
    # Indices - JS is not used, URLs contain all needed details
    'US Indices': 'https://www.investing.com/indices/usa-indices?&majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on',
    'Japan Indices': 'https://www.investing.com/indices/japan-indices?majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on',
    'UK Indices': 'https://www.investing.com/indices/uk-indices?majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on',
    'HK Indices': 'https://www.investing.com/indices/hong-kong-indices?majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on',
    'China Indices': 'https://www.investing.com/indices/china-indices?&majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on',
    'Canada Indices': 'https://www.investing.com/indices/canada-indices?majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on',
    'Germany Indices': 'https://www.investing.com/indices/germany-indices?majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on',
    'Australia Indices': 'https://www.investing.com/indices/australia-indices?majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on',
    # ETFs - JS is not used, URLs contain all needed details
    'US ETFs': 'https://www.investing.com/etfs/usa-etfs?&issuer_filter=0',
    'Japan ETFs': 'https://www.investing.com/etfs/japan-etfs?&issuer_filter=0',
    'UK ETFs': 'https://www.investing.com/etfs/uk-etfs?&issuer_filter=0',
    'HK ETFs': 'https://www.investing.com/etfs/hong-kong-etfs?&issuer_filter=0',
    'China ETFs': 'https://www.investing.com/etfs/china-etfs?&issuer_filter=0',
    'Canada ETFs': 'https://www.investing.com/etfs/canada-etfs?&issuer_filter=0',
    'Germany ETFs': 'https://www.investing.com/etfs/germany-etfs?&issuer_filter=0',
    'Australia ETFs': 'https://www.investing.com/etfs/australia-etfs?&issuer_filter=0',
    # Bonds - JS is not used, URLs contain all needed details
    'US Bonds': 'https://www.investing.com/rates-bonds/usa-government-bonds?maturity_from=40&maturity_to=290',
    'Japan Bonds': 'https://www.investing.com/rates-bonds/japan-government-bonds?maturity_from=40&maturity_to=300',
    'UK Bonds': 'https://www.investing.com/rates-bonds/uk-government-bonds?maturity_from=40&maturity_to=310',
    'HK Bonds': 'https://www.investing.com/rates-bonds/hong-kong-government-bonds?maturity_from=20&maturity_to=230',
    'China Bonds': 'https://www.investing.com/rates-bonds/china-government-bonds?maturity_from=90&maturity_to=290',
    'Canada Bonds': 'https://www.investing.com/rates-bonds/canada-government-bonds?maturity_from=40&maturity_to=290',
    'Germany Bonds': 'https://www.investing.com/rates-bonds/germany-government-bonds?maturity_from=40&maturity_to=290',
    'Australia Bonds': 'https://www.investing.com/rates-bonds/australia-government-bonds?maturity_from=40&maturity_to=290',
    # Funds - JS is not used, URLs contain all needed details
    'US Funds': 'https://www.investing.com/funds/usa-funds?&issuer_filter=0',
    'Japan Funds': 'https://www.investing.com/funds/japan-funds?&issuer_filter=0',
    'UK Funds': 'https://www.investing.com/funds/uk-funds?&issuer_filter=0',
    'HK Funds': 'https://www.investing.com/funds/hong-kong-funds?&issuer_filter=0',
    'China Funds': 'https://www.investing.com/funds/china-funds?&issuer_filter=0',
    'Canada Funds': 'https://www.investing.com/funds/canada-funds?&issuer_filter=0',
    'Germany Funds': 'https://www.investing.com/funds/germany-funds?&issuer_filter=0',
    'Australia Funds': 'https://www.investing.com/funds/australia-funds?&issuer_filter=0',
}
table_class = 'genTbl closedTbl crossRatesTbl'
table_class1 = 'genTbl closedTbl crossRatesTbl elpTbl elp25' 
table_class2 = 'genTbl closedTbl crossRatesTbl elpTbl elp30' 
table_class3 = 'genTbl closedTbl crossRatesTbl elpTbl elp40' 
STATIC_OBJECTS = {
    'Commodities': {
        'object': CommodityStaticInfo, 'type': 'cmdty', 'link': TABLE_LINKS['Commodities'], 'table class': table_class},
    'Currencies': {
        'object': CurrencyStaticInfo, 'type': 'crncy', 'link': TABLE_LINKS['Currencies'], 'table class': table_class},
    'Cryptocurrencies': {
        'object': CryptocurrencyStaticInfo, 'type': 'crptcrncy', 'link': TABLE_LINKS['Cryptocurrencies'], 'table class': 'genTbl openTbl js-all-crypto-table mostActiveStockTbl crossRatesTbl allCryptoTlb wideTbl elpTbl elp15'},
    'US Stocks': {
        'object': USStockStaticInfo, 'type': 'stck', 'link': TABLE_LINKS['US Stocks'], 'table class': table_class1},
    'Japan Stocks': {
        'object': JapanStockStaticInfo, 'type': 'stck', 'link': TABLE_LINKS['Japan Stocks'], 'table class': table_class1},
    'UK Stocks': {
        'object': UKStockStaticInfo, 'type': 'stck', 'link': TABLE_LINKS['UK Stocks'], 'table class': table_class1},
    'HK Stocks': {
        'object': HKStockStaticInfo, 'type': 'stck', 'link': TABLE_LINKS['HK Stocks'], 'table class': table_class1},
    'China Stocks': {
        'object': ChinaStockStaticInfo, 'type': 'stck', 'link': TABLE_LINKS['China Stocks'], 'table class': table_class1},
    'Canada Stocks': {
        'object': CanadaStockStaticInfo, 'type': 'stck', 'link': TABLE_LINKS['Canada Stocks'], 'table class': table_class1},
    'Germany Stocks': {
        'object': GermanyStockStaticInfo, 'type': 'stck', 'link': TABLE_LINKS['Germany Stocks'], 'table class': table_class1},
    'Australia Stocks': {
        'object': AustraliaStockStaticInfo, 'type': 'stck', 'link': TABLE_LINKS['Australia Stocks'], 'table class': table_class1},
    
    'US Indices': {
        'object': USIndexStaticInfo, 'type': 'indx', 'link': TABLE_LINKS['US Indices'], 'table class': table_class2},
    'Japan Indices': {
        'object': JapanIndexStaticInfo, 'type': 'indx', 'link': TABLE_LINKS['Japan Indices'], 'table class': table_class2},
    'UK Indices': {
        'object': UKIndexStaticInfo, 'type': 'indx', 'link': TABLE_LINKS['UK Indices'], 'table class': table_class2},
    'HK Indices': {
        'object': HKIndexStaticInfo, 'type': 'indx', 'link': TABLE_LINKS['HK Indices'], 'table class': table_class2},
    'China Indices': {
        'object': ChinaIndexStaticInfo, 'type': 'indx', 'link': TABLE_LINKS['China Indices'], 'table class': table_class2},
    'Canada Indices': {
        'object': CanadaIndexStaticInfo, 'type': 'indx', 'link': TABLE_LINKS['Canada Indices'], 'table class': table_class2},
    'Germany Indices': {
        'object': GermanyIndexStaticInfo, 'type': 'indx', 'link': TABLE_LINKS['Germany Indices'], 'table class': table_class2},
    'Australia Indices': {
        'object': AustraliaIndexStaticInfo, 'type': 'indx', 'link': TABLE_LINKS['Australia Indices'], 'table class': table_class2},
    
    'US ETFs': {
        'object': USETFStaticInfo, 'type': 'etf', 'link': TABLE_LINKS['US ETFs'], 'table class': table_class3},
    'Japan ETFs': {
        'object': JapanETFStaticInfo, 'type': 'etf', 'link': TABLE_LINKS['Japan ETFs'], 'table class': table_class3},
    'UK ETFs': {
        'object': UKETFStaticInfo, 'type': 'etf', 'link': TABLE_LINKS['UK ETFs'], 'table class': table_class3},
    'HK ETFs': {
        'object': HKETFStaticInfo, 'type': 'etf', 'link': TABLE_LINKS['HK ETFs'], 'table class': table_class3},
    'China ETFs': {
        'object': ChinaETFStaticInfo, 'type': 'etf', 'link': TABLE_LINKS['China ETFs'], 'table class': table_class3},
    'Canada ETFs': {
        'object': CanadaETFStaticInfo, 'type': 'etf', 'link': TABLE_LINKS['Canada ETFs'], 'table class': table_class3},
    'Germany ETFs': {
        'object': GermanyETFStaticInfo, 'type': 'etf', 'link': TABLE_LINKS['Germany ETFs'], 'table class': table_class3},
    'Australia ETFs': {
        'object': AustraliaETFStaticInfo, 'type': 'etf', 'link': TABLE_LINKS['Australia ETFs'], 'table class': table_class3},
    
    'US Bonds': {
        'object': USBondStaticInfo, 'type': 'bnd', 'link': TABLE_LINKS['US Bonds'], 'table class': table_class},
    'Japan Bonds': {
        'object': JapanBondStaticInfo, 'type': 'bnd', 'link': TABLE_LINKS['Japan Bonds'], 'table class': table_class},
    'UK Bonds': {
        'object': UKBondStaticInfo, 'type': 'bnd', 'link': TABLE_LINKS['UK Bonds'], 'table class': table_class},
    'HK Bonds': {
        'object': HKBondStaticInfo, 'type': 'bnd', 'link': TABLE_LINKS['HK Bonds'], 'table class': table_class},
    'China Bonds': {
        'object': ChinaBondStaticInfo, 'type': 'bnd', 'link': TABLE_LINKS['China Bonds'], 'table class': table_class},
    'Canada Bonds': {
        'object': CanadaBondStaticInfo, 'type': 'bnd', 'link': TABLE_LINKS['Canada Bonds'], 'table class': table_class},
    'Germany Bonds': {
        'object': GermanyBondStaticInfo, 'type': 'bnd', 'link': TABLE_LINKS['Germany Bonds'], 'table class': table_class},
    'Australia Bonds': {
        'object': AustraliaBondStaticInfo, 'type': 'bnd', 'link': TABLE_LINKS['Australia Bonds'], 'table class': table_class},
    
    'US Funds': {
        'object': USFundStaticInfo, 'type': 'fnd', 'link': TABLE_LINKS['US Funds'], 'table class': table_class3},
    'Japan Funds': {
        'object': JapanFundStaticInfo, 'type': 'fnd', 'link': TABLE_LINKS['Japan Funds'], 'table class': table_class3},
    'UK Funds': {
        'object': UKFundStaticInfo, 'type': 'fnd', 'link': TABLE_LINKS['UK Funds'], 'table class': table_class3},
    'HK Funds': {
        'object': HKFundStaticInfo, 'type': 'fnd', 'link': TABLE_LINKS['HK Funds'], 'table class': table_class3},
    'China Funds': {
        'object': ChinaFundStaticInfo, 'type': 'fnd', 'link': TABLE_LINKS['China Funds'], 'table class': table_class3},
    'Canada Funds': {
        'object': CanadaFundStaticInfo, 'type': 'fnd', 'link': TABLE_LINKS['Canada Funds'], 'table class': table_class3},
    'Germany Funds': {
        'object': GermanyFundStaticInfo, 'type': 'fnd', 'link': TABLE_LINKS['Germany Funds'], 'table class': table_class3},
    'Australia Funds': {
        'object': AustraliaFundStaticInfo, 'type': 'fnd', 'link': TABLE_LINKS['Australia Funds'], 'table class': table_class3},
}

def init_selenium_tabs(driver, selenium_dct):
    # Opening a tab
    def work(driver, title, object_, type_, link, table_class):
        print(f'{title}: Visiting the Table')
        driver.execute_script(f'window.open("","_blank");') # open new blank tab
        for tab in driver.window_handles[::-1]:
            driver.switch_to.window(tab)
            if driver.current_url == 'about:blank':
                break
            
        print(f'{title}: Waiting the page to load')
        driver.get(link) # visit the link
        print('Executing JS scripts')
        driver.execute_script('$("#stocksFilter").val("#all");')
        driver.execute_script("doStocksFilter('select',this)")
        print('Executed JS scripts, sleeping for 15 seconds')
        sleep(15)
        while True:
            try:
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                table = soup.find('table', class_=table_class)
                if len(table.find_all('tr')) < object_.objects.count():
                    continue
                break
            except Exception as e: 
                print_exception(e)
                sleep(1)
    
    start = time.time()
    for key, value in selenium_dct.items():
        work(driver, key, value['object'], value['type'], value['link'], value['table class'])
    
    print('Selenium Tabs are ready!')
    print(f'Init Selenium Tabs: {time.time() - start}')

def loop_selenium_tabs(driver):
    start = time.time()
    tabs = driver.window_handles
    for tab in tabs:
        driver.switch_to.window(tab)
        print(driver.current_url)
        if driver.current_url in 'data:, about:blank':
            continue
        title = [key for key, value in TABLE_LINKS.items() if value == driver.current_url][0]
        table_class = STATIC_OBJECTS[title]['table class']
        while True:
            try:
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                table = soup.find('table', class_=table_class)
                # print('The page have been loaded!')
                print(len(table.find_all('tr')))
                break
            except Exception as e: 
                print_exception(e)
                sleep(1)
    print(f'Loop Selnium Tabs: {time.time()-start}')

header  ={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) CArome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
def non_selenium_requests(non_selenium_dct):
    # Send a request
    def work(title, object_, type_, link, table_class):
        print(f'{title}: Visiting the Table')
        req = requests.get(link, headers=header)
        print(f'{title}: Waiting the page to load')
        soup = BeautifulSoup(req.text, 'html.parser')
        table = soup.find('table', class_=table_class)
        print(len(table.find_all('tr')))

    start = time.time()
    for key, value in non_selenium_dct.items():
        work(key, value['object'], value['type'], value['link'], value['table class'])
    print(f'Non-Selenium Requests: {time.time()-start}')

def seperate_dct(dct):
    selenium_dct, non_selenium_dct = {}, {}
    for key, value in dct.items():
        if 'Stock' in key:
            selenium_dct[key] = value
        else:
            non_selenium_dct[key] = value
    return selenium_dct, non_selenium_dct


# from scraper_app import live_scraper as l
# Logic of current module
# init
# open stocks' tabs with selenium and execute js scripts
# others are visited with request.get

# 1. Visit the link
# 2. Check condition
# 3. Call appropriate function
# 4. Repeat
driver = vps_selenium_setup()
print('Driver is ready')
try:
    start = time.time()
    
    selenium_dct, non_selenium_dct = seperate_dct(STATIC_OBJECTS)
    init_selenium_tabs(driver, selenium_dct)
    # non_selenium_requests(non_selenium_dct)
    
    with_init = time.time() - start
    
    start = time.time()
    
    loop_selenium_tabs(driver)
    # non_selenium_requests(non_selenium_dct)

    print(f'With init: {with_init}, Without: {time.time() - start}')
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
        

            
