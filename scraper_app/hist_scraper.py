"""
1. Visit the link
2. Go from 1M to Max (if not found) switch to the next link
3. Go through ages and execute js scripts 
(time frame, start date, waiting until the table is fully loaded)
4. Take appropriate Django model and save an instance
"""
import datetime, time
from bs4 import BeautifulSoup
from time import sleep
from .scraper_functions import (
    vps_selenium_setup, execute_js_scripts, validate_price, print_exception)
from .scraper_data import STATIC_OBJECTS
from .models import (
    AllAssetsHistoricalMax, AllAssetsHistorical5Y, AllAssetsHistorical1Y, AllAssetsHistorical6M1M)


driver = vps_selenium_setup()
print('Driver is ready!')

data_ages = ['1M', '3M', '6M', '1Y', '5Y', 'Max']
hist_objects = {
    '1M': AllAssetsHistorical6M1M, '3M': AllAssetsHistorical6M1M, '6M': AllAssetsHistorical6M1M, 
    '1Y': AllAssetsHistorical1Y, '5Y': AllAssetsHistorical5Y, 'Max': AllAssetsHistoricalMax}

# Deleting old historical data
for obj in hist_objects.values():
    obj.objects.all().delete()
print('Old data has been removed')

start = time.time()
try:
    for key, value in STATIC_OBJECTS.items():
        if value['type'] == 'crptcrncy':
            hist_link = '/historical-data'
        else:
            hist_link = '-historical-data'

        obj_list = value['object'].objects.values_list('short_name', 'link')
        quanity = len(obj_list)

        for obj in obj_list:
            link = obj[1]
            if link is None:
                continue
            if '?cid' in link:
                cid = link[link.index('?cid'):]
                link = link[:link.index('?cid')]
                link += hist_link + cid
            else:
                link += hist_link
            driver.get(link)
            for data_age in data_ages:
                while True:
                    try: 
                        print(link)
                        soup = BeautifulSoup(driver.page_source, 'html.parser')
                        table = soup.find(class_='genTbl closedTbl historicalTbl')
                        trs = table.tbody.find_all('tr')
                        if trs[0].td.get_text() == 'No results found':
                            print('No results found')
                            break
                        
                        execute_js_scripts(driver, data_age)
                        
                        while True:
                            try:
                                soup = BeautifulSoup(driver.page_source, 'html.parser')
                                table = soup.find(class_='genTbl closedTbl historicalTbl')
                                trs = table.tbody.find_all('tr')
                                break
                            except Exception as e:
                                print_exception(e)
                                sleep(1)
                        
                        for row in trs:
                            data = row.find_all('td')
                            data = [d.get_text() for d in data]
                            
                            Type = value['type']
                            short_name = obj[0]
                            if data_age == 'Max':
                                date = datetime.datetime.strptime(data[0], '%b %y')
                            else:
                                date = datetime.datetime.strptime(data[0], '%b %d, %Y')
                            price = validate_price(data[1])
                            price = price[:price.index('.')+2+1]
                            if value['type'] in 'crncybndfnd':
                                volume = None
                                change_perc = data[5][:-1] # Removing % symbo
                            else:
                                volume = data[5]
                                if volume == '-':
                                    volume = None
                                change_perc = data[6][:-1] # Removing % symbo
                            
                            hist_objects[data_age]( 
                                Type=Type, 
                                short_name=short_name,
                                link=link,
                                date=date, 
                                price=price,
                                volume=volume).save()
                        print(f'({key})Stored {short_name} {data_age}')
                        break
                    except Exception as e:
                        print_exception(e)
                        sleep(1)
                        pass
finally:
    driver.quit()
    print('Driver is closed!')
    print(f'Executed in {time.time()-start} seconds.')                    