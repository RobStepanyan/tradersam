import requests, datetime, pytz
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

STATIC_OBJECTS = {
    'Commodities': [CommodityStaticInfo, 'cmdty'],
    'Currencies': [CurrencyStaticInfo, 'crncy'],
    'Cryptocurrencies': [CryptocurrencyStaticInfo, 'crptcrncy'],
    
    'US Stocks': [USStockStaticInfo, 'stck'],
    'Japan Stocks': [JapanStockStaticInfo, 'stck'],
    'UK Stocks': [UKStockStaticInfo, 'stck'],
    'HK Stocks': [HKStockStaticInfo, 'stck'],
    'China Stocks': [ChinaStockStaticInfo, 'stck'],
    'Canada Stocks': [CanadaStockStaticInfo, 'stck'],
    'Germany Stocks': [GermanyStockStaticInfo, 'stck'],
    'Australia Stocks': [AustraliaStockStaticInfo, 'stck'],
    
    'US Indices': [USIndexStaticInfo, 'indx'],
    'Japan Indices': [JapanIndexStaticInfo, 'indx'],
    'UK Indices': [UKIndexStaticInfo, 'indx'],
    'HK Indices': [HKIndexStaticInfo, 'indx'],
    'China Indices': [ChinaIndexStaticInfo, 'indx'],
    'Canada Indices': [CanadaIndexStaticInfo, 'indx'],
    'Germany Indices': [GermanyIndexStaticInfo, 'indx'],
    'Australia Indices': [AustraliaIndexStaticInfo, 'indx'],
    
    'US ETFs': [USETFStaticInfo, 'etf'],
    'Japan ETFs': [JapanETFStaticInfo, 'etf'],
    'UK ETFs': [UKETFStaticInfo, 'etf'],
    'HK ETFs': [HKETFStaticInfo, 'etf'],
    'China ETFs': [ChinaETFStaticInfo, 'etf'],
    'Canada ETFs': [CanadaETFStaticInfo, 'etf'],
    'Germany ETFs': [GermanyETFStaticInfo, 'etf'],
    'Australia ETFs': [AustraliaETFStaticInfo, 'etf'],
    
    'US Bonds': [USBondStaticInfo, 'bnd'],
    'Japan Bonds': [JapanBondStaticInfo, 'bnd'],
    'UK Bonds': [UKBondStaticInfo, 'bnd'],
    'HK Bonds': [HKBondStaticInfo, 'bnd'],
    'China Bonds': [ChinaBondStaticInfo, 'bnd'],
    'Canada Bonds': [CanadaBondStaticInfo, 'bnd'],
    'Germany Bonds': [GermanyBondStaticInfo, 'bnd'],
    'Australia Bonds': [AustraliaBondStaticInfo, 'bnd'],
    
    'US Funds': [USFundStaticInfo, 'fnd'],
    'Japan Funds': [JapanFundStaticInfo, 'fnd'],
    'UK Funds': [UKFundStaticInfo, 'fnd'],
    'HK Funds': [HKFundStaticInfo, 'fnd'],
    'China Funds': [ChinaFundStaticInfo, 'fnd'],
    'Canada Funds': [CanadaFundStaticInfo, 'fnd'],
    'Germany Funds': [GermanyFundStaticInfo, 'fnd'],
    'Australia Funds': [AustraliaFundStaticInfo, 'fnd'],
}

# from scraper_app import live_scraper as l
# Logic of current module
# 1. Visit the link
# 2. Check condition
# 3. Call appropriate function
# 4. Repeat
def start():
    driver = vps_selenium_setup()
    print('Driver is ready')
    try:
        import time
        start_time = time.time()
        threads_by_chunks(target=work)
        for title, link in TABLE_LINKS.items():
            work(driver, title, link)

        print(time.time() - start_time)
    finally:
        driver.quit()
        print('Driver is closed!')


def work(driver, title, link):
    # while True:
    time_icons = []
    print(f'{title}: Visiting the Table')
    driver.get(link)
    print('Waiting the page to load')
    sleep(3)
    short_names = STATIC_OBJECTS[title][0].objects.values_list('short_name') # [(,), (.)]
    short_names = [item[0] for item in short_names] # [, , ,]
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.find('table', class_='genTbl closedTbl crossRatesTbl').tbody
        print(f'{title}: table is updated ({datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")})')
        for tr in table.find_all('tr'):
            tds = []
            for td in tr.find_all('td')[1:-1]:
                tds.append(td.get_text())
            if not tds[0] in short_names:
                print(f'SKIPED ROW: {tds[0]}')
                continue # skip row 
            link = 'https://www.investing.com' + tr.find_all('td')[1].a['href']
            time_icon = tr.find_all('td')[-1].span['class'][0]
            now = make_aware(datetime.datetime.now())
            time_icons.append(time_icon)
    except:
        print('Waiting more')
        sleep(2)






def commodities():
    """  
    If the market is closed (redClockIcon) then collect "after live"
    
    If the market is open (greenClockIcon) then collect "live data" and every 1 minutes pass 
    it to "historical 1D", every 5m to "historical 5D",  then check whether "before live data" for
    the last "live data" day is collected
    """
    #----------------- ---VPS------------------
    driver = vps_selenium_setup()
    #-----------------------------------------
    print('Commodities: driver is ready')
    url = TABLE_LINKS['Commodities']
    driver.get(url)
    print('Commodities: table\'s link is visited')
    c_list = models.CommodityStaticInfo.objects.values_list('short_name') # [(,), (.)]
    c_list = [item[0] for item in c_list] # [, , ,]
    try:
        while True:
            print('Commodities: waiting...')
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            table = soup.find('table', class_='genTbl closedTbl crossRatesTbl').tbody
            print(f'Commodities: table is updated ({datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")})')
            for tr in table.find_all('tr'):
                tds = []
                for td in tr.find_all('td')[1:-1]:
                    tds.append(td.get_text())
                if not tds[0] in c_list:
                    print(f'SKIPED ROW: {tds[0]}')
                    continue # skip row 
                link = 'https://www.investing.com' + tr.find_all('td')[1].a['href']
                time_icon = tr.find_all('td')[-1].span['class'][0]
                now = make_aware(datetime.datetime.now())
                if time_icon == 'greenClockIcon':
                    month = tds[1].strip()
                    # Update Live Data
                    if month in '  ':
                        month = None
                    else:
                        month = datetime.datetime.strptime(month, '%b %y')

                    AllAssetsLive.objects.filter(link=link).delete()
                    AllAssetsLive(
                        short_name=tds[0], link=link, 
                        month=month,
                        last_price=tds[2], last_price_time=tds[7],
                        high=tds[3], low=tds[4],
                        change=tds[5], change_perc=[tds[6]],
                        Type='cmdty'
                    ).save()
                    print('Commodities: saved LIVE')

                    def collectBeforeLive():
                        header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'}
                        request = requests.get(link, headers=header)
                        print(link)
                        while True:
                            try:
                                soup = BeautifulSoup(request.text, 'html.parser')
                                prev_close = soup.find('span', text='Prev. Close:').find_next_sibling('span').get_text()
                                Open = soup.find('span', text='Open:').find_next_sibling('span').get_text()
                                break
                            except Exception as e:
                                print_exception(e)
                                sleep(3)
                        
                        AllAssetsBeforeLive(
                            short_name=tds[0], link=link,
                            date=now.date(),
                            prev_close=prev_close, Open=Open,
                            Type='cmdty'
                        ).save()
                        print('Commodities: saved BEFORELIVE')

                    last_obj_before_count = AllAssetsBeforeLive.objects.filter(link=link).count()
                    if last_obj_before_count > 0:
                        last_obj_before = AllAssetsBeforeLive.objects.filter(link=link).order_by('-id')[0]
                    
                    if last_obj_before_count == 0:
                        collectBeforeLive()
                    elif (now.date() - last_obj_before.date).days >= 1:
                        collectBeforeLive()
                
                    # Send data to AllAssetsHistorical1D once a minute, ...Historical5D once 5 minutes
                    last_obj_1d_count = AllAssetsHistorical1D.objects.filter(link=link).count()
                    if last_obj_1d_count > 0:
                        last_obj_1d = AllAssetsHistorical1D.objects.filter(link=link).order_by('-id')[0]
                    
                    last_obj_5d_count = AllAssetsHistorical5D.objects.filter(link=link).count()
                    if last_obj_5d_count > 0:
                        last_obj_5d = AllAssetsHistorical5D.objects.filter(link=link).order_by('-id')[0]
                    
                    if last_obj_1d_count == 0 or last_obj_1d.date.minute<now.minute:
                        # if there's no data at all or latest data is already outdated
                        # send (Save) data
                        AllAssetsHistorical1D(
                            short_name=tds[0], link=link,
                            date=now,
                            price=tds[2],
                            Type='cmdty'
                        ).save()
                        print('Commodities: saved HISTORICAL1D')

                        if last_obj_1d_count:
                            data1 = last_obj_1d.date
                            data2 = now
                            diff = data2 - data1
                            days, seconds = diff.days, diff.seconds
                            hours = days * 24 + seconds // 3600
                            if hours > 24:
                                AllAssetsHistorical1D.objects.filter(link=link).order_by('id')[0].delete()
                    if (last_obj_5d_count == 0 or now.minute - last_obj_5d.date.minute>=5) and now.minute % 5 == 0:
                        # if there's no data at all or latest data is already outdated also divisible by 5
                        # send (Save) data
                        AllAssetsHistorical5D(
                            short_name=tds[0], link=link,
                            date=now,
                            price=tds[2],
                            Type='cmdty'
                        ).save()
                        print('Commodities: saved HISTORICAL5D')
                        
                        if last_obj_5d_count:
                            data1 = last_obj_5d.date
                            data2 = now
                            diff = data2 - data1
                            days, seconds = diff.days, diff.seconds
                            hours = days * 24 + seconds // 3600
                            if hours > 24*5:
                                AllAssetsHistorical5D.objects.filter(link=link).order_by('id')[0].delete()
                elif time_icon == 'redClockIcon':
                    # check whether "after live data" for today is available
                    last_obj_after_count = AllAssetsAfterLive.objects.filter(link=link).count()
                    if last_obj_after_count > 0:
                        last_obj_after = AllAssetsAfterLive.objects.filter(link=link).order_by('-id')[0]

                    def collectAfterLive():
                        header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'}
                        request = requests.get(link, headers=header)
                        print(f'Visited: {link}')
                        while True:
                            try:
                                soup = BeautifulSoup(request.text, 'html.parser')
                                one_year_rng = soup.find('span', text='52 wk Range').find_next_sibling('span').get_text()
                                one_year_chg = soup.find('span', text='1-Year Change').find_next_sibling('span').get_text()
                                months = soup.find('span', text='Months').find_next_sibling('span').get_text()
                                settlement_day = soup.find('span', text='Settlement Day').find_next_sibling('span').get_text()
                                try:
                                    settlement_day = datetime.datetime.strptime(settlement_day, '%m/%d/%Y')
                                except:
                                    settlement_day = None
                                last_roll_day = soup.find('span', text='Last Rollover Day').find_next_sibling('span').get_text()
                                try:
                                    last_roll_day = datetime.datetime.strptime(last_roll_day, '%m/%d/%Y')
                                except:
                                    last_roll_day = None
                                break
                            except Exception as e:
                                print_exception(e)
                                sleep(3)

                        AllAssetsAfterLive(
                            short_name=tds[0], link=link,
                            date=now.date(),
                            one_year_rng=one_year_rng, one_year_chg=one_year_chg.strip(),
                            months=months, 
                            settlement_day=settlement_day, last_roll_day=last_roll_day,
                            Type='cmdty'
                        ).save()
                        print(f'Commodities: saved AFTERLIVE for {tds[0]}')

                    if last_obj_after_count == 0:
                        collectAfterLive()
                    elif (now.date() - last_obj_after.date).days >= 1:
                        # if last after live data is outdated
                        collectAfterLive()
                else:
                    print('Time Icon is not found/recognized')
    finally:
        driver.quit()
        

            
