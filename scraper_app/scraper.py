import requests, os, datetime
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
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
)

# This class is used only for cryptocurrencies, currencies, commodities, stocks and indices
class CollectStaticInfo:
    def commodities():
        print('Starting CollectStaticInfo.commodities()')
        print('Removing old records')
        CommodityStaticInfo.objects.all().delete()
        print('Old records have been removed')
        print('Starting to collect new ones')
        short_names = []
        links = []
        url = 'https://www.investing.com/commodities/'
        url2 = 'https://www.investing.com'
        header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'}
        request = requests.get(url, headers=header)
        soup = BeautifulSoup(request.text, 'html.parser')
        soup = soup.find_all('td', class_='noWrap bold left noWrap')
        fields_to_scrape = CommodityStaticInfo.fields_to_scrape

        for td in soup:
            short_names.append(td.find('a').get_text())
            links.append(url2+str(td.a['href']))
        print('Collected names and links')
        name_link = dict(zip(short_names, links))
        static_infos = []
        print('Starting Collecting Fields')
        
        for name, link in name_link.items():
            fields = {}
            request = requests.get(link, headers=header)
            soup = BeautifulSoup(request.text, 'html.parser')
            soup = soup.find_all('span')
            for field in soup:
                if field.get_text() in fields_to_scrape:
                    fields[field.get_text()] = field.next_sibling.get_text()
            static_infos.append({**{'Short Name': name, 'Link': link}, **fields})
            print(f'{len(short_names)-short_names.index(name)-1} Commodities Left')
            print('Sleeping for 10 seconds')
            sleep(10)
        print('Collected fields of all commodities')
        print('Starting to save data')
        for static_info in static_infos:
            print(f'Storing {static_info["Short Name"] + " Futures Contract"}')
            CommodityStaticInfo(
                short_name=static_info['Short Name'], base_symbol=static_info['Base Symbol'],
                contract_size=static_info['Contract Size'],
                tick_size=static_info['Tick Size'], tick_value=static_info['Tick Value'],
                months=static_info['Months'], point_value=static_info['Point Value'],
                link=static_info['Link']).save()
        print('Data has been successfuly stored!')
        return ''

    def currencies():
        print('Starting CollectStaticInfo.currencies()')
        print('Removing old records')
        CurrencyStaticInfo.objects.all().delete()
        print('Old records have been removed')
        print('Starting to collect new ones')
        short_names = []
        links = []
        url = 'https://www.investing.com/currencies/'
        url2 = 'https://www.investing.com'
        header={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
        request = requests.get(url, headers=header)
        soup = BeautifulSoup(request.text, 'html.parser')
        soup = soup.find_all('td', class_='noWrap bold left noWrap')
        for td in soup:
            short_names.append(td.find('a').get_text())
            links.append(url2+str(td.a['href']))
        print('Collected names and links')
        print('Sleeping for 2 seconds!')
        sleep(2)
        name_link = dict(zip(short_names, links))
        print('Starting to collect long names')
        static_infos = []
        for name, link in name_link.items():
            request = requests.get(link, headers=header)
            soup = BeautifulSoup(request.text, 'html.parser')
            soup = soup.find('div', class_='instrumentHead').h1.get_text() #EUR/USD - Euro US Dollar
            long_name = soup[soup.index('-')+1:] #Euro US Dollar
            static_infos.append({'Short Name': name, 'Long Name': long_name, 'Link': link})
            print(f'{len(short_names)-short_names.index(name)-1} Currencies Left')
            print('Sleeping for 10 seconds')
            sleep(10)

        for static_info in static_infos:
            print(f'Storing {static_info["Long Name"]}')
            CurrencyStaticInfo(
                short_name=static_info['Short Name'], long_name=static_info['Long Name'],
                link=static_info['Link']).save()
        
        print('Data has been successfuly stored!')
        return ''

    def cryptocurrencies():
        print('Starting CollectStaticInfo.cryptocurrencies()')
        print('Removing old records')
        CryptocurrencyStaticInfo.objects.all().delete()
        print('Old records have been removed')
        print('Starting to collect new ones')
        short_names = []
        long_names = []
        links = []
        url = 'https://www.investing.com/crypto/'
        url2 = 'https://www.investing.com'
        header={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
        request = requests.get(url, headers=header)
        soup = BeautifulSoup(request.text, 'html.parser')
        soup1 = soup.find_all('td', class_='left bold elp name cryptoName first js-currency-name')
        soup2 = soup.find_all('td', class_='left noWrap elp symb js-currency-symbol')
        for td1, td2 in zip(soup1, soup2):
            try:
                long_names.append(td1.find('a').get_text())
                links.append(url2+str(td1.a['href']))
                short_names.append(td2.get_text())
            except:
                pass
        print('Collected all data')
        print('Starting to store data')
        for i in range(len(short_names)):
            print(f'Storing {long_names[i]}')
            CryptocurrencyStaticInfo(
                short_name=short_names[i], long_name=long_names[i],
                link=links[i]).save()
        
        print('Data has been successfuly stored!')
        return ''

    def usstocks():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectStaticInfo.usstocks()')
        print('Removing old records')
        dd = input('Are you sure you want to delete all the old records, and scrape new ones? Press Y or y to continue: ')
        if dd.upper() != 'Y':
            print('Closing CollectStaticInfo.usstocks()')
            return ''
        USStockStaticInfo.objects.all().delete()
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        url = 'https://www.investing.com/equities/united-states'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        print('Executing JS scripts')
        driver.execute_script('$("#stocksFilter").val("#all");')
        sleep(5)
        driver.execute_script("doStocksFilter('select',this)")
        sleep(15)
        print('Executed JS scripts, sleeping for 15 seconds')
        sleep(15)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        long_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            long_names.append(link.a['title'])

        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 3M Company (MMM)
                short_name = short_name[short_name.index('(')+1:].strip().replace(')', '') # MMM
                market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                markets = [m[0] for m in MARKETS_US]
                isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                if market not in markets:
                    market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                    market = market.find_all('tr')
                    for tr in market:
                        if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                            market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                            break
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 3M Company (MMM)
                    short_name = short_name[short_name.index('(')+1:].strip().replace(')', '') # MMM
                    market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                    markets = [m[0] for m in MARKETS_US]
                    isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                    if market not in markets:
                        market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                        market = market.find_all('tr')
                        for tr in market:
                            if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                                market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                                break
                except:
                    continue

            USStockStaticInfo(
                short_name=short_name, long_name=long_names[i],
                market=market, isin=isin, link=l).save()
            print(f'Stored {i}: {long_names[i]}')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
            i += 1

        print('Data has been successfuly stored!')
        return ''

    def japanstocks():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectStaticInfo.japanstocks()')
        print('Removing old records')
        dd = input('Are you sure you want to delete all the old records, and scrape new ones? Press Y or y to continue: ')
        if dd.upper() != 'Y':
            print('Closing CollectStaticInfo.japanstocks()')
            return ''
        JapanStockStaticInfo.objects.all().delete()
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        url = 'https://www.investing.com/equities/japan'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        print('Executing JS scripts')
        driver.execute_script('$("#stocksFilter").val("#all");')
        sleep(5)
        driver.execute_script("doStocksFilter('select',this)")
        sleep(15)
        print('Executed JS scripts, sleeping for 15 seconds')
        sleep(15)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        long_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            long_names.append(link.a['title'])

        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 3M Company (MMM)
                short_name = short_name[short_name.index('(')+1:].strip().replace(')', '') # MMM
                isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                markets = [m[0] for m in MARKETS_JP]
                if market not in markets:
                    market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                    market = market.find_all('tr')
                    for tr in market:
                        if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                            market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                            break
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 3M Company (MMM)
                    short_name = short_name[short_name.index('(')+1:].strip().replace(')', '') # MMM
                    isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                    market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                    markets = [m[0] for m in MARKETS_JP]
                    if market not in markets:
                        market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                        market = market.find_all('tr')
                        for tr in market:
                            if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                                market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                                break
                except:
                    continue
            
            JapanStockStaticInfo(
                short_name=short_name, long_name=long_names[i],
                market=market, isin=isin, link=l).save()
            print(f'Stored {i}: {long_names[i]}')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
            i += 1

        print('Data has been successfuly stored!')
        return ''

    def ukstocks():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectStaticInfo.ukstocks()')
        print('Removing old records')
        dd = input('Are you sure you want to delete all the old records, and scrape new ones? Press Y or y to continue: ')
        if dd.upper() != 'Y':
            print('Closing CollectStaticInfo.ukstocks()')
            return ''
        UKStockStaticInfo.objects.all().delete()
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        url = 'https://www.investing.com/equities/united-kingdom'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        print('Executing JS scripts')
        driver.execute_script('$("#stocksFilter").val("#all");')
        sleep(5)
        driver.execute_script("doStocksFilter('select',this)")
        sleep(15)
        print('Executed JS scripts, sleeping for 15 seconds')
        sleep(15)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        long_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            long_names.append(link.a['title'])

        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 3M Company (MMM)
                short_name = short_name[short_name.index('(')+1:].strip().replace(')', '') # MMM
                isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
            except:
                try:
                    print('Some Complications')
                    sleep(10) 
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 3M Company (MMM)
                    short_name = short_name[short_name.index('(')+1:].strip().replace(')', '') # MMM
                    isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                except:
                    continue
                    
            UKStockStaticInfo(
                short_name=short_name, long_name=long_names[i],
                isin=isin, link=l).save()
            print(f'Stored {i}: {long_names[i]}')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
            i += 1

        print('Data has been successfuly stored!')
        return ''

    def hkstocks():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectStaticInfo.hkstocks()')
        print('Removing old records')
        dd = input('Are you sure you want to delete all the old records, and scrape new ones? Press Y or y to continue: ')
        if dd.upper() != 'Y':
            print('Closing CollectStaticInfo.hkstocks()')
            return ''
        HKStockStaticInfo.objects.all().delete()
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        url = 'https://www.investing.com/equities/hong-kong'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        print('Executing JS scripts')
        driver.execute_script('$("#stocksFilter").val("#all");')
        sleep(5)
        driver.execute_script("doStocksFilter('select',this)")
        sleep(15)
        print('Executed JS scripts, sleeping for 15 seconds')
        sleep(15)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        long_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            long_names.append(link.a['title'])

        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 3M Company (1234)
                short_name = short_name.strip()[-5:-1] # 1234
                isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
            except:
                try:
                    print('Some Complications')
                    sleep(10) 
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 3M Company (1234)
                    short_name = short_name.strip()[-5:-1] # 1234
                    isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                except:
                    continue
            HKStockStaticInfo(
                short_name=short_name, long_name=long_names[i],
                isin=isin, link=l).save()
            print(f'Stored {i}: {long_names[i]}')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
            i += 1

        print('Data has been successfuly stored!')
        return ''

    def chinastocks():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectStaticInfo.chinastocks()')
        print('Removing old records')
        dd = input('Are you sure you want to delete all the old records, and scrape new ones? Press Y or y to continue: ')
        if dd.upper() != 'Y':
            print('Closing CollectStaticInfo.chinastocks()')
            return ''
        ChinaStockStaticInfo.objects.all().delete()
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        url = 'https://www.investing.com/equities/china'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        print('Executing JS scripts')
        driver.execute_script('$("#stocksFilter").val("#all");')
        sleep(5)
        driver.execute_script("doStocksFilter('select',this)")
        sleep(15)
        print('Executed JS scripts, sleeping for 15 seconds')
        sleep(15)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        long_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            long_names.append(link.a['title'])

        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # Huadian Ener-B - (900937)
                short_name = short_name.strip()[-7:-1] # 900937
                market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
            except:
                try:
                    print('Some Complications')
                    sleep(10) 
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # Huadian Ener-B - (900937)
                    short_name = short_name.strip()[-7:-1] # 900937
                    market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                    isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                except:
                    continue
                    
            ChinaStockStaticInfo(
                short_name=short_name, long_name=long_names[i],
                isin=isin, market=market, link=l).save()
            print(f'Stored {i}: {long_names[i]}')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
            i += 1

        print('Data has been successfuly stored!')
        return ''

    def canadastocks():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectStaticInfo.canadastocks()')
        print('Removing old records')
        dd = input('Are you sure you want to delete all the old records, and scrape new ones? Press Y or y to continue: ')
        if dd.upper() != 'Y':
            print('Closing CollectStaticInfo.canadastocks()')
            return ''
        CanadaStockStaticInfo.objects.all().delete()
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        url = 'https://www.investing.com/equities/canada'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        print('Executing JS scripts')
        driver.execute_script('$("#stocksFilter").val("#all");')
        sleep(5)
        driver.execute_script("doStocksFilter('select',this)")
        sleep(15)
        print('Executed JS scripts, sleeping for 15 seconds')
        sleep(15)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        long_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            long_names.append(link.a['title'])
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 'Hang Seng China Affiliated Corps (CCI) (HSCC)'
                short_name = short_name[::-1] # ')CCSH( )ICC( sproC detailiffA anihC gneS gnaH'
                short_name = short_name[short_name.index(')')+1:short_name.index('(')][::-1] # HSCC
                isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                markets = [m[0] for m in MARKETS_CA]
                if market not in markets:
                    market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                    market = market.find_all('tr')
                    for tr in market:
                        if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                            market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                            break
            except:
                try:
                    print('Some Complications')
                    sleep(10) 
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 'Hang Seng China Affiliated Corps (CCI) (HSCC)'
                    short_name = short_name[::-1] # ')CCSH( )ICC( sproC detailiffA anihC gneS gnaH'
                    short_name = short_name[short_name.index(')')+1:short_name.index('(')][::-1] # HSCC
                    isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                    market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                    markets = [m[0] for m in MARKETS_CA]
                    if market not in markets:
                        market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                        market = market.find_all('tr')
                        for tr in market:
                            if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                                market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                                break
                except:
                    continue
                    
            CanadaStockStaticInfo(
                short_name=short_name, long_name=long_names[i],
                isin=isin, market=market, link=l).save()
            print(f'Stored {i}: {long_names[i]}')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
            i += 1

        print('Data has been successfuly stored!')
        return ''

    def germanystocks():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectStaticInfo.germanystocks()')
        print('Removing old records')
        dd = input('Are you sure you want to delete all the old records, and scrape new ones? Press Y or y to continue: ')
        if dd.upper() != 'Y':
            print('Closing CollectStaticInfo.germanystocks()')
            return ''
        GermanyStockStaticInfo.objects.all().delete()
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        url = 'https://www.investing.com/equities/germany'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        print('Executing JS scripts')
        driver.execute_script('$("#stocksFilter").val("#all");')
        sleep(5)
        driver.execute_script("doStocksFilter('select',this)")
        sleep(15)
        print('Executed JS scripts, sleeping for 15 seconds')
        sleep(15)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        long_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            long_names.append(link.a['title'])
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 'Hang Seng China Affiliated Corps (CCI) (HSCC)'
                short_name = short_name[::-1] # ')CCSH( )ICC( sproC detailiffA anihC gneS gnaH'
                short_name = short_name[short_name.index(')')+1:short_name.index('(')]
                isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                markets = [m[0] for m in MARKETS_GE]
                if market not in markets:
                    market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                    market = market.find_all('tr')
                    for tr in market:
                        if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                            market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                            break
            except:
                try:
                    print('Some Complications')
                    sleep(10) 
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 'Hang Seng China Affiliated Corps (CCI) (HSCC)'
                    short_name = short_name[::-1] # ')CCSH( )ICC( sproC detailiffA anihC gneS gnaH'
                    short_name = short_name[short_name.index(')')+1:short_name.index('(')]
                    isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                    market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                    markets = [m[0] for m in MARKETS_GE]
                    if market not in markets:
                        market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                        market = market.find_all('tr')
                        for tr in market:
                            if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                                market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                                break
                except:
                    continue
            GermanyStockStaticInfo(
                short_name=short_name, long_name=long_names[i],
                isin=isin, market=market, link=l).save()
            print(f'Stored {i}: {long_names[i]}')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
            i += 1

        print('Data has been successfuly stored!')
        return ''

    def australiastocks():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectStaticInfo.australiastocks()')
        print('Removing old records')
        dd = input('Are you sure you want to delete all the old records, and scrape new ones? Press Y or y to continue: ')
        if dd.upper() != 'Y':
            print('Closing CollectStaticInfo.australiastocks()')
            return ''
        AustraliaStockStaticInfo.objects.all().delete()
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        url = 'https://www.investing.com/equities/australia'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        print('Executing JS scripts')
        driver.execute_script('$("#stocksFilter").val("#all");')
        sleep(5)
        driver.execute_script("doStocksFilter('select',this)")
        sleep(15)
        print('Executed JS scripts, sleeping for 15 seconds')
        sleep(15)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        long_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            long_names.append(link.a['title'])
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 3M Company (MMM)
                short_name = short_name[short_name.index('(')+1:].strip().replace(')', '') # MMM
                isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
            except:
                try:
                    print('Some Complications')
                    sleep(10) 
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 3M Company (MMM)
                    short_name = short_name[short_name.index('(')+1:].strip().replace(')', '') # MMM
                    isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                except:
                    continue
            AustraliaStockStaticInfo(
                short_name=short_name, long_name=long_names[i],
                isin=isin, link=l).save()
            print(f'Stored {i}: {long_names[i]}')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
            i += 1

        print('Data has been successfuly stored!')
        return ''


    # INDICES' STATIC INFO AREA
    def usindices():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectStaticInfo.usindices()')
        dd = input('Are you sure you want to delete all the old records, and scrape new ones? Press Y or y to continue: ')
        print('Removing old records')
        if dd.upper() != 'Y':
            print('Closing CollectStaticInfo.usindices()')
            return ''
        USIndexStaticInfo.objects.all().delete()
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        url = 'https://www.investing.com/indices/usa-indices?&majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        long_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            long_names.append(link.a['title'])

        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 3M Company (MMM)
                short_name = short_name[short_name.index('(')+1:].strip().replace(')', '') # MMM
                market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                markets = [m[0] for m in MARKETS_US]
                if market not in markets:
                    market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                    market = market.find_all('tr')
                    for tr in market:
                        if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                            market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                            break
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 3M Company (MMM)
                    short_name = short_name[short_name.index('(')+1:].strip().replace(')', '') # MMM
                    market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                    markets = [m[0] for m in MARKETS_US]
                    if market not in markets:
                        market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                        market = market.find_all('tr')
                        for tr in market:
                            if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                                market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                                break
                except:
                    continue
            USIndexStaticInfo(
                short_name=short_name, long_name=long_names[i],
                market=market, link=l).save()
            print(f'Stored {i}: {long_names[i]}')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
            i += 1

        print('Data has been successfuly stored!')
        return ''

    def japanindices():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectStaticInfo.japanindices()')
        dd = input('Are you sure you want to delete all the old records, and scrape new ones? Press Y or y to continue: ')
        print('Removing old records')
        if dd.upper() != 'Y':
            print('Closing CollectStaticInfo.japanindices()')
            return ''
        JapanIndexStaticInfo.objects.all().delete()
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        url = 'https://www.investing.com/indices/japan-indices?majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        long_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            long_names.append(link.a['title'])

        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 3M Company (MMM)
                short_name = short_name[short_name.index('(')+1:].strip().replace(')', '') # MMM
                market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                markets = [m[0] for m in MARKETS_JP]
                if market not in markets:
                    market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                    market = market.find_all('tr')
                    for tr in market:
                        if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                            market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                            break
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 3M Company (MMM)
                    short_name = short_name[short_name.index('(')+1:].strip().replace(')', '') # MMM
                    market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                    markets = [m[0] for m in MARKETS_JP]
                    if market not in markets:
                        market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                        market = market.find_all('tr')
                        for tr in market:
                            if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                                market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                                break
                except:
                    continue
            JapanIndexStaticInfo(
                short_name=short_name, long_name=long_names[i],
                market=market, link=l).save()
            print(f'Stored {i}: {long_names[i]}')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
            i += 1

        print('Data has been successfuly stored!')
        return ''

    def ukindices():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectStaticInfo.ukindices()')
        dd = input('Are you sure you want to delete all the old records, and scrape new ones? Press Y or y to continue: ')
        print('Removing old records')
        if dd.upper() != 'Y':
            print('Closing CollectStaticInfo.ukindices()')
            return ''
        UKIndexStaticInfo.objects.all().delete()
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        url = 'https://www.investing.com/indices/uk-indices?majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        long_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            long_names.append(link.a['title'])
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 3M Company (MMM)
                short_name = short_name[short_name.index('(')+1:].strip().replace(')', '') # MMM
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 3M Company (MMM)
                    short_name = short_name[short_name.index('(')+1:].strip().replace(')', '') # MMM
                except:
                    continue
            UKIndexStaticInfo(
                short_name=short_name, long_name=long_names[i], link=l).save()
            print(f'Stored {i}: {long_names[i]}')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
            i += 1

        print('Data has been successfuly stored!')
        return ''

    def hkindices():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectStaticInfo.hkindices()')
        dd = input('Are you sure you want to delete all the old records, and scrape new ones? Press Y or y to continue: ')
        print('Removing old records')
        if dd.upper() != 'Y':
            print('Closing CollectStaticInfo.hkindices()')
            return ''
        HKIndexStaticInfo.objects.all().delete()
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        url = 'https://www.investing.com/indices/hong-kong-indices?majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        long_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            long_names.append(link.a['title'])
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 'Hang Seng China Affiliated Corps (CCI) (HSCC)'
                short_name = short_name[::-1] # ')CCSH( )ICC( sproC detailiffA anihC gneS gnaH'
                short_name = short_name[short_name.index(')')+1:short_name.index('(')][::-1] # HSCC
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 'Hang Seng China Affiliated Corps (CCI) (HSCC)'
                    short_name = short_name[::-1] # ')CCSH( )ICC( sproC detailiffA anihC gneS gnaH'
                    short_name = short_name[short_name.index(')')+1:short_name.index('(')][::-1] # HSCC
                except:
                    continue
            HKIndexStaticInfo(
                short_name=short_name, long_name=long_names[i], link=l).save()
            print(f'Stored {i}: {long_names[i]}')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
            i += 1

        print('Data has been successfuly stored!')
        return ''

    def chinaindices():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectStaticInfo.chinaindices()')
        dd = input('Are you sure you want to delete all the old records, and scrape new ones? Press Y or y to continue: ')
        print('Removing old records')
        if dd.upper() != 'Y':
            print('Closing CollectStaticInfo.chinaindices()')
            return ''
        ChinaIndexStaticInfo.objects.all().delete()
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        url = 'https://www.investing.com/indices/china-indices?&majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        long_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            long_names.append(link.a['title'])
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 'Hang Seng China Affiliated Corps (CCI) (HSCC)'
                short_name = short_name[::-1] # ')CCSH( )ICC( sproC detailiffA anihC gneS gnaH'
                short_name = short_name[short_name.index(')')+1:short_name.index('(')][::-1] # HSCC
                market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                markets = [m[0] for m in MARKETS_CH]
                if market not in markets:
                    market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                    market = market.find_all('tr')
                    for tr in market:
                        if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                            market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                            break
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 'Hang Seng China Affiliated Corps (CCI) (HSCC)'
                    short_name = short_name[::-1] # ')CCSH( )ICC( sproC detailiffA anihC gneS gnaH'
                    short_name = short_name[short_name.index(')')+1:short_name.index('(')][::-1] # HSCC
                    market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                    markets = [m[0] for m in MARKETS_CH]
                    if market not in markets:
                        market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                        market = market.find_all('tr')
                        for tr in market:
                            if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                                market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                                break
                except:
                    continue
            ChinaIndexStaticInfo(
                short_name=short_name, long_name=long_names[i], 
                market=market, link=l).save()
            print(f'Stored {i}: {long_names[i]}')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
            i += 1

        print('Data has been successfuly stored!')
        return ''

    def canadaindices():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectStaticInfo.canadaindices()')
        dd = input('Are you sure you want to delete all the old records, and scrape new ones? Press Y or y to continue: ')
        if dd.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectStaticInfo.canadaindices()')
            return ''
        CanadaIndexStaticInfo.objects.all().delete()
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        url = 'https://www.investing.com/indices/canada-indices?majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        long_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            long_names.append(link.a['title'])
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 'Hang Seng China Affiliated Corps (CCI) (HSCC)'
                short_name = short_name[::-1] # ')CCSH( )ICC( sproC detailiffA anihC gneS gnaH'
                short_name = short_name[short_name.index(')')+1:short_name.index('(')][::-1] # HSCC
                market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                markets = [m[0] for m in MARKETS_CA]
                if market not in markets:
                    market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                    market = market.find_all('tr')
                    for tr in market:
                        if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                            market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                            break
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 'Hang Seng China Affiliated Corps (CCI) (HSCC)'
                    short_name = short_name[::-1] # ')CCSH( )ICC( sproC detailiffA anihC gneS gnaH'
                    short_name = short_name[short_name.index(')')+1:short_name.index('(')][::-1] # HSCC
                    market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                    markets = [m[0] for m in MARKETS_CA]
                    if market not in markets:
                        market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                        market = market.find_all('tr')
                        for tr in market:
                            if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                                market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                                break
                except:
                    continue
            CanadaIndexStaticInfo(
                short_name=short_name, long_name=long_names[i], 
                market=market, link=l).save()
            print(f'Stored {i}: {long_names[i]}')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
                i += 1
        
        print('Data has been successfuly stored!')
        return ''

    def germanyindices():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectStaticInfo.germanyindices()')
        dd = input('Are you sure you want to delete all the old records, and scrape new ones? Press Y or y to continue: ')
        if dd.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectStaticInfo.germanyindices()')
            return ''
        GermanyIndexStaticInfo.objects.all().delete()
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        url = 'https://www.investing.com/indices/germany-indices?majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        long_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            long_names.append(link.a['title'])
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 'Hang Seng China Affiliated Corps (CCI) (HSCC)'
                short_name = short_name[::-1] # ')CCSH( )ICC( sproC detailiffA anihC gneS gnaH'
                short_name = short_name[short_name.index(')')+1:short_name.index('(')][::-1] # HSCC
                market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                markets = [m[0] for m in MARKETS_GE]
                if market not in markets:
                    market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                    market = market.find_all('tr')
                    for tr in market:
                        if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                            market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                            break
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 'Hang Seng China Affiliated Corps (CCI) (HSCC)'
                    short_name = short_name[::-1] # ')CCSH( )ICC( sproC detailiffA anihC gneS gnaH'
                    short_name = short_name[short_name.index(')')+1:short_name.index('(')][::-1] # HSCC
                    market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                    markets = [m[0] for m in MARKETS_GE]
                    if market not in markets:
                        market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                        market = market.find_all('tr')
                        for tr in market:
                            if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                                market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                                break
                except:
                    continue
            GermanyIndexStaticInfo(
                short_name=short_name, long_name=long_names[i], 
                market=market, link=l).save() 
            print(f'Stored {i}: {long_names[i]}')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
                i += 1
        
        print('Data has been successfuly stored!')
        return ''

    def australiaindices():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectStaticInfo.australiaindices()')
        dd = input('Are you sure you want to delete all the old records, and scrape new ones? Press Y or y to continue: ')
        if dd.upper() != 'Y':
            print('Removing old records')
            print('Closing CollectStaticInfo.australiaindices()')
            return ''
        AustraliaIndexStaticInfo.objects.all().delete()
        print('Old records have been removed')
        print('Starting to collect new ones')
        print('Starting Selenium')
        url = 'https://www.investing.com/indices/australia-indices?majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        long_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            long_names.append(link.a['title'])
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 'Hang Seng China Affiliated Corps (CCI) (HSCC)'
                short_name = short_name[::-1] # ')CCSH( )ICC( sproC detailiffA anihC gneS gnaH'
                short_name = short_name[short_name.index(')')+1:short_name.index('(')][::-1] # HSCC
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 'Hang Seng China Affiliated Corps (CCI) (HSCC)'
                    short_name = short_name[::-1] # ')CCSH( )ICC( sproC detailiffA anihC gneS gnaH'
                    short_name = short_name[short_name.index(')')+1:short_name.index('(')][::-1] # HSCC
                except:
                    continue
            AustraliaIndexStaticInfo(
                short_name=short_name, long_name=long_names[i], link=l).save()
            print(f'Stored {i}: {long_names[i]}')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
                i += 1

        
        print('Data has been successfuly stored!')
        return ''

class CollectETFIssuers:
    def all():
        print('Starting to collect for United States')
        CollectETFIssuers.us()
        print('Starting to collect for Japan')
        CollectETFIssuers.japan()
        print('Starting to collect for United Kingdom')
        CollectETFIssuers.uk()
        print('Starting to collect for Honk Kong')
        CollectETFIssuers.hk()
        print('Starting to collect for China')
        CollectETFIssuers.china()
        print('Starting to collect for Canada')
        CollectETFIssuers.canada()
        print('Starting to collect for Germany')
        CollectETFIssuers.germany()
        print('Starting to collect for Australia')
        CollectETFIssuers.australia()


    def us():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting get_etf_issuers.us()')
        print('Starting Selenium')
        url = 'https://www.investing.com/etfs/usa-etfs?&issuer_filter=0'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        ETFIssuers.objects.filter(country='US').delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and collect issuers info')
        i = 0
        issuers = []
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                except:
                    continue
            print(f'Visited {i}/{len(links)-1}')
            i += 1
            issuers.append(issuer)
        issuers = list(set(issuers))
        for issuer in issuers:
            ETFIssuers(country='US', name=issuer).save()
        return ''

    def japan():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting get_etf_issuers.japan()')
        print('Starting Selenium')
        url = 'https://www.investing.com/etfs/japan-etfs?&issuer_filter=0'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        ETFIssuers.objects.filter(country='JP').delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and collect issuers info')
        i = 0
        issuers = []
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                except:
                    continue
            print(f'Visited {i}/{len(links)-1}')
            i += 1
            issuers.append(issuer)
        issuers = list(set(issuers))
        for issuer in issuers:
            ETFIssuers(country='JP', name=issuer).save()
        return ''

    def uk():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting get_etf_issuers.uk()')
        print('Starting Selenium')
        url = 'https://www.investing.com/etfs/uk-etfs?&issuer_filter=0'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        ETFIssuers.objects.filter(country='UK').delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and collect issuers info')
        i = 0
        issuers = []
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                except:
                    continue
            print(f'Visited {i}/{len(links)-1}')
            i += 1
            issuers.append(issuer)
        issuers = list(set(issuers))
        for issuer in issuers:
            ETFIssuers(country='UK', name=issuer).save()
        print('Results are saved in -> United Kingdom ETF Issuers.txt')
        return ''

    def hk():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting get_etf_issuers.hk()')
        print('Starting Selenium')
        url = 'https://www.investing.com/etfs/hong-kong-etfs?&issuer_filter=0'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        ETFIssuers.objects.filter(country='HK').delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and collect issuers info')
        i = 0
        issuers = []
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                except:
                    continue
            print(f'Visited {i}/{len(links)-1}')
            i += 1
            issuers.append(issuer)
        issuers = list(set(issuers))
        for issuer in issuers:
            ETFIssuers(country='HK', name=issuer).save()
        print('Results are saved in -> Honk Kong ETF Issuers.txt')
        return ''

    def china():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting get_etf_issuers.china()')
        print('Starting Selenium')
        url = 'https://www.investing.com/etfs/china-etfs?&issuer_filter=0'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        ETFIssuers.objects.filter(country='CH').delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and collect issuers info')
        i = 0
        issuers = []
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                except:
                    continue
            print(f'Visited {i}/{len(links)-1}')
            i += 1
            issuers.append(issuer)
        issuers = list(set(issuers))
        for issuer in issuers:
            ETFIssuers(country='CH', name=issuer).save()
        print('Results are saved in -> China ETF Issuers.txt')
        return ''

    def canada():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting get_etf_issuers.canada()')
        print('Starting Selenium')
        url = 'https://www.investing.com/etfs/canada-etfs?&issuer_filter=0'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        ETFIssuers.objects.filter(country='CA').delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and collect issuers info')
        i = 0
        issuers = []
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                except:
                    continue
            print(f'Visited {i}/{len(links)-1}')
            i += 1
            issuers.append(issuer)
        issuers = list(set(issuers))
        for issuer in issuers:
            ETFIssuers(country='CA', name=issuer).save()
        print('Results are saved in -> Canada ETF Issuers.txt')
        return ''

    def germany():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting get_etf_issuers.germany()')
        print('Starting Selenium')
        url = 'https://www.investing.com/etfs/germany-etfs?&issuer_filter=0'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        ETFIssuers.objects.filter(country='GE').delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and collect issuers info')
        i = 0
        issuers = []
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                except:
                    continue
            print(f'Visited {i}/{len(links)-1}')
            i += 1
            issuers.append(issuer)
        issuers = list(set(issuers))
        for issuer in issuers:
            ETFIssuers(country='GE', name=issuer).save()
        print('Results are saved in -> Germany ETF Issuers.txt')
        return ''

    def australia():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting get_etf_issuers.australia()')
        print('Starting Selenium')
        url = 'https://www.investing.com/etfs/australia-etfs?&issuer_filter=0'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        ETFIssuers.objects.filter(country='AU').delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and collect issuers info')
        i = 0
        issuers = []
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                except:
                    continue
            print(f'Visited {i}/{len(links)-1}')
            i += 1
            issuers.append(issuer)
        issuers = list(set(issuers))
        for issuer in issuers:
            ETFIssuers(country='AU', name=issuer).save()
        print('Results are saved in -> Australia ETF Issuers.txt')
        return ''

class CollectETFStaticInfo:
    def all():
        print('Starting CollectETFStaticInfo')
        print('Starting to collect for United States')
        CollectETFStaticInfo.us()
        print('Starting to collect for Japan')
        CollectETFStaticInfo.japan()
        print('Starting to collect for United Kingdom')
        CollectETFStaticInfo.uk()
        print('Starting to collect for Honk Kong')
        CollectETFStaticInfo.hk()
        print('Starting to collect for China')
        CollectETFStaticInfo.china()
        print('Starting to collect for Canada')
        CollectETFStaticInfo.canada()
        print('Starting to collect for Germany')
        CollectETFStaticInfo.germany()
        print('Starting to collect for Australia')
        CollectETFStaticInfo.australia()


    def us():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting get_etf_issuers.us()')
        print('Starting Selenium')
        url = 'https://www.investing.com/etfs/usa-etfs?&issuer_filter=0'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        USETFStaticInfo.objects.all().delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        long_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            long_names.append(link.a['title'])
        
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 'Hang Seng China Affiliated Corps (CCI) (HSCC)'
                short_name = short_name[::-1] # ')CCSH( )ICC( sproC detailiffA anihC gneS gnaH'
                short_name = short_name[short_name.index(')')+1:short_name.index('(')][::-1] # HSCC
                market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                markets = [m[0] for m in MARKETS_US]
                issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                if market not in markets:
                    market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                    market = market.find_all('tr')
                    for tr in market:
                        if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                            market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                            break
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 'Hang Seng China Affiliated Corps (CCI) (HSCC)'
                    short_name = short_name[::-1] # ')CCSH( )ICC( sproC detailiffA anihC gneS gnaH'
                    short_name = short_name[short_name.index(')')+1:short_name.index('(')][::-1] # HSCC
                    market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                    markets = [m[0] for m in MARKETS_US]
                    issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                    isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                    if market not in markets:
                        market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                        market = market.find_all('tr')
                        for tr in market:
                            if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                                market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                                break
                except:
                    continue
            USETFStaticInfo(
                short_name=short_name, long_name=long_names[i],
                market=market, issuer=issuer, isin=isin, link=l).save()
            print(f'Stored {i}: {long_names[i]} ({i}/{len(long_names)})')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
            i += 1

        print('Data has been successfuly stored!')
        return ''

    def japan():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting get_etf_issuers.japan()')
        print('Starting Selenium')
        url = 'https://www.investing.com/etfs/japan-etfs?&issuer_filter=0'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        JapanETFStaticInfo.objects.all().delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        long_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            long_names.append(link.a['title'])
        
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 'Hang Seng China Affiliated Corps (CCI) (HSCC)'
                short_name = short_name[::-1] # ')CCSH( )ICC( sproC detailiffA anihC gneS gnaH'
                short_name = short_name[short_name.index(')')+1:short_name.index('(')][::-1] # HSCC
                market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                markets = [m[0] for m in MARKETS_JP]
                issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                if market not in markets:
                    market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                    market = market.find_all('tr')
                    for tr in market:
                        if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                            market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                            break
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 'Hang Seng China Affiliated Corps (CCI) (HSCC)'
                    short_name = short_name[::-1] # ')CCSH( )ICC( sproC detailiffA anihC gneS gnaH'
                    short_name = short_name[short_name.index(')')+1:short_name.index('(')][::-1] # HSCC
                    market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                    markets = [m[0] for m in MARKETS_JP]
                    issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                    isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                    if market not in markets:
                        market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                        market = market.find_all('tr')
                        for tr in market:
                            if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                                market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                                break
                except:
                    continue

            JapanETFStaticInfo(
                short_name=short_name, long_name=long_names[i],
                market=market, issuer=issuer, isin=isin, link=l).save()
            print(f'Stored {i}: {long_names[i]} ({i}/{len(long_names)})')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
            i += 1

        print('Data has been successfuly stored!')
        return ''

    def uk():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting get_etf_issuers.uk()')
        print('Starting Selenium')
        url = 'https://www.investing.com/etfs/uk-etfs?&issuer_filter=0'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        UKETFStaticInfo.objects.all().delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        long_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            long_names.append(link.a['title'])
        
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 'Hang Seng China Affiliated Corps (CCI) (HSCC)'
                short_name = short_name[::-1] # ')CCSH( )ICC( sproC detailiffA anihC gneS gnaH'
                short_name = short_name[short_name.index(')')+1:short_name.index('(')][::-1] # HSCC
                issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 'Hang Seng China Affiliated Corps (CCI) (HSCC)'
                    short_name = short_name[::-1] # ')CCSH( )ICC( sproC detailiffA anihC gneS gnaH'
                    short_name = short_name[short_name.index(')')+1:short_name.index('(')][::-1] # HSCC
                    issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                    isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                except:
                    continue

            UKETFStaticInfo(
                short_name=short_name, long_name=long_names[i],
                issuer=issuer, isin=isin, link=l).save()
            print(f'Stored {i}: {long_names[i]} ({i}/{len(long_names)})')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
            i += 1

        print('Data has been successfuly stored!')
        return ''

    def hk():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting get_etf_issuers.hk()')
        print('Starting Selenium')
        url = 'https://www.investing.com/etfs/hong-kong-etfs?&issuer_filter=0'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        HKETFStaticInfo.objects.all().delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        long_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            long_names.append(link.a['title'])
        
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 'Hang Seng China Affiliated Corps (CCI) (HSCC)'
                short_name = short_name[::-1] # ')CCSH( )ICC( sproC detailiffA anihC gneS gnaH'
                short_name = short_name[short_name.index(')')+1:short_name.index('(')][::-1] # HSCC
                issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 'Hang Seng China Affiliated Corps (CCI) (HSCC)'
                    short_name = short_name[::-1] # ')CCSH( )ICC( sproC detailiffA anihC gneS gnaH'
                    short_name = short_name[short_name.index(')')+1:short_name.index('(')][::-1] # HSCC
                    issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                    isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                except:
                    continue

            HKETFStaticInfo(
                short_name=short_name, long_name=long_names[i],
                issuer=issuer, isin=isin, link=l).save()
            print(f'Stored {i}: {long_names[i]} ({i}/{len(long_names)})')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
            i += 1

        print('Data has been successfuly stored!')
        return ''

    def china():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting get_etf_issuers.china()')
        print('Starting Selenium')
        url = 'https://www.investing.com/etfs/china-etfs?&issuer_filter=0'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        ChinaETFStaticInfo.objects.all().delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        long_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            long_names.append(link.a['title'])
        
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 'Hang Seng China Affiliated Corps (CCI) (HSCC)'
                short_name = short_name[::-1] # ')CCSH( )ICC( sproC detailiffA anihC gneS gnaH'
                short_name = short_name[short_name.index(')')+1:short_name.index('(')][::-1] # HSCC
                market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                markets = [m[0] for m in MARKETS_CH]
                issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                if market not in markets:
                    market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                    market = market.find_all('tr')
                    for tr in market:
                        if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                            market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                            break
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 'Hang Seng China Affiliated Corps (CCI) (HSCC)'
                    short_name = short_name[::-1] # ')CCSH( )ICC( sproC detailiffA anihC gneS gnaH'
                    short_name = short_name[short_name.index(')')+1:short_name.index('(')][::-1] # HSCC
                    market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                    markets = [m[0] for m in MARKETS_CH]
                    issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                    isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                    if market not in markets:
                        market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                        market = market.find_all('tr')
                        for tr in market:
                            if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                                market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                                break
                except:
                    continue

            ChinaETFStaticInfo(
                short_name=short_name, long_name=long_names[i],
                market=market, issuer=issuer, isin=isin, link=l).save()
            print(f'Stored {i}: {long_names[i]} ({i}/{len(long_names)})')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
            i += 1

        print('Data has been successfuly stored!')
        return ''

    def canada():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting get_etf_issuers.canada()')
        print('Starting Selenium')
        url = 'https://www.investing.com/etfs/canada-etfs?&issuer_filter=0'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        CanadaETFStaticInfo.objects.all().delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        long_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            long_names.append(link.a['title'])
        
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 'Hang Seng China Affiliated Corps (CCI) (HSCC)'
                short_name = short_name[::-1] # ')CCSH( )ICC( sproC detailiffA anihC gneS gnaH'
                short_name = short_name[short_name.index(')')+1:short_name.index('(')][::-1] # HSCC
                market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                markets = [m[0] for m in MARKETS_CA]
                issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                if market not in markets:
                    market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                    market = market.find_all('tr')
                    for tr in market:
                        if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                            market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                            break
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 'Hang Seng China Affiliated Corps (CCI) (HSCC)'
                    short_name = short_name[::-1] # ')CCSH( )ICC( sproC detailiffA anihC gneS gnaH'
                    short_name = short_name[short_name.index(')')+1:short_name.index('(')][::-1] # HSCC
                    market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                    markets = [m[0] for m in MARKETS_CA]
                    issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                    isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                    if market not in markets:
                        market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                        market = market.find_all('tr')
                        for tr in market:
                            if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                                market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                                break
                except:
                    continue

            CanadaETFStaticInfo(
                short_name=short_name, long_name=long_names[i],
                market=market, issuer=issuer, isin=isin, link=l).save()
            print(f'Stored {i}: {long_names[i]} ({i}/{len(long_names)})')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
            i += 1

        print('Data has been successfuly stored!')
        return ''

    def germany():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting get_etf_issuers.germany()')
        print('Starting Selenium')
        url = 'https://www.investing.com/etfs/germany-etfs?&issuer_filter=0'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        GermanyETFStaticInfo.objects.all().delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        long_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            long_names.append(link.a['title'])
        
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 'Hang Seng China Affiliated Corps (CCI) (HSCC)'
                short_name = short_name[::-1] # ')CCSH( )ICC( sproC detailiffA anihC gneS gnaH'
                short_name = short_name[short_name.index(')')+1:short_name.index('(')][::-1] # HSCC
                market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                markets = [m[0] for m in MARKETS_GE]
                issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                if market not in markets:
                    market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                    market = market.find_all('tr')
                    for tr in market:
                        if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                            market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                            break
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 'Hang Seng China Affiliated Corps (CCI) (HSCC)'
                    short_name = short_name[::-1] # ')CCSH( )ICC( sproC detailiffA anihC gneS gnaH'
                    short_name = short_name[short_name.index(')')+1:short_name.index('(')][::-1] # HSCC
                    market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                    markets = [m[0] for m in MARKETS_GE]
                    issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                    isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                    if market not in markets:
                        market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                        market = market.find_all('tr')
                        for tr in market:
                            if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                                market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                                break
                except:
                    continue

            GermanyETFStaticInfo(
                short_name=short_name, long_name=long_names[i],
                market=market, issuer=issuer, isin=isin, link=l).save()
            print(f'Stored {i}: {long_names[i]} ({i}/{len(long_names)})')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
            i += 1

        print('Data has been successfuly stored!')
        return ''

    def australia():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting get_etf_issuers.australia()')
        print('Starting Selenium')
        url = 'https://www.investing.com/etfs/australia-etfs?&issuer_filter=0'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        AustraliaETFStaticInfo.objects.all().delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        long_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            long_names.append(link.a['title'])
        
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 'Hang Seng China Affiliated Corps (CCI) (HSCC)'
                short_name = short_name[::-1] # ')CCSH( )ICC( sproC detailiffA anihC gneS gnaH'
                short_name = short_name[short_name.index(')')+1:short_name.index('(')][::-1] # HSCC
                issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 'Hang Seng China Affiliated Corps (CCI) (HSCC)'
                    short_name = short_name[::-1] # ')CCSH( )ICC( sproC detailiffA anihC gneS gnaH'
                    short_name = short_name[short_name.index(')')+1:short_name.index('(')][::-1] # HSCC
                    issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                    isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                except:
                    continue

            AustraliaETFStaticInfo(
                short_name=short_name, long_name=long_names[i],
                issuer=issuer, isin=isin, link=l).save()
            print(f'Stored {i}: {long_names[i]} ({i}/{len(long_names)})')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
            i += 1

        print('Data has been successfuly stored!')
        return ''

# Used for collecting bonds static info
class CollectBondStaticInfo:
    def all():
        print('Starting CollectBondStaticInfo')
        print('Starting to collect for United States')
        CollectBondStaticInfo.us()
        print('Starting to collect for Japan')
        CollectBondStaticInfo.japan()
        print('Starting to collect for United Kingdom')
        CollectBondStaticInfo.uk()
        print('Starting to collect for Honk Kong')
        CollectBondStaticInfo.hk()
        print('Starting to collect for China')
        CollectBondStaticInfo.china()
        print('Starting to collect for Canada')
        CollectBondStaticInfo.canada()
        print('Starting to collect for Germany')
        CollectBondStaticInfo.germany()
        print('Starting to collect for Australia')
        CollectBondStaticInfo.australia()


    def us():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectBondStaticInfo.us()')
        print('Starting Selenium')
        url = 'https://www.investing.com/rates-bonds/usa-government-bonds?maturity_from=40&maturity_to=290'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        USBondStaticInfo.objects.all().delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        long_names = []
        short_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            short_names.append(link.a.get_text())
            long_names.append(link.a['title']+' Bond Yield')
        
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                markets = [m[0] for m in MARKETS_US]
                if market not in markets:
                    market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                    market = market.find_all('tr')
                    for tr in market:
                        if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                            market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                            break
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                    markets = [m[0] for m in MARKETS_US]
                    if market not in markets:
                        market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                        market = market.find_all('tr')
                        for tr in market:
                            if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                                market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                                break
                except:
                    continue
            USBondStaticInfo(
                short_name=short_names[i], long_name=long_names[i],
                market=market, link=l).save()
            print(f'Stored {i}: {long_names[i]} ({i}/{len(long_names)})')
            if i % 100 == 0:
                print (f'{len(links)-i} bonds left')
            i += 1
        print('Data has been successfuly stored!')
        return ''

    def japan():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectBondStaticInfo.japan()')
        print('Starting Selenium')
        url = 'https://www.investing.com/rates-bonds/japan-government-bonds?maturity_from=40&maturity_to=300'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        JapanBondStaticInfo.objects.all().delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        long_names = []
        short_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            short_names.append(link.a.get_text())
            long_names.append(link.a['title']+' Bond Yield')
        
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                markets = [m[0] for m in MARKETS_JP]
                if market not in markets:
                    market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                    market = market.find_all('tr')
                    for tr in market:
                        if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                            market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                            break
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                    markets = [m[0] for m in MARKETS_JP]
                    if market not in markets:
                        market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                        market = market.find_all('tr')
                        for tr in market:
                            if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                                market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                                break
                except:
                    continue
            JapanBondStaticInfo(
                short_name=short_names[i], long_name=long_names[i],
                market=market, link=l).save()
            print(f'Stored {i}: {long_names[i]} ({i}/{len(long_names)})')
            if i % 100 == 0:
                print (f'{len(links)-i} bonds left')
            i += 1

        print('Data has been successfuly stored!')
        return ''

    def uk():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectBondStaticInfo.uk()')
        print('Starting Selenium')
        url = 'https://www.investing.com/rates-bonds/uk-government-bonds?maturity_from=40&maturity_to=310'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        UKBondStaticInfo.objects.all().delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        long_names = []
        short_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            short_names.append(link.a.get_text())
            long_names.append(link.a['title']+' Bond Yield')
        
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                except:
                    continue
            UKBondStaticInfo(
                short_name=short_names[i], long_name=long_names[i], link=l).save()
            print(f'Stored {i}: {long_names[i]} ({i}/{len(long_names)})')
            if i % 100 == 0:
                print (f'{len(links)-i} bonds left')
            i += 1

        print('Data has been successfuly stored!')
        return ''

    def hk():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectBondStaticInfo.hk()')
        print('Starting Selenium')
        url = 'https://www.investing.com/rates-bonds/hong-kong-government-bonds?maturity_from=20&maturity_to=230'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        HKBondStaticInfo.objects.all().delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        long_names = []
        short_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            short_names.append(link.a.get_text())
            long_names.append(link.a['title']+' Bond Yield')
        
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                except:
                    continue
            HKBondStaticInfo(
                short_name=short_names[i], long_name=long_names[i], link=l).save()
            print(f'Stored {i}: {long_names[i]} ({i}/{len(long_names)})')
            if i % 100 == 0:
                print (f'{len(links)-i} bonds left')
            i += 1

        print('Data has been successfuly stored!')
        return ''

    def china():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectBondStaticInfo.china()')
        print('Starting Selenium')
        url = 'https://www.investing.com/rates-bonds/china-government-bonds?maturity_from=90&maturity_to=290'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        ChinaBondStaticInfo.objects.all().delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        long_names = []
        short_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            short_names.append(link.a.get_text())
            long_names.append(link.a['title']+' Bond Yield')
        
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                markets = [m[0] for m in MARKETS_CH]
                if market not in markets:
                    market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                    market = market.find_all('tr')
                    for tr in market:
                        if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                            market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                            break
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                    markets = [m[0] for m in MARKETS_CH]
                    if market not in markets:
                        market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                        market = market.find_all('tr')
                        for tr in market:
                            if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                                market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                                break
                except:
                    continue
            ChinaBondStaticInfo(
                short_name=short_names[i], long_name=long_names[i],
                market=market, link=l).save()
            print(f'Stored {i}: {long_names[i]} ({i}/{len(long_names)})')
            if i % 100 == 0:
                print (f'{len(links)-i} bonds left')
            i += 1

        print('Data has been successfuly stored!')
        return ''

    def canada():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectBondStaticInfo.canada()')
        print('Starting Selenium')
        url = 'https://www.investing.com/rates-bonds/canada-government-bonds?maturity_from=40&maturity_to=290'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        CanadaBondStaticInfo.objects.all().delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        long_names = []
        short_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            short_names.append(link.a.get_text())
            long_names.append(link.a['title']+' Bond Yield')
        
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                markets = [m[0] for m in MARKETS_CA]
                if market not in markets:
                    market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                    market = market.find_all('tr')
                    for tr in market:
                        if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                            market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                            break
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                    markets = [m[0] for m in MARKETS_CA]
                    if market not in markets:
                        market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                        market = market.find_all('tr')
                        for tr in market:
                            if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                                market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                                break
                except:
                    continue
            CanadaBondStaticInfo(
                short_name=short_names[i], long_name=long_names[i],
                market=market, link=l).save()
            print(f'Stored {i}: {long_names[i]} ({i}/{len(long_names)})')
            if i % 100 == 0:
                print (f'{len(links)-i} bonds left')
            i += 1

        print('Data has been successfuly stored!')
        return ''

    def germany():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectBondStaticInfo.germany()')
        print('Starting Selenium')
        url = 'https://www.investing.com/rates-bonds/germany-government-bonds?maturity_from=40&maturity_to=290'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        GermanyBondStaticInfo.objects.all().delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        long_names = []
        short_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            short_names.append(link.a.get_text())
            long_names.append(link.a['title']+' Bond Yield')
        
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                markets = [m[0] for m in MARKETS_GE]
                if market not in markets:
                    market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                    market = market.find_all('tr')
                    for tr in market:
                        if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                            market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                            break
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                    markets = [m[0] for m in MARKETS_GE]
                    if market not in markets:
                        market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                        market = market.find_all('tr')
                        for tr in market:
                            if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                                market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                                break
                except:
                    continue
            GermanyBondStaticInfo(
                short_name=short_names[i], long_name=long_names[i],
                market=market, link=l).save()
            print(f'Stored {i}: {long_names[i]} ({i}/{len(long_names)})')
            if i % 100 == 0:
                print (f'{len(links)-i} bonds left')
            i += 1

        print('Data has been successfuly stored!')
        return ''

    def australia():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectBondStaticInfo.australia()')
        print('Starting Selenium')
        url = 'https://www.investing.com/rates-bonds/australia-government-bonds?maturity_from=40&maturity_to=290'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        AustraliaBondStaticInfo.objects.all().delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        long_names = []
        short_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            short_names.append(link.a.get_text())
            long_names.append(link.a['title']+' Bond Yield')
        
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                except:
                    continue
            AustraliaBondStaticInfo(
                short_name=short_names[i], long_name=long_names[i], link=l).save()
            print(f'Stored {i}: {long_names[i]} ({i}/{len(long_names)})')
            if i % 100 == 0:
                print (f'{len(links)-i} bonds left')
            i += 1

        print('Data has been successfuly stored!')
        return ''

# Used for collecting funds' issuers
class CollectFundIssuers:
    def all():
        print('Starting to Collect Fund Issuers for United States')
        CollectFundIssuers.us()
        print('Starting to Collect Fund Issuers for Japan')
        CollectFundIssuers.japan()
        print('Starting to Collect Fund Issuers for United Kingdom')
        CollectFundIssuers.uk()
        print('Starting to Collect Fund Issuers for Honk Kong')
        CollectFundIssuers.hk()
        print('Starting to Collect Fund Issuers for China')
        CollectFundIssuers.china()
        print('Starting to Collect Fund Issuers for Canada')
        CollectFundIssuers.canada()
        print('Starting to Collect Fund Issuers for Germany')
        CollectFundIssuers.germany()
        print('Starting to Collect Fund Issuers for Australia')
        CollectFundIssuers.australia()
    
    def us():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectFundIssuers.us()')
        print('Starting Selenium')
        url = 'https://www.investing.com/funds/usa-funds?&issuer_filter=0'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        FundIssuers.objects.filter(country='US').delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and collect issuers info')
        i = 0
        issuers = []
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                except:
                    continue
            print(f'Visited {i}/{len(links)-1}')
            i += 1
            issuers.append(issuer)
        issuers = list(set(issuers))
        print(f'Longest Issuer Name: {len(max(issuers, key=len))}')
        for issuer in issuers:
            FundIssuers(country='US', name=issuer).save()
        return ''

    def japan():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectFundIssuers.japan()')
        print('Starting Selenium')
        url = 'https://www.investing.com/funds/japan-funds?&issuer_filter=0'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        FundIssuers.objects.filter(country='JP').delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and collect issuers info')
        i = 0
        issuers = []
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                except:
                    continue
            print(f'Visited {i}/{len(links)-1}')
            i += 1
            issuers.append(issuer)
        issuers = list(set(issuers))
        print(f'Longest Issuer Name: {len(max(issuers, key=len))}')
        for issuer in issuers:
            FundIssuers(country='JP', name=issuer).save()
        return ''

    def uk():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectFundIssuers.uk()')
        print('Starting Selenium')
        url = 'https://www.investing.com/funds/uk-funds?&issuer_filter=0'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        FundIssuers.objects.filter(country='UK').delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and collect issuers info')
        i = 0
        issuers = []
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                except:
                    continue
            print(f'Visited {i}/{len(links)-1}')
            i += 1
            issuers.append(issuer)
        issuers = list(set(issuers))
        print(f'Longest Issuer Name: {len(max(issuers, key=len))}')
        for issuer in issuers:
            FundIssuers(country='UK', name=issuer).save()
        return ''

    def hk():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectFundIssuers.hk()')
        print('Starting Selenium')
        url = 'https://www.investing.com/funds/hong-kong-funds?&issuer_filter=0'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        FundIssuers.objects.filter(country='HK').delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and collect issuers info')
        i = 0
        issuers = []
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                except:
                    continue
            print(f'Visited {i}/{len(links)-1}')
            i += 1
            issuers.append(issuer)
        issuers = list(set(issuers))
        print(f'Longest Issuer Name: {len(max(issuers, key=len))}')
        for issuer in issuers:
            FundIssuers(country='HK', name=issuer).save()
        return ''

    def china():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectFundIssuers.china()')
        print('Starting Selenium')
        url = 'https://www.investing.com/funds/china-funds?&issuer_filter=0'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        FundIssuers.objects.filter(country='CH').delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and collect issuers info')
        i = 0
        issuers = []
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                except:
                    continue
            print(f'Visited {i}/{len(links)-1}')
            i += 1
            issuers.append(issuer)
        issuers = list(set(issuers))
        print(f'Longest Issuer Name: {len(max(issuers, key=len))}')
        for issuer in issuers:
            FundIssuers(country='CH', name=issuer).save()
        return ''

    def canada():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectFundIssuers.canada()')
        print('Starting Selenium')
        url = 'https://www.investing.com/funds/canada-funds?&issuer_filter=0'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        FundIssuers.objects.filter(country='CA').delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and collect issuers info')
        i = 0
        issuers = []
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                except:
                    continue
            print(f'Visited {i}/{len(links)-1}')
            i += 1
            issuers.append(issuer)
        issuers = list(set(issuers))
        print(f'Longest Issuer Name: {len(max(issuers, key=len))}')
        for issuer in issuers:
            FundIssuers(country='CA', name=issuer).save()
        return ''

    def germany():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectFundIssuers.germany()')
        print('Starting Selenium')
        url = 'https://www.investing.com/funds/germany-funds?&issuer_filter=0'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        FundIssuers.objects.filter(country='GE').delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) CArome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and collect issuers info')
        i = 0
        issuers = []
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                except:
                    continue
            print(f'Visited {i}/{len(links)-1}')
            i += 1
            issuers.append(issuer)
        issuers = list(set(issuers))
        print(f'Longest Issuer Name: {len(max(issuers, key=len))}')
        for issuer in issuers:
            FundIssuers(country='GE', name=issuer).save()
        return ''

    def australia():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectFundIssuers.australia()')
        print('Starting Selenium')
        url = 'https://www.investing.com/funds/australia-funds?&issuer_filter=0'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        FundIssuers.objects.filter(country='AU').delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) CArome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and collect issuers info')
        i = 0
        issuers = []
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                except:
                    continue
            print(f'Visited {i}/{len(links)-1}')
            i += 1
            issuers.append(issuer)
        issuers = list(set(issuers))
        print(f'Longest Issuer Name: {len(max(issuers, key=len))}')
        for issuer in issuers:
            FundIssuers(country='AU', name=issuer).save()
        return ''

class CollectFundStaticInfo:
    fields_to_scrape = (
        'Inception Date', 'Min. Investment', 'Category')
    
    def all():
        print('Starting CollectFundStaticInfo')
        print('Starting to collect for United States')
        CollectFundStaticInfo.us()
        print('Starting to collect for Japan')
        CollectFundStaticInfo.japan()
        print('Starting to collect for United Kingdom')
        CollectFundStaticInfo.uk()
        print('Starting to collect for Honk Kong')
        CollectFundStaticInfo.hk()
        print('Starting to collect for China')
        CollectFundStaticInfo.china()
        print('Starting to collect for Canada')
        CollectFundStaticInfo.canada()
        print('Starting to collect for Germany')
        CollectFundStaticInfo.germany()
        print('Starting to collect for Australia')
        CollectFundStaticInfo.australia()

        
    def us():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectFundStaticInfo.us()')
        print('Starting Selenium')
        url = 'https://www.investing.com/funds/usa-funds?&issuer_filter=0'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        USFundStaticInfo.objects.all().delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        short_names = []
        long_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            short_names.append(link.find_next_sibling()['title'].strip())
            long_names.append(link.a['title'])
        
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                markets = [m[0] for m in MARKETS_US]
                if market not in markets:
                    market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                    market = market.find_all('tr')
                    for tr in market:
                        if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                            market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                            break
                soup = soup.find_all('span')
                fields = {}
                for field in soup:
                    if field.get_text() in CollectFundStaticInfo.fields_to_scrape:
                        if field.get_text() == 'Category':
                            try:
                                fields['Category Descrptn'] = field.next_sibling['data-tooltip']
                            except:
                                fields['Category Descrptn'] = ''
                        fields[field.get_text()] = field.next_sibling.get_text()
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                    isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                    market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                    markets = [m[0] for m in MARKETS_US]
                    if market not in markets:
                        market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                        market = market.find_all('tr')
                        for tr in market:
                            if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                                market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                                break
                    soup = soup.find_all('span')
                    fields = {}
                    for field in soup:
                        if field.get_text() in CollectFundStaticInfo.fields_to_scrape:
                            if field.get_text() == 'Category':
                                try:
                                    fields['Category Descrptn'] = field.next_sibling['data-tooltip']
                                except:
                                    fields['Category Descrptn'] = ''
                            fields[field.get_text()] = field.next_sibling.get_text()
                except:
                    continue

            if fields['Min. Investment'] == 'N/A':
                fields['Min. Investment'] = None # Will be converted to 'null' before postgresql automatically
            else:
                fields['Min. Investment'] = fields['Min. Investment'].replace(',', '').strip()

            USFundStaticInfo(
                short_name=short_names[i], long_name=long_names[i],
                market=market, issuer=issuer, isin=isin, link=l, 
                min_investment=fields['Min. Investment'],
                category=fields['Category'], category_descrptn=fields['Category Descrptn'],
                inception_date=datetime.datetime.strptime(fields['Inception Date'], '%b %d, %Y')).save()
            print(f'Stored {i}: {long_names[i]} ({i}/{len(long_names)})')
            i += 1

        print('Data has been successfuly stored!')
        return ''

    def japan():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectFundStaticInfo.japan()')
        print('Starting Selenium')
        url = 'https://www.investing.com/funds/japan-funds?&issuer_filter=0'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        JapanFundStaticInfo.objects.all().delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        short_names = []
        long_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            short_names.append(link.find_next_sibling()['title'].strip())
            long_names.append(link.a['title'])
        
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                markets = [m[0] for m in MARKETS_JP]
                if market not in markets:
                    market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                    market = market.find_all('tr')
                    for tr in market:
                        if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                            market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                            break
                soup = soup.find_all('span')
                fields = {}
                for field in soup:
                    if field.get_text() in CollectFundStaticInfo.fields_to_scrape:
                        if field.get_text() == 'Category':
                            try:
                                fields['Category Descrptn'] = field.next_sibling['data-tooltip']
                            except:
                                fields['Category Descrptn'] = ''
                        fields[field.get_text()] = field.next_sibling.get_text()
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                    isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                    market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                    markets = [m[0] for m in MARKETS_JP]
                    if market not in markets:
                        market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                        market = market.find_all('tr')
                        for tr in market:
                            if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                                market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                                break
                    soup = soup.find_all('span')
                    fields = {}
                    for field in soup:
                        if field.get_text() in CollectFundStaticInfo.fields_to_scrape:
                            if field.get_text() == 'Category':
                                try:
                                    fields['Category Descrptn'] = field.next_sibling['data-tooltip']
                                except:
                                    fields['Category Descrptn'] = ''
                            fields[field.get_text()] = field.next_sibling.get_text()
                except:
                    continue

            if fields['Min. Investment'] == 'N/A':
                fields['Min. Investment'] = None # Will be converted to 'null' before postgresql automatically
            else:
                fields['Min. Investment'] = fields['Min. Investment'].replace(',', '').strip()
            JapanFundStaticInfo(
                short_name=short_names[i], long_name=long_names[i],
                market=market, issuer=issuer, isin=isin, link=l, 
                min_investment=fields['Min. Investment'],
                category=fields['Category'], category_descrptn=fields['Category Descrptn'],
                inception_date=datetime.datetime.strptime(fields['Inception Date'], '%b %d, %Y')).save()
            print(f'Stored {i}: {long_names[i]} ({i}/{len(long_names)})')
            i += 1

        print('Data has been successfuly stored!')
        return ''

    def uk():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectFundStaticInfo.uk()')
        print('Starting Selenium')
        url = 'https://www.investing.com/funds/uk-funds?&issuer_filter=0'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        UKFundStaticInfo.objects.all().delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        short_names = []
        long_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            short_names.append(link.find_next_sibling()['title'].strip())
            long_names.append(link.a['title'])
        
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                soup = soup.find_all('span')
                fields = {}
                for field in soup:
                    if field.get_text() in CollectFundStaticInfo.fields_to_scrape:
                        if field.get_text() == 'Category':
                            try:
                                fields['Category Descrptn'] = field.next_sibling['data-tooltip']
                            except:
                                fields['Category Descrptn'] = ''
                        fields[field.get_text()] = field.next_sibling.get_text()
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                    isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                    soup = soup.find_all('span')
                    fields = {}
                    for field in soup:
                        if field.get_text() in CollectFundStaticInfo.fields_to_scrape:
                            if field.get_text() == 'Category':
                                try:
                                    fields['Category Descrptn'] = field.next_sibling['data-tooltip']
                                except:
                                    fields['Category Descrptn'] = ''
                            fields[field.get_text()] = field.next_sibling.get_text()
                except:
                    continue

            if fields['Min. Investment'] == 'N/A':
                fields['Min. Investment'] = None # Will be converted to 'null' before postgresql automatically
            else:
                fields['Min. Investment'] = fields['Min. Investment'].replace(',', '').strip()
            UKFundStaticInfo(
                short_name=short_names[i], long_name=long_names[i],
                issuer=issuer, isin=isin, link=l, 
                min_investment=fields['Min. Investment'],
                category=fields['Category'], category_descrptn=fields['Category Descrptn'],
                inception_date=datetime.datetime.strptime(fields['Inception Date'], '%b %d, %Y')).save()
            print(f'Stored {i}: {long_names[i]} ({i}/{len(long_names)})')
            i += 1

        print('Data has been successfuly stored!')
        return ''

    def hk():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectFundStaticInfo.hk()')
        print('Starting Selenium')
        url = 'https://www.investing.com/funds/hong-kong-funds?&issuer_filter=0'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        HKFundStaticInfo.objects.all().delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        short_names = []
        long_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            short_names.append(link.find_next_sibling()['title'].strip())
            long_names.append(link.a['title'])
        
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                soup = soup.find_all('span')
                fields = {}
                for field in soup:
                    if field.get_text() in CollectFundStaticInfo.fields_to_scrape:
                        if field.get_text() == 'Category':
                            try:
                                fields['Category Descrptn'] = field.next_sibling['data-tooltip']
                            except:
                                fields['Category Descrptn'] = ''
                        fields[field.get_text()] = field.next_sibling.get_text()
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                    isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                    soup = soup.find_all('span')
                    fields = {}
                    for field in soup:
                        if field.get_text() in CollectFundStaticInfo.fields_to_scrape:
                            if field.get_text() == 'Category':
                                try:
                                    fields['Category Descrptn'] = field.next_sibling['data-tooltip']
                                except:
                                    fields['Category Descrptn'] = ''
                            fields[field.get_text()] = field.next_sibling.get_text()
                except:
                    continue

            if fields['Min. Investment'] == 'N/A':
                fields['Min. Investment'] = None # Will be converted to 'null' before postgresql automatically
            else:
                fields['Min. Investment'] = fields['Min. Investment'].replace(',', '').strip()
            HKFundStaticInfo(
                short_name=short_names[i], long_name=long_names[i],
                issuer=issuer, isin=isin, link=l, 
                min_investment=fields['Min. Investment'],
                category=fields['Category'], category_descrptn=fields['Category Descrptn'],
                inception_date=datetime.datetime.strptime(fields['Inception Date'], '%b %d, %Y')).save()
            print(f'Stored {i}: {long_names[i]} ({i}/{len(long_names)})')
            i += 1

        print('Data has been successfuly stored!')
        return ''

    def china():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectFundStaticInfo.china()')
        print('Starting Selenium')
        url = 'https://www.investing.com/funds/china-funds?&issuer_filter=0'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        ChinaFundStaticInfo.objects.all().delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        short_names = []
        long_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            short_names.append(link.find_next_sibling()['title'].strip())
            long_names.append(link.a['title'])
        
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                markets = [m[0] for m in MARKETS_CH]
                if market not in markets:
                    market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                    market = market.find_all('tr')
                    for tr in market:
                        if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                            market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                            break
                soup = soup.find_all('span')
                fields = {}
                for field in soup:
                    if field.get_text() in CollectFundStaticInfo.fields_to_scrape:
                        if field.get_text() == 'Category':
                            try:
                                fields['Category Descrptn'] = field.next_sibling['data-tooltip']
                            except:
                                fields['Category Descrptn'] = ''
                        fields[field.get_text()] = field.next_sibling.get_text()
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                    isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                    market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                    markets = [m[0] for m in MARKETS_CH]
                    if market not in markets:
                        market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                        market = market.find_all('tr')
                        for tr in market:
                            if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                                market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                                break
                    soup = soup.find_all('span')
                    fields = {}
                    for field in soup:
                        if field.get_text() in CollectFundStaticInfo.fields_to_scrape:
                            if field.get_text() == 'Category':
                                try:
                                    fields['Category Descrptn'] = field.next_sibling['data-tooltip']
                                except:
                                    fields['Category Descrptn'] = ''
                            fields[field.get_text()] = field.next_sibling.get_text()
                except:
                    continue

            if fields['Min. Investment'] == 'N/A':
                fields['Min. Investment'] = None # Will be converted to 'null' before postgresql automatically
            else:
                fields['Min. Investment'] = fields['Min. Investment'].replace(',', '').strip()
            ChinaFundStaticInfo(
                short_name=short_names[i], long_name=long_names[i],
                market=market, issuer=issuer, isin=isin, link=l, 
                min_investment=fields['Min. Investment'],
                category=fields['Category'], category_descrptn=fields['Category Descrptn'],
                inception_date=datetime.datetime.strptime(fields['Inception Date'], '%b %d, %Y')).save()
            print(f'Stored {i}: {long_names[i]} ({i}/{len(long_names)})')
            i += 1

        print('Data has been successfuly stored!')
        return ''

    def canada():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectFundStaticInfo.canada()')
        print('Starting Selenium')
        url = 'https://www.investing.com/funds/canada-funds?&issuer_filter=0'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        CanadaFundStaticInfo.objects.all().delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        short_names = []
        long_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            short_names.append(link.find_next_sibling()['title'].strip())
            long_names.append(link.a['title'])
        
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                markets = [m[0] for m in MARKETS_CA]
                if market not in markets:
                    market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                    market = market.find_all('tr')
                    for tr in market:
                        if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                            market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                            break
                soup = soup.find_all('span')
                fields = {}
                for field in soup:
                    if field.get_text() in CollectFundStaticInfo.fields_to_scrape:
                        if field.get_text() == 'Category':
                            try:
                                fields['Category Descrptn'] = field.next_sibling['data-tooltip']
                            except:
                                fields['Category Descrptn'] = ''
                        fields[field.get_text()] = field.next_sibling.get_text()
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                    market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                    markets = [m[0] for m in MARKETS_CA]
                    if market not in markets:
                        market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                        market = market.find_all('tr')
                        for tr in market:
                            if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                                market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                                break
                    soup = soup.find_all('span')
                    fields = {}
                    for field in soup:
                        if field.get_text() in CollectFundStaticInfo.fields_to_scrape:
                            if field.get_text() == 'Category':
                                try:
                                    fields['Category Descrptn'] = field.next_sibling['data-tooltip']
                                except:
                                    fields['Category Descrptn'] = ''
                            fields[field.get_text()] = field.next_sibling.get_text()
                except:
                    continue

            if fields['Min. Investment'] == 'N/A':
                fields['Min. Investment'] = None # Will be converted to 'null' before postgresql automatically
            else:
                fields['Min. Investment'] = fields['Min. Investment'].replace(',', '').strip()
            CanadaFundStaticInfo(
                short_name=short_names[i], long_name=long_names[i],
                market=market, issuer=issuer, link=l, 
                min_investment=fields['Min. Investment'],
                category=fields['Category'], category_descrptn=fields['Category Descrptn'],
                inception_date=datetime.datetime.strptime(fields['Inception Date'], '%b %d, %Y')).save()
            print(f'Stored {i}: {long_names[i]} ({i}/{len(long_names)})')
            i += 1

        print('Data has been successfuly stored!')
        return ''

    def germany():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectFundStaticInfo.germany()')
        print('Starting Selenium')
        url = 'https://www.investing.com/funds/germany-funds?&issuer_filter=0'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        GermanyFundStaticInfo.objects.all().delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        short_names = []
        long_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            short_names.append(link.find_next_sibling()['title'].strip())
            long_names.append(link.a['title'])
        
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                markets = [m[0] for m in MARKETS_GE]
                if market not in markets:
                    market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                    market = market.find_all('tr')
                    for tr in market:
                        if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                            market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                            break
                soup = soup.find_all('span')
                fields = {}
                for field in soup:
                    if field.get_text() in CollectFundStaticInfo.fields_to_scrape:
                        if field.get_text() == 'Category':
                            try:
                                fields['Category Descrptn'] = field.next_sibling['data-tooltip']
                            except:
                                fields['Category Descrptn'] = ''
                        fields[field.get_text()] = field.next_sibling.get_text()
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                    isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                    market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                    markets = [m[0] for m in MARKETS_GE]
                    if market not in markets:
                        market = soup.find('table', class_='genTbl closedTbl exchangeDropdownTbl displayNone').tbody
                        market = market.find_all('tr')
                        for tr in market:
                            if tr.find('td', class_='left bold').find_next_sibling().get_text() in markets:
                                market = tr.find('td', class_='left bold').find_next_sibling().get_text()
                                break
                    soup = soup.find_all('span')
                    fields = {}
                    for field in soup:
                        if field.get_text() in CollectFundStaticInfo.fields_to_scrape:
                            if field.get_text() == 'Category':
                                try:
                                    fields['Category Descrptn'] = field.next_sibling['data-tooltip']
                                except:
                                    fields['Category Descrptn'] = ''
                            fields[field.get_text()] = field.next_sibling.get_text()
                except:
                    continue

            if fields['Min. Investment'] == 'N/A':
                fields['Min. Investment'] = None # Will be converted to 'null' before postgresql automatically
            else:
                fields['Min. Investment'] = fields['Min. Investment'].replace(',', '').strip()
            GermanyFundStaticInfo(
                short_name=short_names[i], long_name=long_names[i],
                market=market, issuer=issuer, isin=isin, link=l, 
                min_investment=fields['Min. Investment'],
                category=fields['Category'], category_descrptn=fields['Category Descrptn'],
                inception_date=datetime.datetime.strptime(fields['Inception Date'], '%b %d, %Y')).save()
            print(f'Stored {i}: {long_names[i]} ({i}/{len(long_names)})')
            i += 1

        print('Data has been successfuly stored!')
        return ''

    def australia():
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectFundStaticInfo.australia()')
        print('Starting Selenium')
        url = 'https://www.investing.com/funds/australia-funds?&issuer_filter=0'
        url2 = 'https://www.investing.com'
        # driver = webdriver.Chrome()
        driver.get(url)
        AustraliaFundStaticInfo.objects.all().delete()
        print('Removed old records starting to collect new ones')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print('Saved page source')
        print('Starting to collect links')
        links = []
        short_names = []
        long_names = []
        for link in soup.find_all('td', class_='bold left noWrap elp plusIconTd'):
            links.append(link.a['href'])
            short_names.append(link.find_next_sibling()['title'].strip())
            long_names.append(link.a['title'])
        
        header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
        print('Links are collected')
        print('Starting to visit them and store in database')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                soup = soup.find_all('span')
                fields = {}
                for field in soup:
                    if field.get_text() in CollectFundStaticInfo.fields_to_scrape:
                        if field.get_text() == 'Category':
                            try:
                                fields['Category Descrptn'] = field.next_sibling['data-tooltip']
                            except:
                                fields['Category Descrptn'] = ''
                        fields[field.get_text()] = field.next_sibling.get_text()
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    issuer = soup.find('span', text='Issuer:').find_next_sibling().get_text().strip()
                    soup = soup.find_all('span')
                    fields = {}
                    for field in soup:
                        if field.get_text() in CollectFundStaticInfo.fields_to_scrape:
                            if field.get_text() == 'Category':
                                try:
                                    fields['Category Descrptn'] = field.next_sibling['data-tooltip']
                                except:
                                    fields['Category Descrptn'] = ''
                            fields[field.get_text()] = field.next_sibling.get_text()
                except:
                    continue

            if fields['Min. Investment'] == 'N/A':
                fields['Min. Investment'] = None # Will be converted to 'null' before postgresql automatically
            else:
                fields['Min. Investment'] = fields['Min. Investment'].replace(',', '').strip()
            AustraliaFundStaticInfo(
                short_name=short_names[i], long_name=long_names[i],
                issuer=issuer, link=l, 
                min_investment=fields['Min. Investment'],
                category=fields['Category'], category_descrptn=fields['Category Descrptn'],
                inception_date=datetime.datetime.strptime(fields['Inception Date'], '%b %d, %Y')).save()
            print(f'Stored {i}: {long_names[i]} ({i}/{len(long_names)})')
            i += 1

        print('Data has been successfuly stored!')
        return ''