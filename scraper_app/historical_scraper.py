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
        # returns a list of tuples
        c_list = CommodityStaticInfo.objects.values_list('country', 'short_name', 'link')
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        print('Starting CollectAllAssetsHistoricalMax.commodities()')
        print('Removing old records')
        delete = input('Are you sure you want to delete all the old records, and scrape new ones? Press Y or y to continue: ')
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
            driver.get(url)
            print('Executing JS scripts')
            driver.execute_script('$("#data_interval").val("Monthly")')
            driver.execute_script('$("#widgetFieldDateRange").click();')
            driver.execute_script('$("#startDate").val("01/01/1980");')
            driver.execute_script('$("#applyBtn").click()')
            print('Executed JS scripts, sleeping for 5 seconds')
            sleep(5)
        driver.quit()