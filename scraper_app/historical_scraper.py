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
# download csv to unstored
# Import data from csv to db (AllAssetsHistoricalData)
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
            for link in c_list:
                link = link[2] + '-historical-data'
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
                    print(data)
        finally:
            ('Quiting the driver')
            driver.quit()
        print('Downloaded Successfuly')