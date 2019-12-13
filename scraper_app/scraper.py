import requests
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from .models import (
    CommodityStaticInfo, CurrencyStaticInfo, CryptocurrencyStaticInfo, USStockStaticInfo, JapanStockStaticInfo,
    UKStockStaticInfo, HKStockStaticInfo, ChinaStockStaticInfo, CanadaStockStaticInfo, GermanyStockStaticInfo,
    AustraliaStockStaticInfo, 
    USIndexStaticInfo, JapanIndexStaticInfo, UKIndexStaticInfo, HKIndexStaticInfo, ChinaIndexStaticInfo
)
from .models import (
    MARKETS_USA, MARKETS_JPN, MARKETS_CH
)
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
                markets = [m[0] for m in MARKETS_USA]
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
                    markets = [m[0] for m in MARKETS_USA]
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
            i += 1
            print(f'Stored {i}: {long_names[i]}')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
        
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
                markets = [m[0] for m in MARKETS_JPN]
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
                    markets = [m[0] for m in MARKETS_JPN]
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
            i += 1
            print(f'Stored {i}: {long_names[i]}')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
        
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
                market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
            except:
                try:
                    print('Some Complications')
                    sleep(10) 
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 3M Company (MMM)
                    short_name = short_name[short_name.index('(')+1:].strip().replace(')', '') # MMM
                    market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                    isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                except:
                    continue
                    
            UKStockStaticInfo(
                short_name=short_name, long_name=long_names[i],
                isin=isin, link=l).save()
            i += 1
            print(f'Stored {i}: {long_names[i]}')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
        
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
            i += 1
            print(f'Stored {i}: {long_names[i]}')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
        
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
            i += 1
            print(f'Stored {i}: {long_names[i]}')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
        
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
                short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 3M Company (MMM)
                short_name = short_name[short_name.index('(')+1:].strip().replace(')', '') # MMM
                market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
            except:
                try:
                    print('Some Complications')
                    sleep(10) 
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 3M Company (MMM)
                    short_name = short_name[short_name.index('(')+1:].strip().replace(')', '') # MMM
                    market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                    isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                except:
                    continue
                    
            CanadaStockStaticInfo(
                short_name=short_name, long_name=long_names[i],
                isin=isin, market=market, link=l).save()
            i += 1
            print(f'Stored {i}: {long_names[i]}')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
        
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
        errors = []
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 3M Company (MMM)
                short_name = short_name[short_name.index('(')+1:].strip().replace(')', '') # MMM
                market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
            except:
                try:
                    print('Some Complications')
                    sleep(10) 
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 3M Company (MMM)
                    short_name = short_name[short_name.index('(')+1:].strip().replace(')', '') # MMM
                    market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                    isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                except:
                    continue
            GermanyStockStaticInfo(
                short_name=short_name, long_name=long_names[i],
                isin=isin, market=market, link=l).save()
            i += 1
            print(f'Stored {i}: {long_names[i]}')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
        
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
        errors = []
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 3M Company (MMM)
                short_name = short_name[short_name.index('(')+1:].strip().replace(')', '') # MMM
                market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
            except:
                try:
                    print('Some Complications')
                    sleep(10) 
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 3M Company (MMM)
                    short_name = short_name[short_name.index('(')+1:].strip().replace(')', '') # MMM
                    market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                    isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
                except:
                    continue
            AustraliaStockStaticInfo(
                short_name=short_name, long_name=long_names[i],
                isin=isin, link=l).save()
            i += 1
            print(f'Stored {i}: {long_names[i]}')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
        
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
        errors = []
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 3M Company (MMM)
                short_name = short_name[short_name.index('(')+1:].strip().replace(')', '') # MMM
                market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                markets = [m[0] for m in MARKETS_USA]
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
                    markets = [m[0] for m in MARKETS_USA]
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
            i += 1
            print(f'Stored {i}: {long_names[i]}')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
        
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
        errors = []
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 3M Company (MMM)
                short_name = short_name[short_name.index('(')+1:].strip().replace(')', '') # MMM
                market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
                markets = [m[0] for m in MARKETS_JPN]
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
                    markets = [m[0] for m in MARKETS_JPN]
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
            i += 1
            print(f'Stored {i}: {long_names[i]}')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
        
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
        errors = []
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
            i += 1
            print(f'Stored {i}: {long_names[i]}')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
        
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
        errors = []
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 'Hang Seng China Affiliated Corps (CCI) (HSCC)'
                short_name = short_name[::-1] # ')CCSH( )ICC( sproC detailiffA anihC gneS gnaH'
                short_name = short_name[short_name.index(')')+1:short_name.index('(')] # CCSH
            except:
                try:
                    print('Some Complication, sleeping for 10sec')
                    sleep(10)
                    request = requests.get(l, headers=header)
                    soup = BeautifulSoup(request.text, 'html.parser')
                    short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 'Hang Seng China Affiliated Corps (CCI) (HSCC)'
                    short_name = short_name[::-1] # ')CCSH( )ICC( sproC detailiffA anihC gneS gnaH'
                    short_name = short_name[short_name.index(')')+1:short_name.index('(')] # CCSH
                except:
                    continue
            HKIndexStaticInfo(
                short_name=short_name, long_name=long_names[i], link=l).save()
            i += 1
            print(f'Stored {i}: {long_names[i]}')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
        
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
        errors = []
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
                soup = BeautifulSoup(request.text, 'html.parser')
                short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 'Hang Seng China Affiliated Corps (CCI) (HSCC)'
                short_name = short_name[::-1] # ')CCSH( )ICC( sproC detailiffA anihC gneS gnaH'
                short_name = short_name[short_name.index(')')+1:short_name.index('(')] # CCSH
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
                    short_name = short_name[short_name.index(')')+1:short_name.index('(')] # CCSH
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
            i += 1
            print(f'Stored {i}: {long_names[i]}')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
        
        print('Data has been successfuly stored!')
        return ''