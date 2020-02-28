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
    # Historical
    AllAssetsHistoricalMax, AllAssetsHistorical5Y, AllAssetsHistorical5D, AllAssetsHistorical1D,
    # Live
    AllAssetsBeforeLive, AllAssetsLive, AllAssetsAfterLive
)

TABLE_LINKS = {
    # JS Scripts are not used to access the table
    'Commodities': 'https://www.investing.com/commodities/real-time-futures',
    'Currencies': 'https://www.investing.com/currencies/',
    'Cryptocurrencies': 'https://www.investing.com/crypto/currencies',
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
table_class = 'genTbl closedTbl crossRatesTbl'
table_class1 = 'genTbl closedTbl crossRatesTbl elpTbl elp25' 
table_class2 = 'genTbl closedTbl crossRatesTbl elpTbl elp30' 
table_class3 = 'genTbl closedTbl crossRatesTbl elpTbl elp40' 

# Live fields to be collected
before_live_fields = ['Prev. Close']
# live is different for everyone, check STATIC_OBJECTS

#  All unique items of live_fields
#  ['Chg. %', 'Open', 'Chg.', 'Vol.', 'Market Cap', 'Yield', 
# 'Total Vol', 'Total Assets', 'Month', 'Low', 'Last', 
# 'High', 'Chg (7D)', 'Time']
live_fields = {
    'Commodities': ['Month', 'Last', 'High', 'Low', 'Chg.', 'Chg. %', 'Time'],
    'Currencies': ['Last', 'Open', 'High', 'Low', 'Chg.', 'Chg. %', 'Time'], 
    'Cryptocurrencies': ['Last', 'Market Cap', 'Vol.', 'Total Vol.', 'Chg. %', 'Chg (7D)'], 
    'Stocks': ['Last', 'High', 'Low', 'Chg.', 'Chg. %', 'Vol.', 'Time'],
    'Indices': ['Last', 'High', 'Low', 'Chg.', 'Chg. %', 'Time'],
    'ETFs': ['Last', 'Chg. %', 'Vol.', 'Time'],
    'Bonds': ['Yield', 'Prev. Close', 'High', 'Low', 'Chg.', 'Chg. %', 'Time'],
    'Funds': ['Last', 'Chg. %', 'Total Assets', 'Time']
}

# All unique values of after_live_fields
# ['P/E Ratio', 'Coupon', 'Dividend Yield', 'Shares Outstanding', 
# 'Average Vol. (3m)', 'Beta', 'Next Earnings Date', 'Max Supply', 'Volume', 
# 'Dividends (TTM)', 'Price Range', 'ROE', 'Market Cap', 'Rating', 'Maturity Date', 
# 'Total Assets', 'TTM Yield', '52 wk Range', 'Revenue', 'Dividend (Yield)', 
# '1-Year Change', 'Price Open', 'ROA', 'Price', 'Turnover', "Day's Range", 
# 'Expenses', 'ROI (TTM)', 'Circulating Supply', 'Risk Rating', 'Last Rollover Day', 
# 'Months', 'Settlement Day', 'Asset Class', 'EPS']
after_live_fields = {
    'Commodities': ['Day\'s Range', '52 wk Range', '1-Year Change',
    'Last Rollover Day', 'Settlement Day', 'Months'],
    
    'Currencies': ['1-Year Change', 'Day\'s Range', '52 wk Range'],
    
    'Cryptocurrencies': ['Circulating Supply', 'Max Supply', 'Day\'s Range'],
    
    'Stocks': ['Average Vol. (3m)', '1-Year Change', 'Day\'s Range', '52 wk Range',
    'Market Cap', 'P/E Ratio', 'Shares Outstanding', 'Revenue', 'EPS',
    'Dividend (Yield)', 'Beta', 'Next Earnings Date'],

    'Indices': ['1-Year Change', 'Volume', 'Average Vol. (3m)', 'Day\'s Range',
    '52 wk Range'],

    'ETFs': ['Average Vol. (3m)', '1-Year Change', 'Day\'s Range', '52 wk Range',
    'Market Cap', 'Total Assets', 'Shares Outstanding', 'ROI (TTM)',
    'Dividends (TTM)', 'Dividend Yield', 'Beta', 'Asset Class'],

    'Bonds': ['Day\'s Range', '52 wk Range', 'Price', 'Price Open', 'Price Range',
    'Coupon', 'Maturity Date', '1-Year Change'],

    'Funds': ['Rating', 'Risk Rating', '1-Year Change', 'TTM Yield', 'Turnover',
    'Total Assets', 'Market Cap', 'ROE', 'ROA', 'Expenses']
}

STATIC_OBJECTS = {
    'Commodities': {
        'object': CommodityStaticInfo, 'type': 'cmdty', 'link': TABLE_LINKS['Commodities'], 'table class': table_class,
        'before live fields': before_live_fields, 'live fields': live_fields['Commodities'], 'after live fields': after_live_fields['Commodities']},
    'Currencies': {
        'object': CurrencyStaticInfo, 'type': 'crncy', 'link': TABLE_LINKS['Currencies'], 'table class': table_class,
        'before live fields': before_live_fields, 'live fields': live_fields['Currencies'], 'after live fields': after_live_fields['Currencies']},
    'Cryptocurrencies': {
        'object': CryptocurrencyStaticInfo, 'type': 'crptcrncy', 'link': TABLE_LINKS['Cryptocurrencies'], 'table class': 'genTbl openTbl js-all-crypto-table mostActiveStockTbl crossRatesTbl allCryptoTlb wideTbl elpTbl elp15',
        'before live fields': before_live_fields, 'live fields': live_fields['Cryptocurrencies'], 'after live fields': after_live_fields['Cryptocurrencies']},
    'US Stocks': {
        'object': USStockStaticInfo, 'type': 'stck', 'link': TABLE_LINKS['US Stocks'], 'table class': table_class1,
        'before live fields': before_live_fields, 'live fields': live_fields['Stocks'], 'after live fields': after_live_fields['Stocks']},
    'Japan Stocks': {
        'object': JapanStockStaticInfo, 'type': 'stck', 'link': TABLE_LINKS['Japan Stocks'], 'table class': table_class1,
        'before live fields': before_live_fields, 'live fields': live_fields['Stocks'], 'after live fields': after_live_fields['Stocks']},
    'UK Stocks': {
        'object': UKStockStaticInfo, 'type': 'stck', 'link': TABLE_LINKS['UK Stocks'], 'table class': table_class1,
        'before live fields': before_live_fields, 'live fields': live_fields['Stocks'], 'after live fields': after_live_fields['Stocks']},
    'HK Stocks': {
        'object': HKStockStaticInfo, 'type': 'stck', 'link': TABLE_LINKS['HK Stocks'], 'table class': table_class1,
        'before live fields': before_live_fields, 'live fields': live_fields['Stocks'], 'after live fields': after_live_fields['Stocks']},
    'China Stocks': {
        'object': ChinaStockStaticInfo, 'type': 'stck', 'link': TABLE_LINKS['China Stocks'], 'table class': table_class1,
        'before live fields': before_live_fields, 'live fields': live_fields['Stocks'], 'after live fields': after_live_fields['Stocks']},
    'Canada Stocks': {
        'object': CanadaStockStaticInfo, 'type': 'stck', 'link': TABLE_LINKS['Canada Stocks'], 'table class': table_class1,
        'before live fields': before_live_fields, 'live fields': live_fields['Stocks'], 'after live fields': after_live_fields['Stocks']},
    'Germany Stocks': {
        'object': GermanyStockStaticInfo, 'type': 'stck', 'link': TABLE_LINKS['Germany Stocks'], 'table class': table_class1,
        'before live fields': before_live_fields, 'live fields': live_fields['Stocks'], 'after live fields': after_live_fields['Stocks']},
    'Australia Stocks': {
        'object': AustraliaStockStaticInfo, 'type': 'stck', 'link': TABLE_LINKS['Australia Stocks'], 'table class': table_class1,
        'before live fields': before_live_fields, 'live fields': live_fields['Stocks'], 'after live fields': after_live_fields['Stocks']},
    
    'US Indices': {
        'object': USIndexStaticInfo, 'type': 'indx', 'link': TABLE_LINKS['US Indices'], 'table class': table_class2,
        'before live fields': before_live_fields, 'live fields': live_fields['Indices'], 'after live fields': after_live_fields['Indices']},
    'Japan Indices': {
        'object': JapanIndexStaticInfo, 'type': 'indx', 'link': TABLE_LINKS['Japan Indices'], 'table class': table_class2,
        'before live fields': before_live_fields, 'live fields': live_fields['Indices'], 'after live fields': after_live_fields['Indices']},
    'UK Indices': {
        'object': UKIndexStaticInfo, 'type': 'indx', 'link': TABLE_LINKS['UK Indices'], 'table class': table_class2,
        'before live fields': before_live_fields, 'live fields': live_fields['Indices'], 'after live fields': after_live_fields['Indices']},
    'HK Indices': {
        'object': HKIndexStaticInfo, 'type': 'indx', 'link': TABLE_LINKS['HK Indices'], 'table class': table_class2,
        'before live fields': before_live_fields, 'live fields': live_fields['Indices'], 'after live fields': after_live_fields['Indices']},
    'China Indices': {
        'object': ChinaIndexStaticInfo, 'type': 'indx', 'link': TABLE_LINKS['China Indices'], 'table class': table_class2,
        'before live fields': before_live_fields, 'live fields': live_fields['Indices'], 'after live fields': after_live_fields['Indices']},
    'Canada Indices': {
        'object': CanadaIndexStaticInfo, 'type': 'indx', 'link': TABLE_LINKS['Canada Indices'], 'table class': table_class2,
        'before live fields': before_live_fields, 'live fields': live_fields['Indices'], 'after live fields': after_live_fields['Indices']},
    'Germany Indices': {
        'object': GermanyIndexStaticInfo, 'type': 'indx', 'link': TABLE_LINKS['Germany Indices'], 'table class': table_class2,
        'before live fields': before_live_fields, 'live fields': live_fields['Indices'], 'after live fields': after_live_fields['Indices']},
    'Australia Indices': {
        'object': AustraliaIndexStaticInfo, 'type': 'indx', 'link': TABLE_LINKS['Australia Indices'], 'table class': table_class2,
        'before live fields': before_live_fields, 'live fields': live_fields['Indices'], 'after live fields': after_live_fields['Indices']},
    
    'US ETFs': {
        'object': USETFStaticInfo, 'type': 'etf', 'link': TABLE_LINKS['US ETFs'], 'table class': table_class3,
        'before live fields': before_live_fields, 'live fields': live_fields['ETFs'], 'after live fields': after_live_fields['ETFs']},
    'Japan ETFs': {
        'object': JapanETFStaticInfo, 'type': 'etf', 'link': TABLE_LINKS['Japan ETFs'], 'table class': table_class3,
        'before live fields': before_live_fields, 'live fields': live_fields['ETFs'], 'after live fields': after_live_fields['ETFs']},
    'UK ETFs': {
        'object': UKETFStaticInfo, 'type': 'etf', 'link': TABLE_LINKS['UK ETFs'], 'table class': table_class3,
        'before live fields': before_live_fields, 'live fields': live_fields['ETFs'], 'after live fields': after_live_fields['ETFs']},
    'HK ETFs': {
        'object': HKETFStaticInfo, 'type': 'etf', 'link': TABLE_LINKS['HK ETFs'], 'table class': table_class3,
        'before live fields': before_live_fields, 'live fields': live_fields['ETFs'], 'after live fields': after_live_fields['ETFs']},
    'China ETFs': {
        'object': ChinaETFStaticInfo, 'type': 'etf', 'link': TABLE_LINKS['China ETFs'], 'table class': table_class3,
        'before live fields': before_live_fields, 'live fields': live_fields['ETFs'], 'after live fields': after_live_fields['ETFs']},
    'Canada ETFs': {
        'object': CanadaETFStaticInfo, 'type': 'etf', 'link': TABLE_LINKS['Canada ETFs'], 'table class': table_class3,
        'before live fields': before_live_fields, 'live fields': live_fields['ETFs'], 'after live fields': after_live_fields['ETFs']},
    'Germany ETFs': {
        'object': GermanyETFStaticInfo, 'type': 'etf', 'link': TABLE_LINKS['Germany ETFs'], 'table class': table_class3,
        'before live fields': before_live_fields, 'live fields': live_fields['ETFs'], 'after live fields': after_live_fields['ETFs']},
    'Australia ETFs': {
        'object': AustraliaETFStaticInfo, 'type': 'etf', 'link': TABLE_LINKS['Australia ETFs'], 'table class': table_class3,
        'before live fields': before_live_fields, 'live fields': live_fields['ETFs'], 'after live fields': after_live_fields['ETFs']},
    
    'US Bonds': {
        'object': USBondStaticInfo, 'type': 'bnd', 'link': TABLE_LINKS['US Bonds'], 'table class': table_class,
        'before live fields': ['Prev. Close'], 'live fields': live_fields['Bonds'], 'after live fields': after_live_fields['Bonds']},
    'Japan Bonds': {
        'object': JapanBondStaticInfo, 'type': 'bnd', 'link': TABLE_LINKS['Japan Bonds'], 'table class': table_class,
        'before live fields': ['Prev. Close'], 'live fields': live_fields['Bonds'], 'after live fields': after_live_fields['Bonds']},
    'UK Bonds': {
        'object': UKBondStaticInfo, 'type': 'bnd', 'link': TABLE_LINKS['UK Bonds'], 'table class': table_class,
        'before live fields': ['Prev. Close'], 'live fields': live_fields['Bonds'], 'after live fields': after_live_fields['Bonds']},
    'HK Bonds': {
        'object': HKBondStaticInfo, 'type': 'bnd', 'link': TABLE_LINKS['HK Bonds'], 'table class': table_class,
        'before live fields': ['Prev. Close'], 'live fields': live_fields['Bonds'], 'after live fields': after_live_fields['Bonds']},
    'China Bonds': {
        'object': ChinaBondStaticInfo, 'type': 'bnd', 'link': TABLE_LINKS['China Bonds'], 'table class': table_class,
        'before live fields': ['Prev. Close'], 'live fields': live_fields['Bonds'], 'after live fields': after_live_fields['Bonds']},
    'Canada Bonds': {
        'object': CanadaBondStaticInfo, 'type': 'bnd', 'link': TABLE_LINKS['Canada Bonds'], 'table class': table_class,
        'before live fields': ['Prev. Close'], 'live fields': live_fields['Bonds'], 'after live fields': after_live_fields['Bonds']},
    'Germany Bonds': {
        'object': GermanyBondStaticInfo, 'type': 'bnd', 'link': TABLE_LINKS['Germany Bonds'], 'table class': table_class,
        'before live fields': ['Prev. Close'], 'live fields': live_fields['Bonds'], 'after live fields': after_live_fields['Bonds']},
    'Australia Bonds': {
        'object': AustraliaBondStaticInfo, 'type': 'bnd', 'link': TABLE_LINKS['Australia Bonds'], 'table class': table_class,
        'before live fields': ['Prev. Close'], 'live fields': live_fields['Bonds'], 'after live fields': after_live_fields['Bonds']},
    
    'US Funds': {
        'object': USFundStaticInfo, 'type': 'fnd', 'link': TABLE_LINKS['US Funds'], 'table class': table_class3,
        'before live fields': ['Prev. Close'], 'live fields': live_fields['Funds'], 'after live fields': after_live_fields['Funds']},
    'Japan Funds': {
        'object': JapanFundStaticInfo, 'type': 'fnd', 'link': TABLE_LINKS['Japan Funds'], 'table class': table_class3,
        'before live fields': ['Prev. Close'], 'live fields': live_fields['Funds'], 'after live fields': after_live_fields['Funds']},
    'UK Funds': {
        'object': UKFundStaticInfo, 'type': 'fnd', 'link': TABLE_LINKS['UK Funds'], 'table class': table_class3,
        'before live fields': ['Prev. Close'], 'live fields': live_fields['Funds'], 'after live fields': after_live_fields['Funds']},
    'HK Funds': {
        'object': HKFundStaticInfo, 'type': 'fnd', 'link': TABLE_LINKS['HK Funds'], 'table class': table_class3,
        'before live fields': ['Prev. Close'], 'live fields': live_fields['Funds'], 'after live fields': after_live_fields['Funds']},
    'China Funds': {
        'object': ChinaFundStaticInfo, 'type': 'fnd', 'link': TABLE_LINKS['China Funds'], 'table class': table_class3,
        'before live fields': ['Prev. Close'], 'live fields': live_fields['Funds'], 'after live fields': after_live_fields['Funds']},
    'Canada Funds': {
        'object': CanadaFundStaticInfo, 'type': 'fnd', 'link': TABLE_LINKS['Canada Funds'], 'table class': table_class3,
        'before live fields': ['Prev. Close'], 'live fields': live_fields['Funds'], 'after live fields': after_live_fields['Funds']},
    'Germany Funds': {
        'object': GermanyFundStaticInfo, 'type': 'fnd', 'link': TABLE_LINKS['Germany Funds'], 'table class': table_class3,
        'before live fields': ['Prev. Close'], 'live fields': live_fields['Funds'], 'after live fields': after_live_fields['Funds']},
    'Australia Funds': {
        'object': AustraliaFundStaticInfo, 'type': 'fnd', 'link': TABLE_LINKS['Australia Funds'], 'table class': table_class3,
        'before live fields': ['Prev. Close'], 'live fields': live_fields['Funds'], 'after live fields': after_live_fields['Funds']},
}
