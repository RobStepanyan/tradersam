import requests
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from .models import (
    CommodityStaticInfo, CurrencyStaticInfo, CryptocurrencyStaticInfo, USStockStaticInfo, JapanStockStaticInfo
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
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(chrome_options=options)
        print('Starting CollectStaticInfo.usstocks()')
        print('Removing old records')
        dd = input('Are you sure you want to delete all the old records, and scrape new ones? Press Y or y to continue: ')
        if dd.upper() != 'Y':
            print('Closing CollectStaticInfo.usstocks()')
            return ''
        # USStockStaticInfo.objects.all().delete()
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
        short_names, markets, isins = [], [], []
        print('Links are collected')
        print('Starting to visit them and store in databse')
        i = 0
        for link in links:
            l = url2 + link
            request = requests.get(l, headers=header)
            soup = BeautifulSoup(request.text, 'html.parser')
            short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 3M Company (MMM)
            short_name = short_name[short_name.index('(')+1:].strip().replace(')', '') # MMM
            short_names.append(short_name)
            market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
            markets.append(market)
            isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
            isins.append(isin)
            
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
        # display = Display(visible=0, size=(800, 600))
        # display.start()
        # options = webdriver.ChromeOptions()
        # options.add_argument('--no-sandbox')
        # driver = webdriver.Chrome(chrome_options=options)
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
        driver = webdriver.Chrome()
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
        short_names, markets, isins = [], [], []
        print('Links are collected')
        print('Starting to visit them and store in databse')
        i = 0
        for link in links:
            sleep(1)
            l = url2 + link
            try:
                request = requests.get(l, headers=header)
            except:
                pass
            soup = BeautifulSoup(request.text, 'html.parser')
            short_name = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text() # 3M Company (MMM)
            short_name = short_name[short_name.index('(')+1:].strip().replace(')', '') # MMM
            short_names.append(short_name)
            market = soup.find('i', class_='btnTextDropDwn arial_12 bold').get_text()
            markets.append(market)
            isin = soup.find('span', text='ISIN:').find_next_sibling().get_text().strip()
            isins.append(isin)
            
            JapanStockStaticInfo(
                short_name=short_name, long_name=long_names[i],
                market=market, isin=isin, link=l).save()
            i += 1
            print(f'Stored {i}: {long_names[i]}')
            if i % 100 == 0:
                print (f'{len(links)-i} equities left')
        
        print('Data has been successfuly stored!')
        return ''