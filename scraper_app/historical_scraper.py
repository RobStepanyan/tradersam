import requests, os, datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
from threading import Thread
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
    AllAssetsHistoricalMax,
)

class CollectAllAssetsHistoricalMax:
# CollectAllAssetsHistoricalMax.commodities(delete='n')
# CollectAllAssetsHistoricalMax.currencies(delete='n')
# CollectAllAssetsHistoricalMax.cryptocurrencies(delete='n')
# CollectAllAssetsHistoricalMax.stocks(delete='n')

    def commodities(delete='n'):
        c_list = CommodityStaticInfo.objects.values_list('country', 'short_name', 'link') # returns a list of tuples
        #--------------------VPS------------------
        display = Display(visible=0, size=(1000, 1000))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        try:
            print('Starting CollectAllAssetsHistoricalMax.commodities()')
            if delete.upper() != 'Y':
                print('Removing old records')
                print('Closing CollectAllAssetsHistoricalMax.commodities()')
                return ''
            AllAssetsHistoricalMax.objects.filter(Type='cmdty').delete()
            print('Old records have been removed')
            print('Starting to collect new ones')
            print('Starting Selenium')
            # driver = webdriver.Chrome()
            for i in c_list:
                link = i[2] + '-historical-data'
                driver.get(link)
                print('Executing JS scripts')
                driver.execute_script('$("#data_interval").val("Monthly");')
                driver.find_element_by_id('data_interval').value = "Monthly"
                driver.find_element_by_id('widgetFieldDateRange').click()
                driver.find_element_by_id('startDate').clear()
                driver.find_element_by_id('startDate').send_keys('01/01/1980', Keys.ENTER)
                print('Executed JS scripts, sleeping for 5 seconds')
                sleep(5)
                print(link)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                print(soup.find(id='widgetFieldDateRange'))
                soup = soup.find(class_='genTbl closedTbl historicalTbl')
                soup = soup.tbody.find_all('tr')
                print(len(soup))
                for row in soup:
                    data = row.find_all('td')
                    data = [d.get_text() for d in data]
                    date = datetime.datetime.strptime(data[0], '%b %y')
                    price = data[1]
                    Open = data[2]
                    high = data[3]
                    low = data[4]
                    volume = data[5]
                    change_perc = data[6][:-1] # Removing % symbol
                    Type = 'cmdty'
                    country = i[0]
                    short_name = i[1]
                    AllAssetsHistoricalMax(
                        Type=Type, country=country, short_name=short_name,
                        date=date, price=price, Open=Open,
                        high=high, low=low, change_perc=change_perc,
                        volume=volume).save()

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def currencies(delete='n'):
        c_list = CurrencyStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        #--------------------VPS------------------
        display = Display(visible=0, size=(1000, 1000))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        try:
            print('Starting CollectAllAssetsHistoricalMax.currencies()') #change here
            if delete.upper() != 'Y':
                print('Removing old records')
                print('Closing CollectAllAssetsHistoricalMax.currencies()') #change here
                return ''
            AllAssetsHistoricalMax.objects.filter(Type='crncy').delete() #change here
            print('Old records have been removed')
            print('Starting to collect new ones')
            print('Starting Selenium')
            # driver = webdriver.Chrome()
            for i in c_list:
                link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
                driver.get(link)
                print('Executing JS scripts')
                driver.execute_script('$("#data_interval").val("Monthly");')
                driver.find_element_by_id('data_interval').value = "Monthly"
                driver.find_element_by_id('widgetFieldDateRange').click()
                driver.find_element_by_id('startDate').clear()
                driver.find_element_by_id('startDate').send_keys('01/01/1980', Keys.ENTER)
                print('Executed JS scripts, sleeping for 5 seconds')
                sleep(5)
                print(link)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                print(soup.find(id='widgetFieldDateRange'))
                soup = soup.find(class_='genTbl closedTbl historicalTbl')
                soup = soup.tbody.find_all('tr')
                print(len(soup))
                for row in soup:
                    data = row.find_all('td')
                    data = [d.get_text() for d in data]
                    date = datetime.datetime.strptime(data[0], '%b %y')
                    price = data[1]
                    Open = data[2]
                    high = data[3]
                    low = data[4]
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

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def cryptocurrencies(delete='n'):
        c_list = USStockStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = USStockStaticInfo.objects.count()
        #--------------------VPS------------------
        display = Display(visible=0, size=(1000, 1000))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        try:
            print('Starting CollectAllAssetsHistoricalMax.cryptocurrencies()') #change here
            if delete.upper() != 'Y':
                print('Removing old records')
                print('Closing CollectAllAssetsHistoricalMax.cryptocurrencies()') #change here
                return ''
            AllAssetsHistoricalMax.objects.filter(Type='crptcrncy').delete() #change here
            print('Old records have been removed')
            print('Starting to collect new ones')
            print('Starting Selenium')
            # driver = webdriver.Chrome()
            x = 1
            for i in c_list:
                link = i[1] + '/historical-data' #change here
                driver.get(link)
                print('Executing JS scripts')
                driver.execute_script('$("#data_interval").val("Monthly");')
                driver.find_element_by_id('data_interval').value = "Monthly"
                driver.find_element_by_id('widgetFieldDateRange').click()
                driver.find_element_by_id('startDate').clear()
                driver.find_element_by_id('startDate').send_keys('01/01/1980', Keys.ENTER)
                print('Executed JS scripts, sleeping for 5 seconds')
                sleep(5)
                print(link)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                print(soup.find(id='widgetFieldDateRange'))
                soup = soup.find(class_='genTbl closedTbl historicalTbl')
                soup = soup.tbody.find_all('tr')
                for row in soup:
                    data = row.find_all('td')
                    data = [d.get_text() for d in data]
                    date = datetime.datetime.strptime(data[0], '%b %y')
                    price = data[1][:data.index('.')+2+1]
                    Open = data[2]
                    high = data[3]
                    low = data[4]
                    volume = data[5]  #change here
                    change_perc = data[6][:-1] # Removing % symbol #change here
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
        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def stocks(delete='n'):
        # CollectAllAssetsHistoricalMax.usstocks(delete=delete)
        # CollectAllAssetsHistoricalMax.japanstocks(delete=delete)
        # CollectAllAssetsHistoricalMax.ukstocks(delete=delete)
        CollectAllAssetsHistoricalMax.hkstocks(delete=delete)
        CollectAllAssetsHistoricalMax.chinastocks(delete=delete)
        CollectAllAssetsHistoricalMax.canadastocks(delete=delete)
        CollectAllAssetsHistoricalMax.germanystocks(delete=delete)
        CollectAllAssetsHistoricalMax.australiastocks(delete=delete)

    def indices(delete='n'):
        CollectAllAssetsHistoricalMax.usindices(delete=delete)
        CollectAllAssetsHistoricalMax.japanindices(delete=delete)
        CollectAllAssetsHistoricalMax.ukindices(delete=delete)
        CollectAllAssetsHistoricalMax.hkindices(delete=delete)
        CollectAllAssetsHistoricalMax.chinaindices(delete=delete)
        CollectAllAssetsHistoricalMax.canadaindices(delete=delete)
        CollectAllAssetsHistoricalMax.germanyindices(delete=delete)
        CollectAllAssetsHistoricalMax.australiaindices(delete=delete)        


    def usstocks(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = USStockStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = USStockStaticInfo.objects.count() #change here
        #--------------------VPS------------------
        display = Display(visible=0, size=(1000, 1000))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
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
        def chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n):
                yield lst[i:i + n]
        
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            print(link)
            while True:
                try: 
                    driver.get(link)
                    sleep(5)
                    print('Executing JS scripts')
                    driver.execute_script('$("#data_interval").val("Monthly");')
                    driver.find_element_by_id('data_interval').value = "Monthly"
                    driver.find_element_by_id('widgetFieldDateRange').click()
                    driver.find_element_by_id('startDate').clear()
                    driver.find_element_by_id('startDate').send_keys('01/01/1980', Keys.ENTER)
                    print('Executed JS scripts')
                    sleep(6)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = data[1]
                        price = price[:price.index('.')+2+1]
                        Open = data[2]
                        high = data[3]
                        low = data[4]
                        volume = data[5]  #change here
                        change_perc = data[6][:-1] # Removing % symbol #change here
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
                    print(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        chunk_list = list(chunks(range(quanity), 3))
        try:
            # Code below creates threads for each item, then executes them by chunks
            threads = []
            for i in range(quanity):
                threads.append(Thread(target=work, args=(c_list[i],)))
            print('Threads are ready')
            chunk_n = 1
            chunk_all = len(chunk_list)
            for l in chunk_list:
                for sub_l in l:
                    threads[sub_l].start()
                    sleep(1)
                for sub_l in l:
                    threads[sub_l].join()
                
                print(f'Executed Chunk {chunk_n}/{chunk_all}')
                chunk_n += 1

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def japanstocks(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = JapanStockStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = JapanStockStaticInfo.objects.count() #change here
        #--------------------VPS------------------
        display = Display(visible=0, size=(1000, 1000))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
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
        def chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n):
                yield lst[i:i + n]
        
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            print(link)
            while True:
                try: 
                    driver.get(link)
                    sleep(5)
                    print('Executing JS scripts')
                    driver.execute_script('$("#data_interval").val("Monthly");')
                    driver.find_element_by_id('data_interval').value = "Monthly"
                    driver.find_element_by_id('widgetFieldDateRange').click()
                    driver.find_element_by_id('startDate').clear()
                    driver.find_element_by_id('startDate').send_keys('01/01/1980', Keys.ENTER)
                    print('Executed JS scripts')
                    sleep(6)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = data[1]
                        price = price[:price.index('.')+2+1]
                        Open = data[2]
                        high = data[3]
                        low = data[4]
                        volume = data[5]  #change here
                        change_perc = data[6][:-1] # Removing % symbol #change here
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
                    print(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        chunk_list = list(chunks(range(quanity), 3))
        try:
            # Code below creates threads for each item, then executes them by chunks
            threads = []
            for i in range(quanity):
                threads.append(Thread(target=work, args=(c_list[i],)))
            print('Threads are ready')
            chunk_n = 1
            chunk_all = len(chunk_list)
            for l in chunk_list:
                for sub_l in l:
                    threads[sub_l].start()
                    sleep(1)
                for sub_l in l:
                    threads[sub_l].join()
                
                print(f'Executed Chunk {chunk_n}/{chunk_all}')
                chunk_n += 1

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def ukstocks(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = UKStockStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = UKStockStaticInfo.objects.count() #change here
        #--------------------VPS------------------
        display = Display(visible=0, size=(1000, 1000))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
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
        def chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n):
                yield lst[i:i + n]
        
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            print(link)
            while True:
                try: 
                    driver.get(link)
                    sleep(5)
                    print('Executing JS scripts')
                    driver.execute_script('$("#data_interval").val("Monthly");')
                    driver.find_element_by_id('data_interval').value = "Monthly"
                    driver.find_element_by_id('widgetFieldDateRange').click()
                    driver.find_element_by_id('startDate').clear()
                    driver.find_element_by_id('startDate').send_keys('01/01/1980', Keys.ENTER)
                    print('Executed JS scripts')
                    sleep(6)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = data[1]
                        price = price[:price.index('.')+2+1]
                        Open = data[2]
                        high = data[3]
                        low = data[4]
                        volume = data[5]  #change here
                        change_perc = data[6][:-1] # Removing % symbol #change here
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
                    print(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        chunk_list = list(chunks(range(quanity), 3))
        try:
            # Code below creates threads for each item, then executes them by chunks
            threads = []
            for i in range(quanity):
                threads.append(Thread(target=work, args=(c_list[i],)))
            print('Threads are ready')
            chunk_n = 1
            chunk_all = len(chunk_list)
            for l in chunk_list:
                for sub_l in l:
                    threads[sub_l].start()
                    sleep(1)
                for sub_l in l:
                    threads[sub_l].join()
                
                print(f'Executed Chunk {chunk_n}/{chunk_all}')
                chunk_n += 1

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def hkstocks(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = HKStockStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = HKStockStaticInfo.objects.count() #change here
        #--------------------VPS------------------
        display = Display(visible=0, size=(1000, 1000))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
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
        def chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n):
                yield lst[i:i + n]
        
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            print(link)
            while True:
                try: 
                    driver.get(link)
                    sleep(5)
                    print('Executing JS scripts')
                    driver.execute_script('$("#data_interval").val("Monthly");')
                    driver.find_element_by_id('data_interval').value = "Monthly"
                    driver.find_element_by_id('widgetFieldDateRange').click()
                    driver.find_element_by_id('startDate').clear()
                    driver.find_element_by_id('startDate').send_keys('01/01/1980', Keys.ENTER)
                    print('Executed JS scripts')
                    sleep(6)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = data[1]
                        price = price[:price.index('.')+2+1]
                        Open = data[2]
                        high = data[3]
                        low = data[4]
                        volume = data[5]  #change here
                        change_perc = data[6][:-1] # Removing % symbol #change here
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
                    print(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        chunk_list = list(chunks(range(quanity), 3))
        try:
            # Code below creates threads for each item, then executes them by chunks
            threads = []
            for i in range(quanity):
                threads.append(Thread(target=work, args=(c_list[i],)))
            print('Threads are ready')
            chunk_n = 1
            chunk_all = len(chunk_list)
            for l in chunk_list:
                for sub_l in l:
                    threads[sub_l].start()
                    sleep(1)
                for sub_l in l:
                    threads[sub_l].join()
                
                print(f'Executed Chunk {chunk_n}/{chunk_all}')
                chunk_n += 1

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')
    
    def chinastocks(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = USStockStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = USStockStaticInfo.objects.count() #change here
        #--------------------VPS------------------
        display = Display(visible=0, size=(1000, 1000))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
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
        def chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n):
                yield lst[i:i + n]
        
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            print(link)
            while True:
                try: 
                    driver.get(link)
                    sleep(5)
                    print('Executing JS scripts')
                    driver.execute_script('$("#data_interval").val("Monthly");')
                    driver.find_element_by_id('data_interval').value = "Monthly"
                    driver.find_element_by_id('widgetFieldDateRange').click()
                    driver.find_element_by_id('startDate').clear()
                    driver.find_element_by_id('startDate').send_keys('01/01/1980', Keys.ENTER)
                    print('Executed JS scripts')
                    sleep(6)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = data[1]
                        price = price[:price.index('.')+2+1]
                        Open = data[2]
                        high = data[3]
                        low = data[4]
                        volume = data[5]  #change here
                        change_perc = data[6][:-1] # Removing % symbol #change here
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
                    print(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        chunk_list = list(chunks(range(quanity), 3))
        try:
            # Code below creates threads for each item, then executes them by chunks
            threads = []
            for i in range(quanity):
                threads.append(Thread(target=work, args=(c_list[i],)))
            print('Threads are ready')
            chunk_n = 1
            chunk_all = len(chunk_list)
            for l in chunk_list:
                for sub_l in l:
                    threads[sub_l].start()
                    sleep(1)
                for sub_l in l:
                    threads[sub_l].join()
                
                print(f'Executed Chunk {chunk_n}/{chunk_all}')
                chunk_n += 1

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def canadastocks(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = CanadaStockStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = CanadaStockStaticInfo.objects.count() #change here
        #--------------------VPS------------------
        display = Display(visible=0, size=(1000, 1000))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
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
        def chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n):
                yield lst[i:i + n]
        
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            print(link)
            while True:
                try: 
                    driver.get(link)
                    sleep(5)
                    print('Executing JS scripts')
                    driver.execute_script('$("#data_interval").val("Monthly");')
                    driver.find_element_by_id('data_interval').value = "Monthly"
                    driver.find_element_by_id('widgetFieldDateRange').click()
                    driver.find_element_by_id('startDate').clear()
                    driver.find_element_by_id('startDate').send_keys('01/01/1980', Keys.ENTER)
                    print('Executed JS scripts')
                    sleep(6)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = data[1]
                        price = price[:price.index('.')+2+1]
                        Open = data[2]
                        high = data[3]
                        low = data[4]
                        volume = data[5]  #change here
                        change_perc = data[6][:-1] # Removing % symbol #change here
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
                    print(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        chunk_list = list(chunks(range(quanity), 3))
        try:
            # Code below creates threads for each item, then executes them by chunks
            threads = []
            for i in range(quanity):
                threads.append(Thread(target=work, args=(c_list[i],)))
            print('Threads are ready')
            chunk_n = 1
            chunk_all = len(chunk_list)
            for l in chunk_list:
                for sub_l in l:
                    threads[sub_l].start()
                    sleep(1)
                for sub_l in l:
                    threads[sub_l].join()
                
                print(f'Executed Chunk {chunk_n}/{chunk_all}')
                chunk_n += 1

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def germanystocks(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = GermanyStockStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = GermanyStockStaticInfo.objects.count() #change here
        #--------------------VPS------------------
        display = Display(visible=0, size=(1000, 1000))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
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
        def chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n):
                yield lst[i:i + n]
        
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            print(link)
            while True:
                try: 
                    driver.get(link)
                    sleep(5)
                    print('Executing JS scripts')
                    driver.execute_script('$("#data_interval").val("Monthly");')
                    driver.find_element_by_id('data_interval').value = "Monthly"
                    driver.find_element_by_id('widgetFieldDateRange').click()
                    driver.find_element_by_id('startDate').clear()
                    driver.find_element_by_id('startDate').send_keys('01/01/1980', Keys.ENTER)
                    print('Executed JS scripts')
                    sleep(6)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = data[1]
                        price = price[:price.index('.')+2+1]
                        Open = data[2]
                        high = data[3]
                        low = data[4]
                        volume = data[5]  #change here
                        change_perc = data[6][:-1] # Removing % symbol #change here
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
                    print(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        chunk_list = list(chunks(range(quanity), 3))
        try:
            # Code below creates threads for each item, then executes them by chunks
            threads = []
            for i in range(quanity):
                threads.append(Thread(target=work, args=(c_list[i],)))
            print('Threads are ready')
            chunk_n = 1
            chunk_all = len(chunk_list)
            for l in chunk_list:
                for sub_l in l:
                    threads[sub_l].start()
                    sleep(1)
                for sub_l in l:
                    threads[sub_l].join()
                
                print(f'Executed Chunk {chunk_n}/{chunk_all}')
                chunk_n += 1

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def australiastocks(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = AustraliaStockStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = AustraliaStockStaticInfo.objects.count() #change here
        #--------------------VPS------------------
        display = Display(visible=0, size=(1000, 1000))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
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
        def chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n):
                yield lst[i:i + n]
        
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            print(link)
            while True:
                try: 
                    driver.get(link)
                    sleep(5)
                    print('Executing JS scripts')
                    driver.execute_script('$("#data_interval").val("Monthly");')
                    driver.find_element_by_id('data_interval').value = "Monthly"
                    driver.find_element_by_id('widgetFieldDateRange').click()
                    driver.find_element_by_id('startDate').clear()
                    driver.find_element_by_id('startDate').send_keys('01/01/1980', Keys.ENTER)
                    print('Executed JS scripts')
                    sleep(6)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = data[1]
                        price = price[:price.index('.')+2+1]
                        Open = data[2]
                        high = data[3]
                        low = data[4]
                        volume = data[5]  #change here
                        change_perc = data[6][:-1] # Removing % symbol #change here
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
                    print(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        chunk_list = list(chunks(range(quanity), 3))
        try:
            # Code below creates threads for each item, then executes them by chunks
            threads = []
            for i in range(quanity):
                threads.append(Thread(target=work, args=(c_list[i],)))
            print('Threads are ready')
            chunk_n = 1
            chunk_all = len(chunk_list)
            for l in chunk_list:
                for sub_l in l:
                    threads[sub_l].start()
                    sleep(1)
                for sub_l in l:
                    threads[sub_l].join()
                
                print(f'Executed Chunk {chunk_n}/{chunk_all}')
                chunk_n += 1

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def usindices(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = USIndexStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = USIndexStaticInfo.objects.count() #change here
        #--------------------VPS------------------
        display = Display(visible=0, size=(1000, 1000))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
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
        def chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n):
                yield lst[i:i + n]
        
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            print(link)
            while True:
                try: 
                    driver.get(link)
                    sleep(5)
                    print('Executing JS scripts')
                    driver.execute_script('$("#data_interval").val("Monthly");')
                    driver.find_element_by_id('data_interval').value = "Monthly"
                    driver.find_element_by_id('widgetFieldDateRange').click()
                    driver.find_element_by_id('startDate').clear()
                    driver.find_element_by_id('startDate').send_keys('01/01/1980', Keys.ENTER)
                    print('Executed JS scripts')
                    sleep(6)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = data[1]
                        price = price[:price.index('.')+2+1]
                        Open = data[2]
                        high = data[3]
                        low = data[4]
                        volume = data[5]  #change here
                        if volume == '-':
                            volume = None
                        change_perc = data[6][:-1] # Removing % symbol #change here
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
                    print(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        chunk_list = list(chunks(range(quanity), 3))
        try:
            # Code below creates threads for each item, then executes them by chunks
            threads = []
            for i in range(quanity):
                threads.append(Thread(target=work, args=(c_list[i],)))
            print('Threads are ready')
            chunk_n = 1
            chunk_all = len(chunk_list)
            for l in chunk_list:
                for sub_l in l:
                    threads[sub_l].start()
                    sleep(1)
                for sub_l in l:
                    threads[sub_l].join()
                
                print(f'Executed Chunk {chunk_n}/{chunk_all}')
                chunk_n += 1

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly') 

    def japanindices(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = JapanIndexStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = JapanIndexStaticInfo.objects.count() #change here
        #--------------------VPS------------------
        display = Display(visible=0, size=(1000, 1000))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
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
        def chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n):
                yield lst[i:i + n]
        
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            print(link)
            while True:
                try: 
                    driver.get(link)
                    sleep(5)
                    print('Executing JS scripts')
                    driver.execute_script('$("#data_interval").val("Monthly");')
                    driver.find_element_by_id('data_interval').value = "Monthly"
                    driver.find_element_by_id('widgetFieldDateRange').click()
                    driver.find_element_by_id('startDate').clear()
                    driver.find_element_by_id('startDate').send_keys('01/01/1980', Keys.ENTER)
                    print('Executed JS scripts')
                    sleep(6)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = data[1]
                        price = price[:price.index('.')+2+1]
                        Open = data[2]
                        high = data[3]
                        low = data[4]
                        volume = data[5]  #change here
                        if volume == '-':
                            volume = None
                        change_perc = data[6][:-1] # Removing % symbol #change here
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
                    print(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        chunk_list = list(chunks(range(quanity), 3))
        try:
            # Code below creates threads for each item, then executes them by chunks
            threads = []
            for i in range(quanity):
                threads.append(Thread(target=work, args=(c_list[i],)))
            print('Threads are ready')
            chunk_n = 1
            chunk_all = len(chunk_list)
            for l in chunk_list:
                for sub_l in l:
                    threads[sub_l].start()
                    sleep(1)
                for sub_l in l:
                    threads[sub_l].join()
                
                print(f'Executed Chunk {chunk_n}/{chunk_all}')
                chunk_n += 1

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')   

    def ukindices(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = UKIndexStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = UKIndexStaticInfo.objects.count() #change here
        #--------------------VPS------------------
        display = Display(visible=0, size=(1000, 1000))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
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
        def chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n):
                yield lst[i:i + n]
        
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            print(link)
            while True:
                try: 
                    driver.get(link)
                    sleep(5)
                    print('Executing JS scripts')
                    driver.execute_script('$("#data_interval").val("Monthly");')
                    driver.find_element_by_id('data_interval').value = "Monthly"
                    driver.find_element_by_id('widgetFieldDateRange').click()
                    driver.find_element_by_id('startDate').clear()
                    driver.find_element_by_id('startDate').send_keys('01/01/1980', Keys.ENTER)
                    print('Executed JS scripts')
                    sleep(6)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = data[1]
                        price = price[:price.index('.')+2+1]
                        Open = data[2]
                        high = data[3]
                        low = data[4]
                        volume = data[5]  #change here
                        if volume == '-':
                            volume = None
                        change_perc = data[6][:-1] # Removing % symbol #change here
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
                    print(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        chunk_list = list(chunks(range(885, quanity), 3))
        try:
            # Code below creates threads for each item, then executes them by chunks
            threads = []
            for i in range(quanity):
                threads.append(Thread(target=work, args=(c_list[i],)))
            print('Threads are ready')
            chunk_n = 1
            chunk_all = len(chunk_list)
            for l in chunk_list:
                for sub_l in l:
                    threads[sub_l].start()
                    sleep(1)
                for sub_l in l:
                    threads[sub_l].join()
                
                print(f'Executed Chunk {chunk_n}/{chunk_all}')
                chunk_n += 1

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')       

    def hkindices(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = HKIndexStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = HKIndexStaticInfo.objects.count() #change here
        #--------------------VPS------------------
        display = Display(visible=0, size=(1000, 1000))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
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
        def chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n):
                yield lst[i:i + n]
        
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            print(link)
            while True:
                try: 
                    driver.get(link)
                    sleep(5)
                    print('Executing JS scripts')
                    driver.execute_script('$("#data_interval").val("Monthly");')
                    driver.find_element_by_id('data_interval').value = "Monthly"
                    driver.find_element_by_id('widgetFieldDateRange').click()
                    driver.find_element_by_id('startDate').clear()
                    driver.find_element_by_id('startDate').send_keys('01/01/1980', Keys.ENTER)
                    print('Executed JS scripts')
                    sleep(6)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = data[1]
                        price = price[:price.index('.')+2+1]
                        Open = data[2]
                        high = data[3]
                        low = data[4]
                        volume = data[5]  #change here
                        if volume == '-':
                            volume = None
                        change_perc = data[6][:-1] # Removing % symbol #change here
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
                    print(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        chunk_list = list(chunks(range(quanity), 3))
        try:
            # Code below creates threads for each item, then executes them by chunks
            threads = []
            for i in range(quanity):
                threads.append(Thread(target=work, args=(c_list[i],)))
            print('Threads are ready')
            chunk_n = 1
            chunk_all = len(chunk_list)
            for l in chunk_list:
                for sub_l in l:
                    threads[sub_l].start()
                    sleep(1)
                for sub_l in l:
                    threads[sub_l].join()
                
                print(f'Executed Chunk {chunk_n}/{chunk_all}')
                chunk_n += 1

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly') 

    def chinaindices(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = ChinaIndexStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = ChinaIndexStaticInfo.objects.count() #change here
        #--------------------VPS------------------
        display = Display(visible=0, size=(1000, 1000))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
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
        def chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n):
                yield lst[i:i + n]
        
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            print(link)
            while True:
                try: 
                    driver.get(link)
                    sleep(5)
                    print('Executing JS scripts')
                    driver.execute_script('$("#data_interval").val("Monthly");')
                    driver.find_element_by_id('data_interval').value = "Monthly"
                    driver.find_element_by_id('widgetFieldDateRange').click()
                    driver.find_element_by_id('startDate').clear()
                    driver.find_element_by_id('startDate').send_keys('01/01/1980', Keys.ENTER)
                    print('Executed JS scripts')
                    sleep(6)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = data[1]
                        price = price[:price.index('.')+2+1]
                        Open = data[2]
                        high = data[3]
                        low = data[4]
                        volume = data[5]  #change here
                        if volume == '-':
                            volume = None
                        change_perc = data[6][:-1] # Removing % symbol #change here
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
                    print(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        chunk_list = list(chunks(range(quanity), 3))
        try:
            # Code below creates threads for each item, then executes them by chunks
            threads = []
            for i in range(quanity):
                threads.append(Thread(target=work, args=(c_list[i],)))
            print('Threads are ready')
            chunk_n = 1
            chunk_all = len(chunk_list)
            for l in chunk_list:
                for sub_l in l:
                    threads[sub_l].start()
                    sleep(1)
                for sub_l in l:
                    threads[sub_l].join()
                
                print(f'Executed Chunk {chunk_n}/{chunk_all}')
                chunk_n += 1

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly')

    def canadaindices(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = CanadaIndexStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = CanadaIndexStaticInfo.objects.count() #change here
        #--------------------VPS------------------
        display = Display(visible=0, size=(1000, 1000))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
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
        def chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n):
                yield lst[i:i + n]
        
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            print(link)
            while True:
                try: 
                    driver.get(link)
                    sleep(5)
                    print('Executing JS scripts')
                    driver.execute_script('$("#data_interval").val("Monthly");')
                    driver.find_element_by_id('data_interval').value = "Monthly"
                    driver.find_element_by_id('widgetFieldDateRange').click()
                    driver.find_element_by_id('startDate').clear()
                    driver.find_element_by_id('startDate').send_keys('01/01/1980', Keys.ENTER)
                    print('Executed JS scripts')
                    sleep(6)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = data[1]
                        price = price[:price.index('.')+2+1]
                        Open = data[2]
                        high = data[3]
                        low = data[4]
                        volume = data[5]  #change here
                        if volume == '-':
                            volume = None
                        change_perc = data[6][:-1] # Removing % symbol #change here
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
                    print(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        chunk_list = list(chunks(range(quanity), 3))
        try:
            # Code below creates threads for each item, then executes them by chunks
            threads = []
            for i in range(quanity):
                threads.append(Thread(target=work, args=(c_list[i],)))
            print('Threads are ready')
            chunk_n = 1
            chunk_all = len(chunk_list)
            for l in chunk_list:
                for sub_l in l:
                    threads[sub_l].start()
                    sleep(1)
                for sub_l in l:
                    threads[sub_l].join()
                
                print(f'Executed Chunk {chunk_n}/{chunk_all}')
                chunk_n += 1

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly') 

    def germanyindices(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = GermanyIndexStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = GermanyIndexStaticInfo.objects.count() #change here
        #--------------------VPS------------------
        display = Display(visible=0, size=(1000, 1000))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
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
        def chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n):
                yield lst[i:i + n]
        
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            print(link)
            while True:
                try: 
                    driver.get(link)
                    sleep(5)
                    print('Executing JS scripts')
                    driver.execute_script('$("#data_interval").val("Monthly");')
                    driver.find_element_by_id('data_interval').value = "Monthly"
                    driver.find_element_by_id('widgetFieldDateRange').click()
                    driver.find_element_by_id('startDate').clear()
                    driver.find_element_by_id('startDate').send_keys('01/01/1980', Keys.ENTER)
                    print('Executed JS scripts')
                    sleep(6)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = data[1]
                        price = price[:price.index('.')+2+1]
                        Open = data[2]
                        high = data[3]
                        low = data[4]
                        volume = data[5]  #change here
                        if volume == '-':
                            volume = None
                        change_perc = data[6][:-1] # Removing % symbol #change here
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
                    print(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        chunk_list = list(chunks(range(quanity), 3))
        try:
            # Code below creates threads for each item, then executes them by chunks
            threads = []
            for i in range(quanity):
                threads.append(Thread(target=work, args=(c_list[i],)))
            print('Threads are ready')
            chunk_n = 1
            chunk_all = len(chunk_list)
            for l in chunk_list:
                for sub_l in l:
                    threads[sub_l].start()
                    sleep(1)
                for sub_l in l:
                    threads[sub_l].join()
                
                print(f'Executed Chunk {chunk_n}/{chunk_all}')
                chunk_n += 1

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly') 

    def australiaindices(delete='n'):
        # c_list = commodity_list its an old name never mind
        c_list = AustraliaIndexStaticInfo.objects.values_list('short_name', 'link') # returns a list of tuples #change here
        quanity = AustraliaIndexStaticInfo.objects.count() #change here
        #--------------------VPS------------------
        display = Display(visible=0, size=(1000, 1000))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
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
        def chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n):
                yield lst[i:i + n]
        
        def work(i):
            link = i[1]
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += '-historical-data' + cid
            else:
                link += '-historical-data'
            x = list(c_list).index(i)+1
            print(link)
            while True:
                try: 
                    driver.get(link)
                    sleep(5)
                    print('Executing JS scripts')
                    driver.execute_script('$("#data_interval").val("Monthly");')
                    driver.find_element_by_id('data_interval').value = "Monthly"
                    driver.find_element_by_id('widgetFieldDateRange').click()
                    driver.find_element_by_id('startDate').clear()
                    driver.find_element_by_id('startDate').send_keys('01/01/1980', Keys.ENTER)
                    print('Executed JS scripts')
                    sleep(6)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    soup = soup.find(class_='genTbl closedTbl historicalTbl')
                    soup = soup.tbody.find_all('tr')
                    for row in soup:
                        data = row.find_all('td')
                        data = [d.get_text() for d in data]
                        date = datetime.datetime.strptime(data[0], '%b %y')
                        price = data[1]
                        price = price[:price.index('.')+2+1]
                        Open = data[2]
                        high = data[3]
                        low = data[4]
                        volume = data[5]  #change here
                        if volume == '-':
                            volume = None
                        change_perc = data[6][:-1] # Removing % symbol #change here
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
                    print(e)
                    pass
            
            print(f'Stored {x}/{quanity}')
            print()

        chunk_list = list(chunks(range(quanity), 3))
        try:
            # Code below creates threads for each item, then executes them by chunks
            threads = []
            for i in range(quanity):
                threads.append(Thread(target=work, args=(c_list[i],)))
            print('Threads are ready')
            chunk_n = 1
            chunk_all = len(chunk_list)
            for l in chunk_list:
                for sub_l in l:
                    threads[sub_l].start()
                    sleep(1)
                for sub_l in l:
                    threads[sub_l].join()
                
                print(f'Executed Chunk {chunk_n}/{chunk_all}')
                chunk_n += 1

        finally:
            ('Quiting the driver')
            driver.quit()
        print('Finished Successfuly') 