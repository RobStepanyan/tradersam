import requests
from bs4 import BeautifulSoup
from time import sleep
from .models import CommodityStaticInfo

class CollectStaticInfo:
    def commodities():
        print('Starting CollectStaticInfo.commodities()')
        short_names = []
        links = []
        url = 'https://www.investing.com/commodities/'
        url2 = 'https://www.investing.com'
        header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'}
        request = requests.get(url, headers=header)
        soup = BeautifulSoup(request.text, 'html.parser')
        soup = soup.find_all('td', class_='noWrap bold left noWrap')
        print('Collected names and links')
        fields_to_scrape = CommodityStaticInfo.fields_to_scrape

        for td in soup:
            short_names.append(td.find('a').get_text())
            links.append(url2+str(td.a['href']))

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
            CommodityStaticInfo(
                short_name=static_info['Short Name'], base_symbol=static_info['Base Symbol'],
                contract_size=static_info['Contract Size'],
                tick_size=static_info['Tick Size'], tick_value=static_info['Tick Value'],
                months=static_info['Months'], point_value=static_info['Point Value'],
                link=static_info['Link']).save()
        print('Data has been successfuly stored!')
        return ''