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

TABLE_LINKS = {
    # JS Scripts are not used to access the table
    'Commodities': 'https://www.investing.com/commodities/',
    'Currencies': 'https://www.investing.com/currencies/',
    'Cryptocurrencies': 'https://www.investing.com/crypto/',
    # Stocks - Same JS Scripts
    'US Stocks': 'https://www.investing.com/equities/united-states',
    'Japan Stocks': 'https://www.investing.com/equities/japan',
    'UK Stocks': 'https://www.investing.com/equities/united-kingdom',
    'HK Stocks': 'https://www.investing.com/equities/hong-kong',
    'China Stocks': 'https://www.investing.com/equities/china',
    'Canada Stocks': 'https://www.investing.com/equities/canada',
    'Germany Stocks': 'https://www.investing.com/equities/germany',
    'Australia Stocks': 'https://www.investing.com/equities/australia',
    # Indices - JS is not used, URLs contain all needed details
    'US Indices': 'https://www.investing.com/indices/usa-indices?&majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on',
    'Japan Indices': 'https://www.investing.com/indices/japan-indices?majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on',
    'UK Indices': 'https://www.investing.com/indices/uk-indices?majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on',
    'HK Indices': 'https://www.investing.com/indices/hong-kong-indices?majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on',
    'China Indices': 'https://www.investing.com/indices/china-indices?&majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on',
    'Canada Indices': 'https://www.investing.com/indices/canada-indices?majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on',
    'Germany Indices': 'https://www.investing.com/indices/germany-indices?majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on',
    'Australia Indices': 'https://www.investing.com/indices/australia-indices?majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on',
    # ETFs - JS is not used, URLs contain all needed details
    'US ETFs': 'https://www.investing.com/etfs/usa-etfs?&issuer_filter=0',
    'Japan ETFs': 'https://www.investing.com/etfs/japan-etfs?&issuer_filter=0',
    'UK ETFs': 'https://www.investing.com/etfs/uk-etfs?&issuer_filter=0',
    'HK ETFs': 'https://www.investing.com/etfs/hong-kong-etfs?&issuer_filter=0',
    'China ETFs': 'https://www.investing.com/etfs/china-etfs?&issuer_filter=0',
    'Canada ETFs': 'https://www.investing.com/etfs/canada-etfs?&issuer_filter=0',
    'Germany ETFs': 'https://www.investing.com/etfs/germany-etfs?&issuer_filter=0',
    'Australia ETFs': 'https://www.investing.com/etfs/australia-etfs?&issuer_filter=0',
    # Bonds - JS is not used, URLs contain all needed details
    'US Bonds': 'https://www.investing.com/rates-bonds/usa-government-bonds?maturity_from=40&maturity_to=290',
    'Japan Bonds': 'https://www.investing.com/rates-bonds/japan-government-bonds?maturity_from=40&maturity_to=300',
    'UK Bonds': 'https://www.investing.com/rates-bonds/uk-government-bonds?maturity_from=40&maturity_to=310',
    'HK Bonds': 'https://www.investing.com/rates-bonds/hong-kong-government-bonds?maturity_from=20&maturity_to=230',
    'China Bonds': 'https://www.investing.com/rates-bonds/china-government-bonds?maturity_from=90&maturity_to=290',
    'Canada Bonds': 'https://www.investing.com/rates-bonds/canada-government-bonds?maturity_from=40&maturity_to=290',
    'Germany Bonds': 'https://www.investing.com/rates-bonds/germany-government-bonds?maturity_from=40&maturity_to=290',
    'Australia Bonds': 'https://www.investing.com/rates-bonds/australia-government-bonds?maturity_from=40&maturity_to=290',
    # Funds - JS is not used, URLs contain all needed details
    'US Funds': 'https://www.investing.com/funds/usa-funds?&issuer_filter=0',
    'Japan Funds': 'https://www.investing.com/funds/japan-funds?&issuer_filter=0',
    'UK Funds': 'https://www.investing.com/funds/uk-funds?&issuer_filter=0',
    'HK Funds': 'https://www.investing.com/funds/hong-kong-funds?&issuer_filter=0',
    'China Funds': 'https://www.investing.com/funds/china-funds?&issuer_filter=0',
    'Canada Funds': 'https://www.investing.com/funds/canada-funds?&issuer_filter=0',
    'Germany Funds': 'https://www.investing.com/funds/germany-funds?&issuer_filter=0',
    'Australia Funds': 'https://www.investing.com/funds/australia-funds?&issuer_filter=0',
}

class CollectAllAssetsLive:
# CollectAllAssetsLive.commodities()
# CollectAllAssetsLive.currencies()
# CollectAllAssetsLive.cryptocurrencies()
# CollectAllAssetsLive.stocks()
# CollectAllAssetsLive.indices()
# CollectAllAssetsLive.etfs()
# CollectAllAssetsLive.bonds()
# CollectAllAssetsLive.funds()
    def commodities():
        print('Starting CollectAllAssetsLive.commodities()')
        #--------------------VPS------------------
        display = Display(visible=0, size=(800, 600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        #-----------------------------------------
        url = TABLE_LINKS['Commodities']
        driver.get(url)