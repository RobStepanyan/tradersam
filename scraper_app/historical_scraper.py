# FOR SCRAPING (COLLECTING) DATA FROM MAX TO 1M
import os, datetime, sys
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from time import sleep
from .scraper_functions import *
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
    AllAssetsHistoricalMax, AllAssetsHistorical5Y, AllAssetsHistorical1Y, AllAssetsHistorical6M1M
)
"""


Do NOT use this file. It is deprecated!
Use hist_scraper.py instead.

DEPRECATED DEPRECATED DEPRECATED DEPRECATED DEPRECATED DEPRECATED 
DEPRECATED DEPRECATED DEPRECATED DEPRECATED DEPRECATED DEPRECATED 
DEPRECATED DEPRECATED DEPRECATED DEPRECATED DEPRECATED DEPRECATED 
DEPRECATED DEPRECATED DEPRECATED DEPRECATED DEPRECATED DEPRECATED 
DEPRECATED DEPRECATED DEPRECATED DEPRECATED DEPRECATED DEPRECATED 
DEPRECATED DEPRECATED DEPRECATED DEPRECATED DEPRECATED DEPRECATED 
DEPRECATED DEPRECATED DEPRECATED DEPRECATED DEPRECATED DEPRECATED
"""

class CollectAllAssetsHistoricalMax:
# from scraper_app import historical_scraper as h
# h.CollectAllAssetsHistoricalMax.commodities(delete='n')
# h.CollectAllAssetsHistoricalMax.currencies(delete='n')
# h.CollectAllAssetsHistoricalMax.cryptocurrencies(delete='n')
# h.CollectAllAssetsHistoricalMax.stocks()
# h.CollectAllAssetsHistoricalMax.indices()
# h.CollectAllAssetsHistoricalMax.etfs()
# h.CollectAllAssetsHistoricalMax.bonds()
# h.CollectAllAssetsHistoricalMax.funds()

    def commodities(delete='n'):
        c_list = CommodityStaticInfo.objects.values_list('country', 'short_name', 'link') # returns a list of tuples
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.commodities()')
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistoricalMax.commodities()')
            return ''
        print('Removing old records')
        AllAssetsHistoricalMax.objects.filter(Type='cmdty').delete()
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            x = list(c_list).index(i)+1
            link = i[2]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            driver.get(link)
            sleep(2)
            x = list(c_list).index(i) + 1
            while True:
                try:
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol
                        Type = 'cmdty'
                        country = i[0]
                        short_name = i[1]
                        AllAssetsHistoricalMax(
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    print(f'Stored {x}/{len(c_list)}')
                    x += 1
                    break
                except Exception as e:
                    print_exception(e)
                    print('Waiting for 3 more seconds')
                    sleep(3)
                    continue

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)
        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def currencies(delete='n'):
        c_list = CurrencyStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        driver = vps_selenium_setup()
        try:
            print('Starting CollectAllAssetsHistoricalMax.currencies()') #change here
            if delete.upper() != 'Y':
                print('Closing CollectAllAssetsHistoricalMax.currencies()') #change here
                return ''
            print('Removing old records')
            AllAssetsHistoricalMax.objects.filter(Type='crncy').delete() #change here
            print('Old records have been removed')
            print('Starting to collect new ones')
            print('Starting Selenium')
            # driver = webdriver.Chrome()
            def work(i):
                link = i[1]
                if '?cid' in link:
                    cid = link[link.index('?cid'):]
                    link = link[:link.index('?cid')]
                    link += '-historical-data' + cid
                else:
                    link += '-historical-data'
                driver.get(link)
                x = list(c_list).index(i) + 1
                while True:
                    try:
                        x = list(c_list).index(i) + 1
                        print(link)
                        execute_js_scripts_max(driver)
                        soup = BeautifulSoup(driver.page_source, 'html.parser')
                        print(soup.find(id='widgetFieldDateRange'))
                        soup = soup.find(class_='genTbl closedTbl historicalTbl')
                        soup = soup.tbody.find_all('tr')
                        print(len(soup))
                        for row in soup:
                            data = row.find_all('td')
                            data = [d.get_text() for d in data]
                            date = datetime.datetime.strptime(data[0], '%b %y')
                            price = validate_price(data[1])
                            Open = validate_price(data[2])
                            high = validate_price(data[3])
                            low = validate_price(data[4])
                            volume = None  #change here
                            change_perc = data[5][:-1] # Removing % symbol
                            Type = 'crncy'  #change here
                            country = 'G'  #change here
                            short_name = i[0]  #change here
                            AllAssetsHistoricalMax( 
                                Type=Type, country=country, short_name=short_name,
                                date=date, price=price, Open=Open,
                                high=high, low=low, change_perc=change_perc,
                                volume=volume).save()
                        print(f'Stored {x}/{len(c_list)}')
                        x += 1
                        break
                    except Exception as e:
                        print_exception(e)
                        print('Waiting for 3 more seconds')
                        sleep(3)
                        continue
            work()
        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def cryptocurrencies(delete='n'):
        c_list = CryptocurrencyStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = CryptocurrencyStaticInfo.objects.count()
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.cryptocurrencies()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistoricalMax.cryptocurrencies()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistoricalMax.objects.filter(Type='crptcrncy').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
    
        def work(i):
            if i[1] == None:
                return
            x = list(c_list).index(i)+1
            link = i[1] + '/historical-data' #change here
            driver.get(link)
            sleep(2)
            x = list(c_list).index(i) + 1
            while True:
                try:
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    print(soup.find(id='widgetFieldDateRange'))
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        if len(price) > 12: # in case of invalid data
                            price = None
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'crptcrncy'  #change here
                        country = 'G'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    print(f'Stored {x}/{quanity}: {short_name}')
                    x+=1
                    break
                except Exception as e:
                    print_exception(e)
                    print('Waiting for 3 more seconds')
                    sleep(3)
                    continue
        
        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def stocks():
        print('Do you want to delete old records and collect new ones? ')
        delete = input('Y (Yes) or N (No): ')
        if delete.upper() == 'Y':
            CollectAllAssetsHistoricalMax.usstocks(delete=delete)
            CollectAllAssetsHistoricalMax.japanstocks(delete=delete)
            CollectAllAssetsHistoricalMax.ukstocks(delete=delete)
            CollectAllAssetsHistoricalMax.hkstocks(delete=delete)
            CollectAllAssetsHistoricalMax.chinastocks(delete=delete)
            CollectAllAssetsHistoricalMax.canadastocks(delete=delete)
            CollectAllAssetsHistoricalMax.germanystocks(delete=delete)
            CollectAllAssetsHistoricalMax.australiastocks(delete=delete)
        else:
            print(f'Closing... Your answer was: {delete}')

    def indices():
        print('Do you want to delete old records and collect new ones? ')
        delete = input('Y (Yes) or N (No): ')
        if delete.upper() == 'Y':
            CollectAllAssetsHistoricalMax.usindices(delete=delete)
            CollectAllAssetsHistoricalMax.japanindices(delete=delete)
            CollectAllAssetsHistoricalMax.ukindices(delete=delete)
            CollectAllAssetsHistoricalMax.hkindices(delete=delete)
            CollectAllAssetsHistoricalMax.chinaindices(delete=delete)
            CollectAllAssetsHistoricalMax.canadaindices(delete=delete)
            CollectAllAssetsHistoricalMax.germanyindices(delete=delete)
            CollectAllAssetsHistoricalMax.australiaindices(delete=delete)        
        else:
            print(f'Closing... Your answer was: {delete}')

    def etfs():
        print('Do you want to delete old records and collect new ones? ')
        delete = input('Y (Yes) or N (No): ')
        if delete.upper() == 'Y':
            CollectAllAssetsHistoricalMax.usetfs(delete=delete)
            CollectAllAssetsHistoricalMax.japanetfs(delete=delete)
            CollectAllAssetsHistoricalMax.uketfs(delete=delete)
            CollectAllAssetsHistoricalMax.hketfs(delete=delete)
            CollectAllAssetsHistoricalMax.chinaetfs(delete=delete)
            CollectAllAssetsHistoricalMax.canadaetfs(delete=delete)
            CollectAllAssetsHistoricalMax.germanyetfs(delete=delete)
            CollectAllAssetsHistoricalMax.australiaetfs(delete=delete)        
        else:
            print(f'Closing... Your answer was: {delete}')

    def bonds():
        print('Do you want to delete old records and collect new ones? ')
        delete = input('Y (Yes) or N (No): ')
        if delete.upper() == 'Y':
            CollectAllAssetsHistoricalMax.usbonds(delete=delete)
            CollectAllAssetsHistoricalMax.japanbonds(delete=delete)
            CollectAllAssetsHistoricalMax.ukbonds(delete=delete)
            CollectAllAssetsHistoricalMax.hkbonds(delete=delete)
            CollectAllAssetsHistoricalMax.chinabonds(delete=delete)
            CollectAllAssetsHistoricalMax.canadabonds(delete=delete)
            CollectAllAssetsHistoricalMax.germanybonds(delete=delete)
            CollectAllAssetsHistoricalMax.australiabonds(delete=delete)        
        else:
            print(f'Closing... Your answer was: {delete}')

    def funds():
        print('Do you want to delete old records and collect new ones? ')
        delete = input('Y (Yes) or N (No): ')
        if delete.upper() == 'Y':
            CollectAllAssetsHistoricalMax.usfunds(delete=delete)
            CollectAllAssetsHistoricalMax.japanfunds(delete=delete)
            CollectAllAssetsHistoricalMax.ukfunds(delete=delete)
            CollectAllAssetsHistoricalMax.hkfunds(delete=delete)
            CollectAllAssetsHistoricalMax.chinafunds(delete=delete)
            CollectAllAssetsHistoricalMax.canadafunds(delete=delete)
            CollectAllAssetsHistoricalMax.germanyfunds(delete=delete)
            CollectAllAssetsHistoricalMax.australiafunds(delete=delete)        
        else:
            print(f'Closing... Your answer was: {delete}')

    def usstocks(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = USStockStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = USStockStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.usstocks()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.usstocks()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='stck', country='US').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'stck'  #change here
                        country = 'US'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def japanstocks(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = JapanStockStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = JapanStockStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.japanstocks()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.japanstocks()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='stck', country='JP').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'stck'  #change here
                        country = 'JP'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def ukstocks(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = UKStockStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = UKStockStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.ukstocks()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.ukstocks()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='stck', country='UK').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'stck'  #change here
                        country = 'UK'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                        # print(date, price, Open, high, low, change_perc, volume)
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def hkstocks(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = HKStockStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = HKStockStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.hkstocks()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.hkstocks()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='stck', country='HK').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'stck'  #change here
                        country = 'HK'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')
    
    def chinastocks(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = USStockStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = USStockStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.chinastocks()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.chinastocks()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='stck', country='CH').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'stck'  #change here
                        country = 'CH'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def canadastocks(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = CanadaStockStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = CanadaStockStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.canadastocks()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.canadastocks()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='stck', country='CA').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'stck'  #change here
                        country = 'CA'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def germanystocks(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = GermanyStockStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = GermanyStockStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.germanystocks()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.germanystocks()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='stck', country='GE').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'stck'  #change here
                        country = 'GE'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def australiastocks(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = AustraliaStockStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = AustraliaStockStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.australiastocks()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.australiastocks()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='stck', country='AU').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'stck'  #change here
                        country = 'AU'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def usindices(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = USIndexStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = USIndexStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.usindices()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.usindices()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='indx', country='US').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        if volume == '-':
                            volume = None
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'indx'  #change here
                        country = 'US'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly') 

    def japanindices(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = JapanIndexStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = JapanIndexStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.japanindices()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.japanindices()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='indx', country='JP').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        if volume == '-':
                            volume = None
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'indx'  #change here
                        country = 'JP'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')   

    def ukindices(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = UKIndexStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = UKIndexStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.ukindices()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.ukindices()') #change here
            return ''
        # AllAssetsHistoricalMax.objects.filter(Type='indx', country='UK').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        if volume == '-':
                            volume = None
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'indx'  #change here
                        country = 'UK'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')       

    def hkindices(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = HKIndexStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = HKIndexStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.hkindices()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.hkindices()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='indx', country='HK').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        if volume == '-':
                            volume = None
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'indx'  #change here
                        country = 'HK'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly') 

    def chinaindices(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = ChinaIndexStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = ChinaIndexStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.chinaindices()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.chinaindices()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='indx', country='CH').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        if volume == '-':
                            volume = None
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'indx'  #change here
                        country = 'CH'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def canadaindices(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = CanadaIndexStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = CanadaIndexStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.canadaindices()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.canadaindices()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='indx', country='CA').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        if volume == '-':
                            volume = None
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'indx'  #change here
                        country = 'CA'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly') 

    def germanyindices(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = GermanyIndexStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = GermanyIndexStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.germanyindices()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.germanyindices()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='indx', country='GE').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        if volume == '-':
                            volume = None
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'indx'  #change here
                        country = 'GE'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly') 

    def australiaindices(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = AustraliaIndexStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = AustraliaIndexStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.australiaindices()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.australiaindices()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='indx', country='AU').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        if volume == '-':
                            volume = None
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'indx'  #change here
                        country = 'AU'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly') 

    def usetfs(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = USETFStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = USETFStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.usetfs()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.usetfs()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='etf', country='US').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'etf'  #change here
                        country = 'US'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def japanetfs(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = JapanETFStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = JapanETFStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.japanetfs()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.japanetfs()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='etf', country='JP').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'etf'  #change here
                        country = 'JP'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def uketfs(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = UKETFStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = UKETFStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.uketfs()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.uketfs()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='etf', country='UK').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'etf'  #change here
                        country = 'UK'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def hketfs(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = HKETFStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = HKETFStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.hketfs()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.hketfs()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='etf', country='HK').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'etf'  #change here
                        country = 'HK'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def chinaetfs(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = ChinaETFStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = ChinaETFStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.chinaetfs()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.chinaetfs()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='etf', country='CH').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'etf'  #change here
                        country = 'CH'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def canadaetfs(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = CanadaETFStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = CanadaETFStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.canadaetfs()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.canadaetfs()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='etf', country='CA').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'etf'  #change here
                        country = 'CA'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def germanyetfs(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = GermanyETFStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = GermanyETFStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.germanyetfs()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.germanyetfs()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='etf', country='GE').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'etf'  #change here
                        country = 'GE'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def australiaetfs(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = AustraliaETFStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = AustraliaETFStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.australiaetfs()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.australiaetfs()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='etf', country='AU').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'etf'  #change here
                        country = 'AU'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def usbonds(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = USBondStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = USBondStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.usbonds()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.usbonds()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='bnd', country='US').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = None  #change here
                        change_perc = data[5][:-1] # Removing % symbol #change here
                        Type = 'bnd'  #change here
                        country = 'US'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def japanbonds(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = JapanBondStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = JapanBondStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.japanbonds()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.japanbonds()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='bnd', country='JP').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = None  #change here
                        change_perc = data[5][:-1] # Removing % symbol #change here
                        Type = 'bnd'  #change here
                        country = 'JP'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def ukbonds(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = UKBondStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = UKBondStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.ukbonds()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.ukbonds()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='bnd', country='UK').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = None  #change here
                        change_perc = data[5][:-1] # Removing % symbol #change here
                        Type = 'bnd'  #change here
                        country = 'UK'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def hkbonds(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = HKBondStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = HKBondStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.hkbonds()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.hkbonds()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='bnd', country='HK').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = None  #change here
                        change_perc = data[5][:-1] # Removing % symbol #change here
                        Type = 'bnd'  #change here
                        country = 'HK'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def chinabonds(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = ChinaBondStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = ChinaBondStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.chinabonds()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.chinabonds()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='bnd', country='CH').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = None  #change here
                        change_perc = data[5][:-1] # Removing % symbol #change here
                        Type = 'bnd'  #change here
                        country = 'CH'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def canadabonds(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = CanadaBondStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = CanadaBondStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.canadabonds()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.canadabonds()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='bnd', country='CA').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = None  #change here
                        change_perc = data[5][:-1] # Removing % symbol #change here
                        Type = 'bnd'  #change here
                        country = 'CA'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def germanybonds(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = GermanyBondStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = GermanyBondStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.germanybonds()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.germanybonds()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='bnd', country='GE').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = None  #change here
                        change_perc = data[5][:-1] # Removing % symbol #change here
                        Type = 'bnd'  #change here
                        country = 'GE'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def australiabonds(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = AustraliaBondStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = AustraliaBondStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.australiabonds()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.australiabonds()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='bnd', country='AU').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = None  #change here
                        change_perc = data[5][:-1] # Removing % symbol #change here
                        Type = 'bnd'  #change here
                        country = 'AU'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def usfunds(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = USFundStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = USFundStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.usfunds()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.usfunds()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='fnd', country='US').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = None  #change here
                        change_perc = data[5][:-1] # Removing % symbol #change here
                        Type = 'fnd'  #change here
                        country = 'US'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def japanfunds(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = JapanFundStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = JapanFundStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.japanfunds()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.japanfunds()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='fnd', country='JP').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = None  #change here
                        change_perc = data[5][:-1] # Removing % symbol #change here
                        Type = 'fnd'  #change here
                        country = 'JP'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def ukfunds(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = UKFundStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = UKFundStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.ukfunds()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.ukfunds()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='fnd', country='UK').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = None  #change here
                        change_perc = data[5][:-1] # Removing % symbol #change here
                        Type = 'fnd'  #change here
                        country = 'UK'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def hkfunds(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = HKFundStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = HKFundStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.hkfunds()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.hkfunds()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='fnd', country='HK').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = None  #change here
                        change_perc = data[5][:-1] # Removing % symbol #change here
                        Type = 'fnd'  #change here
                        country = 'HK'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def chinafunds(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = ChinaFundStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = ChinaFundStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.chinafunds()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.chinafunds()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='fnd', country='CH').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = None  #change here
                        change_perc = data[5][:-1] # Removing % symbol #change here
                        Type = 'fnd'  #change here
                        country = 'CH'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def canadafunds(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = CanadaFundStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = CanadaFundStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.canadafunds()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.canadafunds()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='fnd', country='CA').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = None  #change here
                        change_perc = data[5][:-1] # Removing % symbol #change here
                        Type = 'fnd'  #change here
                        country = 'CA'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def germanyfunds(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = GermanyFundStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = GermanyFundStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.germanyfunds()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.germanyfunds()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='fnd', country='GE').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = None  #change here
                        change_perc = data[5][:-1] # Removing % symbol #change here
                        Type = 'fnd'  #change here
                        country = 'GE'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def australiafunds(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = AustraliaFundStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = AustraliaFundStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistoricalMax.australiafunds()') #change here
        if delete.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectAllAssetsHistoricalMax.australiafunds()') #change here
            return ''
        AllAssetsHistoricalMax.objects.filter(Type='fnd', country='AU').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_max(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = None  #change here
                        change_perc = data[5][:-1] # Removing % symbol #change here
                        Type = 'fnd'  #change here
                        country = 'AU'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistoricalMax( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

class CollectAllAssetsHistorical5Y:
# h.CollectAllAssetsHistorical5Y.commodities(delete='n')
# h.CollectAllAssetsHistorical5Y.currencies(delete='n')
# h.CollectAllAssetsHistorical5Y.cryptocurrencies(delete='n')
# h.CollectAllAssetsHistorical5Y.stocks()
# h.CollectAllAssetsHistorical5Y.indices()
# h.CollectAllAssetsHistorical5Y.etfs()
# h.CollectAllAssetsHistorical5Y.bonds()
# h.CollectAllAssetsHistorical5Y.funds()

    def commodities(delete='n'):
        c_list = CommodityStaticInfo.objects.values_list('country', 'short_name', 'link') # returns a list of tuples
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.commodities()')
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.commodities()')
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='cmdty').delete()
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[2]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            driver.get(link)
            sleep(2)
            x = list(c_list).index(i) + 1
            while True:
                try:
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol
                        Type = 'cmdty'
                        country = i[0]
                        short_name = i[1]
                        AllAssetsHistorical5Y(
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    print(f'Stored {x}/{len(c_list)}')
                    x += 1
                    break
                except Exception as e:
                    print_exception(e)
                    print('Waiting for 5 more seconds')
                    sleep(5)
                    continue

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def currencies(delete='n'):
        c_list = CurrencyStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.currencies()') #change here
        if delete.upper() != 'Y':
            
            print('Closing CollectAllAssetsHistorical5Y.currencies()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='crncy').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            driver.get(link)
            x = list(c_list).index(i) + 1
            sleep(2)
            while True:
                try:
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    print(soup.find(id='widgetFieldDateRange').get_text())
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    print(len(soup))
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = None  #change here
                        change_perc = data[5][:-1] # Removing % symbol
                        Type = 'crncy'  #change here
                        country = 'G'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    print(f'Stored {x}/{len(c_list)}')
                    x += 1
                    break
                except Exception as e:
                    print_exception(e)
                    print('Waiting for 5 more seconds')
                    sleep(5)
                    continue
        try:
            # Comment the line that removes all the old data (at the begining of the current function) before using the code below
            # already_saved = AllAssetsHistorical5Y.objects.filter(Type='crptcrncy').values_list('short_name')
            # already_saved = [i[0] for i in already_saved]
            # c_list=remove_already_saved(already_saved, c_list)
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def cryptocurrencies(delete='n'):
        c_list = CryptocurrencyStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = CryptocurrencyStaticInfo.objects.count()
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.cryptocurrencies()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.cryptocurrencies()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='crptcrncy').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            if i[1] == None:
                return
            link = i[1] + '/historical-data' #change here
            driver.get(link)
            x = list(c_list).index(i) + 1
            sleep(2)
            while True:
                try:
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    print(soup.find(id='widgetFieldDateRange').get_text())
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        try:
                            price = validate_price(data[1][:data[1].index('.')+2+1])
                        except:
                            price = validate_price(data[1])
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'crptcrncy'  #change here
                        country = 'G'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, 
                            country=country, 
                            short_name=short_name,
                            date=date, 
                            price=price, 
                            Open=Open,
                            high=high, 
                            low=low, 
                            change_perc=change_perc,
                            volume=volume).save()
                    print(f'Stored {x}/{quanity}: {short_name}')
                    x+=1
                    break
                except Exception as e:
                    print_exception(e)
                    print('Waiting for 5 more seconds')
                    sleep(5)
                    continue
        try:
            # Comment the line that removes all the old data (at the begining of the current function) before using the code below
            # already_saved = AllAssetsHistorical5Y.objects.filter(Type='crptcrncy').values_list('short_name')
            # already_saved = [i[0] for i in already_saved]
            # c_list=remove_already_saved(already_saved, c_list)
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def stocks(delete='n'):
        print('Do you want to delete old records and collect new ones? ')
        if delete.upper() == 'Y':
            print(f'Your answer was "{delete.upper()}. Removing old records..."')
            CollectAllAssetsHistorical5Y.usstocks(delete=delete)
            CollectAllAssetsHistorical5Y.japanstocks(delete=delete)
            CollectAllAssetsHistorical5Y.ukstocks(delete=delete)
            CollectAllAssetsHistorical5Y.hkstocks(delete=delete)
            CollectAllAssetsHistorical5Y.chinastocks(delete=delete)
            CollectAllAssetsHistorical5Y.canadastocks(delete=delete)
            CollectAllAssetsHistorical5Y.germanystocks(delete=delete)
            CollectAllAssetsHistorical5Y.australiastocks(delete=delete)
        else:
            print(f'Closing... Your answer was: {delete}')
   
    def indices(delete='n'):
        print('Do you want to delete old records and collect new ones? ')
        if delete.upper() == 'Y':
            print(f'Your answer was "{delete.upper()}. Removing old records..."')
            CollectAllAssetsHistorical5Y.usindices(delete=delete)
            CollectAllAssetsHistorical5Y.japanindices(delete=delete)
            CollectAllAssetsHistorical5Y.ukindices(delete=delete)
            CollectAllAssetsHistorical5Y.hkindices(delete=delete)
            CollectAllAssetsHistorical5Y.chinaindices(delete=delete)
            CollectAllAssetsHistorical5Y.canadaindices(delete=delete)
            CollectAllAssetsHistorical5Y.germanyindices(delete=delete)
            CollectAllAssetsHistorical5Y.australiaindices(delete=delete)        
        else:
            print(f'Closing... Your answer was: {delete}')

    def etfs(delete='n'):
        print('Do you want to delete old records and collect new ones? ')
        if delete.upper() == 'Y':
            print(f'Your answer was "{delete.upper()}. Removing old records..."')
            CollectAllAssetsHistorical5Y.usetfs(delete=delete)
            CollectAllAssetsHistorical5Y.japanetfs(delete=delete)
            CollectAllAssetsHistorical5Y.uketfs(delete=delete)
            CollectAllAssetsHistorical5Y.hketfs(delete=delete)
            CollectAllAssetsHistorical5Y.chinaetfs(delete=delete)
            CollectAllAssetsHistorical5Y.canadaetfs(delete=delete)
            CollectAllAssetsHistorical5Y.germanyetfs(delete=delete)
            CollectAllAssetsHistorical5Y.australiaetfs(delete=delete)        
        else:
            print(f'Closing... Your answer was: {delete}')

    def bonds(delete='n'):
        print('Do you want to delete old records and collect new ones? ')
        if delete.upper() == 'Y':
            print(f'Your answer was "{delete.upper()}. Removing old records..."')
            CollectAllAssetsHistorical5Y.usbonds(delete=delete)
            CollectAllAssetsHistorical5Y.japanbonds(delete=delete)
            CollectAllAssetsHistorical5Y.ukbonds(delete=delete)
            CollectAllAssetsHistorical5Y.hkbonds(delete=delete)
            CollectAllAssetsHistorical5Y.chinabonds(delete=delete)
            CollectAllAssetsHistorical5Y.canadabonds(delete=delete)
            CollectAllAssetsHistorical5Y.germanybonds(delete=delete)
            CollectAllAssetsHistorical5Y.australiabonds(delete=delete)        
        else:
            print(f'Closing... Your answer was: {delete}')

    def funds(delete='n'):
        print('Do you want to delete old records and collect new ones? ')
        if delete.upper() == 'Y':
            print(f'Your answer was "{delete.upper()}. Removing old records..."')
            CollectAllAssetsHistorical5Y.usfunds(delete=delete)
            CollectAllAssetsHistorical5Y.japanfunds(delete=delete)
            CollectAllAssetsHistorical5Y.ukfunds(delete=delete)
            CollectAllAssetsHistorical5Y.hkfunds(delete=delete)
            CollectAllAssetsHistorical5Y.chinafunds(delete=delete)
            CollectAllAssetsHistorical5Y.canadafunds(delete=delete)
            CollectAllAssetsHistorical5Y.germanyfunds(delete=delete)
            CollectAllAssetsHistorical5Y.australiafunds(delete=delete)        
        else:
            print(f'Closing... Your answer was: {delete}')

    def usstocks(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = USStockStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = USStockStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.usstocks()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.usstocks()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='stck', country='US').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'stck'  #change here
                        country = 'US'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def japanstocks(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = JapanStockStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = JapanStockStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.japanstocks()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.japanstocks()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='stck', country='JP').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'stck'  #change here
                        country = 'JP'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def ukstocks(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = UKStockStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = UKStockStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.ukstocks()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.ukstocks()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='stck', country='UK').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'stck'  #change here
                        country = 'UK'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def hkstocks(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = HKStockStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = HKStockStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.hkstocks()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.hkstocks()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='stck', country='HK').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'stck'  #change here
                        country = 'HK'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def chinastocks(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = ChinaStockStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = ChinaStockStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.chinastocks()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.chinastocks()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='stck', country='CH').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'stck'  #change here
                        country = 'CH'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def canadastocks(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = CanadaStockStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = CanadaStockStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.canadastocks()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.canadastocks()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='stck', country='CA').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'stck'  #change here
                        country = 'CA'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def germanystocks(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = GermanyStockStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = GermanyStockStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.germanystocks()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.germanystocks()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='stck', country='GE').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'stck'  #change here
                        country = 'GE'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def australiastocks(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = AustraliaStockStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = AustraliaStockStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.australiastocks()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.australiastocks()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='stck', country='AU').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'stck'  #change here
                        country = 'AU'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def usindices(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = USIndexStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = USIndexStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.usindices()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.usindices()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='indx', country='US').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'indx'  #change here
                        country = 'US'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def japanindices(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = JapanIndexStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = JapanIndexStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.japanindices()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.japanindices()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='indx', country='JP').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'indx'  #change here
                        country = 'JP'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def ukindices(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = UKIndexStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = UKIndexStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.ukindices()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.ukindices()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='indx', country='UK').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'indx'  #change here
                        country = 'UK'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')        

    def hkindices(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = HKIndexStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = HKIndexStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.hkindices()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.hkindices()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='indx', country='HK').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'indx'  #change here
                        country = 'HK'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def chinaindices(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = ChinaIndexStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = ChinaIndexStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.chinaindices()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.chinaindices()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='indx', country='CH').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'indx'  #change here
                        country = 'CH'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')        

    def canadaindices(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = CanadaIndexStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = CanadaIndexStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.canadaindices()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.canadaindices()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='indx', country='CA').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'indx'  #change here
                        country = 'CA'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')            

    def germanyindices(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = GermanyIndexStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = GermanyIndexStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.germanyindices()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.germanyindices()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='indx', country='GE').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'indx'  #change here
                        country = 'GE'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')     

    def australiaindices(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = AustraliaIndexStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = AustraliaIndexStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.australiaindices()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.australiaindices()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='indx', country='AU').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'indx'  #change here
                        country = 'AU'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')           

    def usetfs(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = USETFStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = USETFStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.usetfs()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.usetfs()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='etf', country='US').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'etf'  #change here
                        country = 'US'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')     

    def japanetfs(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = JapanETFStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = JapanETFStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.japanetfs()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.japanetfs()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='etf', country='JP').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'etf'  #change here
                        country = 'JP'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')   

    def uketfs(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = UKETFStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = UKETFStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.uketfs()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.uketfs()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='etf', country='UK').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'etf'  #change here
                        country = 'UK'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')   

    def hketfs(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = HKETFStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = HKETFStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.hketfs()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.hketfs()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='etf', country='HK').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'etf'  #change here
                        country = 'HK'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')   

    def chinaetfs(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = ChinaETFStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = ChinaETFStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.chinaetfs()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.chinaetfs()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='etf', country='CH').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'etf'  #change here
                        country = 'CH'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')     

    def canadaetfs(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = CanadaETFStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = CanadaETFStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.canadaetfs()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.canadaetfs()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='etf', country='CA').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'etf'  #change here
                        country = 'CA'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')         

    def germanyetfs(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = GermanyETFStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = GermanyETFStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.germanyetfs()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.germanyetfs()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='etf', country='GE').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'etf'  #change here
                        country = 'GE'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')     

    def australiaetfs(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = AustraliaETFStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = AustraliaETFStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.australiaetfs()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.australiaetfs()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='etf', country='AU').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = validate_price(data[5])  #change here
                        change_perc = validate_price(data[6][:-1]) # Removing % symbol #change here
                        Type = 'etf'  #change here
                        country = 'AU'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')                  

    def usbonds(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = USBondStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = USBondStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.usbonds()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.usbonds()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='bnd', country='US').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = None  #change here
                        change_perc = data[5][:-1] # Removing % symbol #change here
                        Type = 'bnd'  #change here
                        country = 'US'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def japanbonds(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = JapanBondStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = JapanBondStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.japanbonds()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.japanbonds()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='bnd', country='JP').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = None  #change here
                        change_perc = data[5][:-1] # Removing % symbol #change here
                        Type = 'bnd'  #change here
                        country = 'JP'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def ukbonds(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = UKBondStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = UKBondStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.ukbonds()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.ukbonds()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='bnd', country='UK').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = None  #change here
                        change_perc = data[5][:-1] # Removing % symbol #change here
                        Type = 'bnd'  #change here
                        country = 'UK'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def hkbonds(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = HKBondStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = HKBondStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.hkbonds()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.hkbonds()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='bnd', country='HK').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = None  #change here
                        change_perc = data[5][:-1] # Removing % symbol #change here
                        Type = 'bnd'  #change here
                        country = 'HK'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def chinabonds(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = ChinaBondStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = ChinaBondStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.chinabonds()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.chinabonds()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='bnd', country='CH').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = None  #change here
                        change_perc = data[5][:-1] # Removing % symbol #change here
                        Type = 'bnd'  #change here
                        country = 'CH'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def canadabonds(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = CanadaBondStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = CanadaBondStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.canadabonds()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.canadabonds()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='bnd', country='CA').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = None  #change here
                        change_perc = data[5][:-1] # Removing % symbol #change here
                        Type = 'bnd'  #change here
                        country = 'CA'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def germanybonds(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = GermanyBondStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = GermanyBondStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.germanybonds()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.germanybonds()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='bnd', country='GE').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = None  #change here
                        change_perc = data[5][:-1] # Removing % symbol #change here
                        Type = 'bnd'  #change here
                        country = 'GE'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def australiabonds(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = AustraliaBondStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = AustraliaBondStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.australiabonds()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.australiabonds()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='bnd', country='AU').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = None  #change here
                        change_perc = data[5][:-1] # Removing % symbol #change here
                        Type = 'bnd'  #change here
                        country = 'AU'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def usfunds(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = USFundStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = USFundStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.usfunds()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.usfunds()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='fnd', country='US').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = None  #change here
                        change_perc = data[5][:-1] # Removing % symbol #change here
                        Type = 'fnd'  #change here
                        country = 'US'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def japanfunds(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = JapanFundStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = JapanFundStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.japanfunds()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.japanfunds()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='fnd', country='JP').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = None  #change here
                        change_perc = data[5][:-1] # Removing % symbol #change here
                        Type = 'fnd'  #change here
                        country = 'JP'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def ukfunds(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = UKFundStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = UKFundStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.ukfunds()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.ukfunds()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='fnd', country='UK').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = None  #change here
                        change_perc = data[5][:-1] # Removing % symbol #change here
                        Type = 'fnd'  #change here
                        country = 'UK'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def hkfunds(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = HKFundStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = HKFundStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.hkfunds()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.hkfunds()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='fnd', country='HK').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = None  #change here
                        change_perc = data[5][:-1] # Removing % symbol #change here
                        Type = 'fnd'  #change here
                        country = 'HK'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def chinafunds(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = ChinaFundStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = ChinaFundStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.chinafunds()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.chinafunds()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='fnd', country='CH').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = None  #change here
                        change_perc = data[5][:-1] # Removing % symbol #change here
                        Type = 'fnd'  #change here
                        country = 'CH'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def canadafunds(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = CanadaFundStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = CanadaFundStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.canadafunds()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.canadafunds()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='fnd', country='CA').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = None  #change here
                        change_perc = data[5][:-1] # Removing % symbol #change here
                        Type = 'fnd'  #change here
                        country = 'CA'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def germanyfunds(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = GermanyFundStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = GermanyFundStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.germanyfunds()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.germanyfunds()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='fnd', country='GE').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = None  #change here
                        change_perc = data[5][:-1] # Removing % symbol #change here
                        Type = 'fnd'  #change here
                        country = 'GE'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def australiafunds(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = AustraliaFundStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = AustraliaFundStaticInfo.objects.count() #change here
        driver = vps_selenium_setup()
        print('Starting CollectAllAssetsHistorical5Y.australiafunds()') #change here
        if delete.upper() != 'Y':
            print('Closing CollectAllAssetsHistorical5Y.australiafunds()') #change here
            return ''
        print('Removing old records')
        AllAssetsHistorical5Y.objects.filter(Type='fnd', country='AU').delete() #change here
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        # driver = webdriver.Chrome()
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            driver.get(link)
            sleep(5)
            while True:
                try: 
                    print(link)
                    execute_js_scripts_5y(driver)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    if soup[0].td.get_text() == 'No results found':
                        print('No results found')
                        break
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                        price = validate_price(data[1])
                        price = price[:price.index('.')+2+1]
                        Open = validate_price(data[2])
                        high = validate_price(data[3])
                        low = validate_price(data[4])
                        volume = None  #change here
                        change_perc = data[5][:-1] # Removing % symbol #change here
                        Type = 'fnd'  #change here
                        country = 'AU'  #change here
                        short_name = i[0]  #change here
                        AllAssetsHistorical5Y( 
                            Type=Type, country=country, short_name=short_name,
                            date=date, price=price, Open=Open,
                            high=high, low=low, change_perc=change_perc,
                            volume=volume).save()
                    break
                except Exception as e:
                    print_exception(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        try:
            threads_by_chunks(target=work, c_list=c_list, n=3)

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')      


class CollectAllAssetsHistorical1Y1M:
    from .live_scraper import STATIC_OBJECTS
    driver = vps_selenium_setup()
    print('Driver is ready!')
    def collect1y1m(driver, dct):
        """takes dct(STATIC_OBJECT's part or all of it) collect historical data"""
        data_ages = ['1m', '3m', '6m', '1y']
        for key, value in dct.items():
            print(f'Started collectallassets1y1m {key}')
            if value['type_'] == 'crptcrncy':
                hist_link = '/historical-data'
            else:
                hist_link = '-historical-data'

            obj_list = value['object_'].objects.values_list('short_name', 'link')
            quanity = len(obj_list)

            for obj in obj_list:
                link = obj[1]
                if '?cid' in link:
                    cid = link[link.index('?cid'):]
                    link = link[:link.index('?cid')]
                    link += hist_link + cid
                else:
                    link += hist_link
                x = list(obj_list).index(obj)+1
                driver.get(link)
                while True:
                    try: 
                        print(link)
                        soup = BeautifulSoup(driver.page_source, 'html.parser')
                        table = soup.find(class_=value['table class'])
                        trs = table.tbody.find_all('tr')
                        if trs[0].td.get_text() == 'No results found':
                            print('No results found')
                            break
                        for data_age in data_ages:
                            execute_js_scripts_1y1m(driver, data_age)
                        
                            while len(trs) < quanity:
                                try:
                                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                                    table = soup.find(class_=value['table class'])
                                    trs = table.tbody.find_all('tr')
                                except Exception as e:
                                    print_exception(e)
                                    sleep(1)
                            
                            for row in trs:
                                data = row.find_all('td')
                                data = [d.get_text() for d in data]
                                date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                                price = validate_price(data[1])
                                price = price[:price.index('.')+2+1]
                                Open = validate_price(data[2])
                                high = validate_price(data[3])
                                low = validate_price(data[4])
                                if value['type_'] in 'crncybndfnd':
                                    volume = None  #change here
                                    change_perc = data[5][:-1] # Removing % symbol #change here
                                else:
                                    volume = data[5]
                                    if volume == '-':
                                        volume = None
                                    change_perc = data[6][:-1] # Removing % symbol #change here
                                Type = value['type_']  #change here
                                if Type in 'crncycrptcrncy':
                                    country = 'G'
                                else:
                                    country = value['object_'].objects.filter(link=obj[1]).first().country  #change here
                                short_name = obj[0]  #change here
                                AllAssetsHistorical5Y( 
                                    Type=Type, country=country, short_name=short_name,
                                    date=date, price=price, Open=Open,
                                    high=high, low=low, change_perc=change_perc,
                                    volume=volume).save()
                        break
                    except Exception as e:
                        print_exception(e)
                        sleep(1)
                        pass 