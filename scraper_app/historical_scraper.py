import requests, os, datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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
    AllAssetsHistoricalMax,
)

class CollectAllAssetsHistoricalMax:
# Start US
# Start commodities
# go through commodities' links
# generate historical data links
# visit a link
# Execute JS
# Collect Data and Save in AllAssetsHistoricalData
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
            print('Removing old records')
            if delete.upper() != 'Y':
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
            print('Removing old records')
            if delete.upper() != 'Y':
                print('Closing CollectAllAssetsHistoricalMax.currencies()') #change here
                return ''
            AllAssetsHistoricalMax.objects.filter(Type='crncy').delete() #change here
            print('Old records have been removed')
            print('Starting to collect new ones')
            print('Starting Selenium')
            # driver = webdriver.Chrome()
            for i in c_list:
                link = i[1] + '-historical-data' #change here
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