import requests
from bs4 import BeautifulSoup
from time import sleep
from .models import CommodityStaticInfo, CurrencyStaticInfo, CryptoCurrencyStaticInfo

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
        CryptoCurrencyStaticInfo.objects.all().delete()
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
            CryptoCurrencyStaticInfo(
                short_name=short_names[i], long_name=long_names[i],
                link=links[i]).save()
        
        print('Data has been successfuly stored!')
        return ''
            