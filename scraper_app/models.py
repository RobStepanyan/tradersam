from django.db import models
import datetime

# Create your models here.
COUNTRIES = (
    ('G', 'Global'), ('US', 'United States'), ('UK', 'United Kingdom'),
    ('JP', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'),
    ('GE', 'Germany'), ('AU', 'Australia')
)


CURRENCIES = (
    ('USD', 'US Dollar'), ('JPY', 'Japanese Yen'), ('GBP', 'Pound Sterling'), ('HKD', 'Hong Kong Dollar'),
    ('CNY', 'Chinese Yuan'), ('CAD', 'Canadian Dollar'), ('EUR', 'Euro'), ('AUD', 'Australian Dollar')
)

MARKETS_US = (
    ('NYSE', 'New York Stock Exchange (NYSE)'), ('NASDAQ', 'NASDAQ Stock Market'), ('OTC Markets', 'Over-The-Counter Markets (OTC)'),
    ('AMEX', 'American Stock Exchange (AMEX)'), ('BSE', 'Boston Stock Exchange (BSE)'), ('CBOE', 'Chicago Board Options Exchange (CBOE)'),
    ('CBOT', 'Chicago Board of Trade (CBOT)'), ('CME', 'Chicago Mercantile Exchange (CME)'), ('CHX', 'Chicago Stock Exchange (CHX)'),
    ('ISE', 'International Securities Exchange i.nameSE)'), ('MS4X', 'Miami Stock Exchange (MS4X)'), ('NSX', 'National Stock Exchange (NSX)'),
    ('PHLX', 'Philadelphia Stock Exchange (PHLX)'), ('NYSE Arca', 'NYSE Arca')
)

MARKETS_JP = (
    ('Tokyo', 'Tokyo Stock Exchange (TYO)'), ('Osaka', 'Osaka Securities Exchange'), ('Nagoya', 'Nagoya Stock Exchange (NSE)'),
    ('Fukuoka', 'Fukuoka Stock Exchange (FSE)'), ('Sapporo', 'Sapporo Securities Exchange'), ('JASDAQ', 'JASDAQ Securities Exchange')
)

MARKETS_UK = (
    ('London', 'London Stock Exchange'),
)

MARKETS_HK = (
    ('HKG', 'The Stock Exchange of Hong Kong Limited'),
)

MARKETS_CH = (
    ('Shanghai', 'Shanghai Stock Exchange'), ('Shenzhen', 'Shenzhen Stock Exchange')
)

MARKETS_CA = (
    ('NEO', 'Aequitas Neo Exchange (NEO)'), ('Toronto', 'Toronto Stock Exchange (TSX)'),
    ('CSE', 'Canadian Securities Exchange (CSE)'), ('NASDAQ', 'NASDAQ Canada'),
    ('TSXV', 'TSX Venture Exchange (TSXV)')
)

MARKETS_GE = (
    ('Frankfurt', 'Frankfurt Stock Exchange (XFRA)'), ('Berlin', 'Berlin Stock Exchange (XBER)'),
    ('Xetra', 'Xetra Stock Exchange (XETR)'), ('Munich', 'Munich Stock Exchange (XMUN)'),
    ('Stuttgart', 'Stuttgart Stock Exchange (XSTU)'), ('Dusseldorf', 'Dusseldorf Stock Exchange(XDUS)'),
    ('Hamburg', 'Hamburg Stock Exchange(XHAM)'), ('Hannover', 'Hannover Stock Exchange (XHAN)')
)

MARKETS_AU = (
    ('ASX', 'Australian Securities Exchange'),
)

TYPES = (
    ('cmdty', 'Commodity'), ('crncy', 'Currency'), ('crptcrncy', 'Cryptocurrency'),
    ('stck', 'Stock'), ('indx', 'Index'), ('etf', 'ETF'), ('bnd', 'Bond'), ('fnd', 'Fund')
)
TYPES_PLURAL = (
    ('cmdty', 'Commodities'), ('crncy', 'Currencies'), ('crptcrncy', 'Cryptocurrencies'),
    ('stck', 'Stocks'), ('indx', 'Indices'), ('etf', 'ETFs'), ('bnd', 'Bonds'), ('fnd', 'Funds')
)
Types = [i for j in TYPES for i in j]
Types_plural = [i for j in TYPES_PLURAL for i in j]
Countries = [i for j in COUNTRIES for i in j]

class CommodityStaticInfo(models.Model):
    fields_to_scrape = (
        'Contract Size', 'Tick Size', 'Tick Value', 'Base Symbol', 'Point Value')
    
    Type = models.CharField(choices=TYPES, max_length=9, default='cmdty')
    short_name = models.CharField(max_length=16)
    @property
    def long_name(self):
        return self.short_name + ' Futures Contract'
    country = models.CharField(choices=COUNTRIES, max_length=2)
    base_symbol = models.CharField(max_length=7)
    contract_size = models.CharField(max_length=30)
    settlement_type = models.CharField(default='Physical', max_length=30)
    tick_size = models.CharField(max_length=30)
    tick_value = models.CharField(max_length=30)
    point_value = models.CharField(max_length=20)
    unit = models.CharField(max_length=15, null=True)
    link = models.URLField()

    def __str__(self):
        return f'({self.country})' + ' ' + self.long_name + ' (' + self.base_symbol + ')'

    class Meta:
        verbose_name = "(Static Info) Commodities'"
        verbose_name_plural = "(Static Info) Commodities'"


class CurrencyStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='crncy')
    short_name = models.CharField(max_length=10)
    long_name = models.CharField(max_length=50)
    country = models.CharField(choices=COUNTRIES, default='G', max_length=2)
    link = models.URLField()

    def __str__(self):
        return self.short_name + ' - ' + self.long_name

    class Meta:
        verbose_name = "(Static Info) Currencies'"
        verbose_name_plural = "(Static Info) Currencies'"

class CryptocurrencyStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='crptcrncy')
    short_name = models.CharField(max_length=10)
    long_name = models.CharField(max_length=50)
    country = models.CharField(choices=COUNTRIES, default='G', max_length=2)
    link = models.URLField(null=True)

    def __str__(self):
        return f'{self.long_name} ({self.short_name})'

    class Meta:
        verbose_name = "(Static Info) Cryptocurrencies"
        verbose_name_plural = "(Static Info) Cryptocurrencies"

class USStockStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='stck')
    short_name = models.CharField(max_length=12)
    long_name = models.CharField(max_length=60)
    country = models.CharField(choices=COUNTRIES, default='US', max_length=2)
    market = models.CharField(choices=MARKETS_US, max_length=11)
    isin = models.CharField(max_length=12)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='USD', max_length=3)

    def __str__(self):
        return self.long_name + f' - ({self.short_name})'

    class Meta:
        verbose_name = "(Static Info) United States Stocks"
        verbose_name_plural = "(Static Info) United States Stocks"

class JapanStockStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='stck')
    short_name = models.CharField(max_length=12)
    long_name = models.CharField(max_length=60)
    country = models.CharField(choices=COUNTRIES, default='JP', max_length=2)
    market = models.CharField(choices=MARKETS_JP, max_length=7)
    isin = models.CharField(max_length=12)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='JPY', max_length=3)

    def __str__(self):
        return self.long_name + f' - ({self.short_name})'

    class Meta:
        verbose_name = "(Static Info) Japan Stocks"
        verbose_name_plural = "(Static Info) Japan Stocks"

class UKStockStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='stck')
    short_name = models.CharField(max_length=12)
    long_name = models.CharField(max_length=60)
    country = models.CharField(choices=COUNTRIES, default='UK', max_length=2)
    market = models.CharField(choices=MARKETS_UK, default='London', max_length=20)
    isin = models.CharField(max_length=12)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='GBP', max_length=3)

    def __str__(self):
        return self.long_name + f' - ({self.short_name})'

    class Meta:
        verbose_name = "(Static Info) United Kingdom Stocks"
        verbose_name_plural = "(Static Info) United Kingdom Stocks"

class HKStockStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='stck')
    short_name = models.CharField(max_length=4)
    long_name = models.CharField(max_length=75)
    country = models.CharField(choices=COUNTRIES, default='HK', max_length=2)
    market = models.CharField(choices=MARKETS_HK, default='HKG', max_length=3)
    isin = models.CharField(max_length=12)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='HKD', max_length=3)

    def __str__(self):
        return self.long_name + f' - ({self.short_name})'

    class Meta:
        verbose_name = "(Static Info) Hong Kong Stocks"
        verbose_name_plural = "(Static Info) Hong Kong Stocks"

class ChinaStockStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='stck')
    short_name = models.CharField(max_length=6)
    long_name = models.CharField(max_length=75)
    country = models.CharField(choices=COUNTRIES, default='CH', max_length=2)
    market = models.CharField(choices=MARKETS_CH, max_length=20)
    isin = models.CharField(max_length=12)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='CNY', max_length=3)

    def __str__(self):
        return self.long_name + f' - ({self.short_name})'

    class Meta:
        verbose_name = "(Static Info) China Stocks"
        verbose_name_plural = "(Static Info) China Stocks"

class CanadaStockStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='stck')
    short_name = models.CharField(max_length=6)
    long_name = models.CharField(max_length=51)
    country = models.CharField(choices=COUNTRIES, default='CA', max_length=2)
    market = models.CharField(choices=MARKETS_CA, max_length=7)
    isin = models.CharField(max_length=12)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='CAD', max_length=3)

    def __str__(self):
        return self.long_name + f' - ({self.short_name})'

    class Meta:
        verbose_name = "(Static Info) Canada Stocks"
        verbose_name_plural = "(Static Info) Canada Stocks"

class GermanyStockStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='stck')
    short_name = models.CharField(max_length=8)
    long_name = models.CharField(max_length=45)
    country = models.CharField(choices=COUNTRIES, default='GE', max_length=2)
    market = models.CharField(choices=MARKETS_GE, max_length=20)
    isin = models.CharField(max_length=12)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='EUR', max_length=3)

    def __str__(self):
        return self.long_name + f' - ({self.short_name})'

    class Meta:
        verbose_name = "(Static Info) Germany Stocks"
        verbose_name_plural = "(Static Info) Germany Stocks"

class AustraliaStockStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='stck')
    short_name = models.CharField(max_length=8)
    long_name = models.CharField(max_length=49)
    country = models.CharField(choices=COUNTRIES, default='AU', max_length=2)
    market = models.CharField(choices=MARKETS_AU, max_length=3, default='ASX')
    isin = models.CharField(max_length=12)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='AUD', max_length=3)

    def __str__(self):
        return self.long_name + f' - ({self.short_name})'

    class Meta:
        verbose_name = "(Static Info) Australia Stocks"
        verbose_name_plural = "(Static Info) Australia Stocks"

class USIndexStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='indx')
    short_name = models.CharField(max_length=12)
    long_name = models.CharField(max_length=63)
    country = models.CharField(choices=COUNTRIES, default='US', max_length=2)
    market = models.CharField(choices=MARKETS_US, max_length=11)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='USD', max_length=3)

    def __str__(self):
        return self.long_name + f' - ({self.short_name})'

    class Meta:
        verbose_name = "(Static Info) United States Indices"
        verbose_name_plural = "(Static Info) United States Indices"

class JapanIndexStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='indx')
    short_name = models.CharField(max_length=12)
    long_name = models.CharField(max_length=49)
    country = models.CharField(choices=COUNTRIES, default='JP', max_length=2)
    market = models.CharField(choices=MARKETS_JP, max_length=7)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='JPY', max_length=3)

    def __str__(self):
        return self.long_name + f' - ({self.short_name})'

    class Meta:
        verbose_name = "(Static Info) Japan Indices"
        verbose_name_plural = "(Static Info) Japan Indices"

class UKIndexStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='indx')
    short_name = models.CharField(max_length=12)
    long_name = models.CharField(max_length=49)
    country = models.CharField(choices=COUNTRIES, default='UK', max_length=2)
    market = models.CharField(choices=MARKETS_UK, default='London', max_length=20)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='GBP', max_length=3)

    def __str__(self):
        return self.long_name + f' - ({self.short_name})'

    class Meta:
        verbose_name = "(Static Info) United Kingdom Indices"
        verbose_name_plural = "(Static Info) United Kingdom Indices"

class HKIndexStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='indx')
    short_name = models.CharField(max_length=12)
    long_name = models.CharField(max_length=56)
    country = models.CharField(choices=COUNTRIES, default='HK', max_length=2)
    market = models.CharField(choices=MARKETS_HK, default='HKG', max_length=3)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='HKD', max_length=3)

    def __str__(self):
        return self.long_name + f' - ({self.short_name})'

    class Meta:
        verbose_name = "(Static Info) Hong Kong Indices"
        verbose_name_plural = "(Static Info) Hong Kong Indices"

class ChinaIndexStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='indx')
    short_name = models.CharField(max_length=12)
    long_name = models.CharField(max_length=56)
    country = models.CharField(choices=COUNTRIES, default='CH', max_length=2)
    market = models.CharField(choices=MARKETS_CH, max_length=8)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='CNY', max_length=3)

    def __str__(self):
        return self.long_name + f' - ({self.short_name})'

    class Meta:
        verbose_name = "(Static Info) China Indices"
        verbose_name_plural = "(Static Info) China Indices"

class CanadaIndexStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='indx')
    short_name = models.CharField(max_length=12)
    long_name = models.CharField(max_length=44)
    country = models.CharField(choices=COUNTRIES, default='CA', max_length=2)
    market = models.CharField(choices=MARKETS_CA, max_length=7)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='CAD', max_length=3)

    def __str__(self):
        return self.long_name + f' - ({self.short_name})'

    class Meta:
        verbose_name = "(Static Info) Canada Indices"
        verbose_name_plural = "(Static Info) Canada Indices"

class GermanyIndexStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='indx')
    short_name = models.CharField(max_length=12)
    long_name = models.CharField(max_length=46)
    country = models.CharField(choices=COUNTRIES, default='GE', max_length=2)
    market = models.CharField(choices=MARKETS_GE, max_length=10)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='EUR', max_length=3)

    def __str__(self):
        return self.long_name + f' - ({self.short_name})'

    class Meta:
        verbose_name = "(Static Info) Germany Indices"
        verbose_name_plural = "(Static Info) Germany Indices"

class AustraliaIndexStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='indx')
    short_name = models.CharField(max_length=12)
    long_name = models.CharField(max_length=47)
    country = models.CharField(choices=COUNTRIES, default='AU', max_length=2)
    market = models.CharField(choices=MARKETS_AU, max_length=3, default='ASX')
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='AUD', max_length=3)

    def __str__(self):
        return self.long_name + f' - ({self.short_name})'

    class Meta:
        verbose_name = "(Static Info) Australia Indices"
        verbose_name_plural = "(Static Info) Australia Indices"

class ETFIssuers(models.Model):
    name = models.CharField(max_length=45)
    country = models.CharField(choices=COUNTRIES, max_length=2)

    def __str__(self):
        return f'{self.country}' + self.name

    class Meta:
        verbose_name = '(Other) ETF Issuers'
        verbose_name_plural = '(Other) ETF Issuers'

ETF_ISSUERS_US = tuple([(i.name, i.name) for i in list(ETFIssuers.objects.filter(country='US'))])
ETF_ISSUERS_JP = tuple([(i.name, i.name) for i in list(ETFIssuers.objects.filter(country='JP'))])
ETF_ISSUERS_UK = tuple([(i.name, i.name) for i in list(ETFIssuers.objects.filter(country='UK'))])
ETF_ISSUERS_HK = tuple([(i.name, i.name) for i in list(ETFIssuers.objects.filter(country='HK'))])
ETF_ISSUERS_CH = tuple([(i.name, i.name) for i in list(ETFIssuers.objects.filter(country='CH'))])
ETF_ISSUERS_CA = tuple([(i.name, i.name) for i in list(ETFIssuers.objects.filter(country='CA'))])
ETF_ISSUERS_GE = tuple([(i.name, i.name) for i in list(ETFIssuers.objects.filter(country='GE'))])
ETF_ISSUERS_AU = tuple([(i.name, i.name) for i in list(ETFIssuers.objects.filter(country='AU'))])

class USETFStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='etf')
    short_name = models.CharField(max_length=12)
    long_name = models.CharField(max_length=120)
    country = models.CharField(choices=COUNTRIES, default='US', max_length=2)
    issuer = models.CharField(choices=ETF_ISSUERS_US, max_length=100)
    market = models.CharField(choices=MARKETS_US, max_length=11)
    currency = models.CharField(choices=CURRENCIES, default='USD', max_length=3)
    isin = models.CharField(max_length=12)
    link = models.URLField()

    def __str__(self):
        return f'{self.country}' + self.long_name

    class Meta:
        verbose_name = '(Static Info) United States ETFs\''
        verbose_name_plural = '(Static Info) United States ETFs\''

class JapanETFStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='etf')
    short_name = models.CharField(max_length=12)
    long_name = models.CharField(max_length=121)
    country = models.CharField(choices=COUNTRIES, default='JP', max_length=2)
    issuer = models.CharField(choices=ETF_ISSUERS_JP, max_length=100)
    market = models.CharField(choices=MARKETS_JP, max_length=7)
    isin = models.CharField(max_length=12)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='JPY', max_length=3)

    def __str__(self):
        return f'{self.country}' + self.long_name

    class Meta:
        verbose_name = '(Static Info) Japan ETFs\''
        verbose_name_plural = '(Static Info) Japan ETFs\''

class UKETFStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='etf')
    short_name = models.CharField(max_length=12)
    long_name = models.CharField(max_length=120)
    country = models.CharField(choices=COUNTRIES, default='UK', max_length=2)
    issuer = models.CharField(choices=ETF_ISSUERS_UK, max_length=100)
    market = models.CharField(choices=MARKETS_UK, default='London', max_length=20)
    isin = models.CharField(max_length=12)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='GBP', max_length=3)

    def __str__(self):
        return f'{self.country}' + self.long_name

    class Meta:
        verbose_name = '(Static Info) United Kingdom ETFs\''
        verbose_name_plural = '(Static Info) United Kingdom ETFs\''

class HKETFStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='etf')
    short_name = models.CharField(max_length=12)
    long_name = models.CharField(max_length=100)
    country = models.CharField(choices=COUNTRIES, default='HK', max_length=2)
    issuer = models.CharField(choices=ETF_ISSUERS_HK, max_length=100)
    market = models.CharField(choices=MARKETS_HK, default='HKG', max_length=3)
    isin = models.CharField(max_length=12)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='HKD', max_length=3)

    def __str__(self):
        return f'{self.country}' + self.long_name

    class Meta:
        verbose_name = '(Static Info) Hong Kong ETFs\''
        verbose_name_plural = '(Static Info) Hong Kong ETFs\''

class ChinaETFStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='etf')
    short_name = models.CharField(max_length=12)
    long_name = models.CharField(max_length=120)
    country = models.CharField(choices=COUNTRIES, default='CH', max_length=2)
    issuer = models.CharField(choices=ETF_ISSUERS_CH, max_length=100)
    market = models.CharField(choices=MARKETS_CH, max_length=20)
    isin = models.CharField(max_length=12)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='CNY', max_length=3)

    def __str__(self):
        return f'{self.country}' + self.long_name

    class Meta:
        verbose_name = '(Static Info) China ETFs\''
        verbose_name_plural = '(Static Info) China ETFs\''

class CanadaETFStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='etf')
    short_name = models.CharField(max_length=12)
    long_name = models.CharField(max_length=120)
    country = models.CharField(choices=COUNTRIES, default='CA', max_length=2)
    issuer = models.CharField(choices=ETF_ISSUERS_CA, max_length=100)
    market = models.CharField(choices=MARKETS_CA, max_length=7)
    isin = models.CharField(max_length=12)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='CAD', max_length=3)

    def __str__(self):
        return f'{self.country}' + self.long_name

    class Meta:
        verbose_name = '(Static Info) Canada ETFs\''
        verbose_name_plural = '(Static Info) Canada ETFs\''

class GermanyETFStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='etf')
    short_name = models.CharField(max_length=12)
    long_name = models.CharField(max_length=120)
    country = models.CharField(choices=COUNTRIES, default='GE', max_length=2)
    issuer = models.CharField(choices=ETF_ISSUERS_GE, max_length=100)
    market = models.CharField(choices=MARKETS_GE, max_length=20)
    isin = models.CharField(max_length=12)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='EUR', max_length=3)

    def __str__(self):
        return f'{self.country}' + self.long_name

    class Meta:
        verbose_name = '(Static Info) Germany ETFs\''
        verbose_name_plural = '(Static Info) Germany ETFs\''

class AustraliaETFStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='etf')
    short_name = models.CharField(max_length=12)
    long_name = models.CharField(max_length=120)
    country = models.CharField(choices=COUNTRIES, default='AU', max_length=2)
    issuer = models.CharField(choices=ETF_ISSUERS_AU, max_length=100)
    market = models.CharField(choices=MARKETS_AU, max_length=3, default='ASX')
    isin = models.CharField(max_length=12)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='AUD', max_length=3)

    def __str__(self):
        return f'{self.country}' + self.long_name

    class Meta:
        verbose_name = '(Static Info) Australia ETFs\''
        verbose_name_plural = '(Static Info) Australia ETFs\''
# *********************** Bonds
class USBondStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='bnd')
    short_name = models.CharField(max_length=18)
    long_name = models.CharField(max_length=32)
    country = models.CharField(choices=COUNTRIES, default='US', max_length=2)
    market = models.CharField(choices=MARKETS_US, max_length=11)
    currency = models.CharField(choices=CURRENCIES, default='USD', max_length=3)
    link = models.URLField()

    def __str__(self):
        return self.long_name

    class Meta:
        verbose_name = '(Static Info) United States Bonds\''
        verbose_name_plural = '(Static Info) United States Bonds\''

class JapanBondStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='bnd')
    short_name = models.CharField(max_length=10)
    long_name = models.CharField(max_length=24)
    country = models.CharField(choices=COUNTRIES, default='JP', max_length=2)
    market = models.CharField(choices=MARKETS_JP, max_length=7)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='JPY', max_length=3)

    def __str__(self):
        return self.long_name

    class Meta:
        verbose_name = '(Static Info) Japan Bonds\''
        verbose_name_plural = '(Static Info) Japan Bonds\''

class UKBondStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='bnd')
    short_name = models.CharField(max_length=8)
    long_name = models.CharField(max_length=33)
    country = models.CharField(choices=COUNTRIES, default='UK', max_length=2)
    market = models.CharField(choices=MARKETS_UK, default='London', max_length=20)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='GBP', max_length=3)

    def __str__(self):
        return self.long_name

    class Meta:
        verbose_name = '(Static Info) United Kingdom Bonds\''
        verbose_name_plural = '(Static Info) United Kingdom Bonds\''

class HKBondStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='bnd')
    short_name = models.CharField(max_length=13)
    long_name = models.CharField(max_length=28)
    country = models.CharField(choices=COUNTRIES, default='HK', max_length=2)
    market = models.CharField(choices=MARKETS_HK, default='HKG', max_length=3)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='HKD', max_length=3)

    def __str__(self):
        return self.long_name

    class Meta:
        verbose_name = '(Static Info) Hong Kong Bonds\''
        verbose_name_plural = '(Static Info) Hong Kong Bonds\''

class ChinaBondStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='bnd')
    short_name = models.CharField(max_length=9)
    long_name = models.CharField(max_length=24)
    country = models.CharField(choices=COUNTRIES, default='CH', max_length=2)
    market = models.CharField(choices=MARKETS_CH, max_length=20)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='CNY', max_length=3)

    def __str__(self):
        return self.long_name

    class Meta:
        verbose_name = '(Static Info) China Bonds\''
        verbose_name_plural = '(Static Info) China Bonds\''

class CanadaBondStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='bnd')
    short_name = models.CharField(max_length=10)
    long_name = models.CharField(max_length=25)
    country = models.CharField(choices=COUNTRIES, default='CA', max_length=2)
    market = models.CharField(choices=MARKETS_CA, max_length=7)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='CAD', max_length=3)

    def __str__(self):
        return self.long_name

    class Meta:
        verbose_name = '(Static Info) Canada Bonds\''
        verbose_name_plural = '(Static Info) Canada Bonds\''

class GermanyBondStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='bnd')
    short_name = models.CharField(max_length=11)
    long_name = models.CharField(max_length=26)
    country = models.CharField(choices=COUNTRIES, default='GE', max_length=2)
    market = models.CharField(choices=MARKETS_GE, max_length=20)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='EUR', max_length=3)

    def __str__(self):
        return self.long_name

    class Meta:
        verbose_name = '(Static Info) Germany Bonds\''
        verbose_name_plural = '(Static Info) Germany Bonds\''

class AustraliaBondStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='bnd')
    short_name = models.CharField(max_length=13)
    long_name = models.CharField(max_length=28)
    country = models.CharField(choices=COUNTRIES, default='AU', max_length=2)
    market = models.CharField(choices=MARKETS_AU, max_length=3, default='ASX')
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='AUD', max_length=3)

    def __str__(self):
        return self.long_name

    class Meta:
        verbose_name = '(Static Info) Australia Bonds\''
        verbose_name_plural = '(Static Info) Australia Bonds\''

class FundIssuers(models.Model):
    name = models.CharField(max_length=55)
    country = models.CharField(choices=COUNTRIES, max_length=2)

    def __str__(self):
        return f'{self.country}' + self.name

    class Meta:
        verbose_name = '(Other) Fund Issuers'
        verbose_name_plural = '(Other) Fund Issuers'

FUND_ISSUERS_US = tuple([(i.name, i.name) for i in list(FundIssuers.objects.filter(country='US'))])
FUND_ISSUERS_JP = tuple([(i.name, i.name) for i in list(FundIssuers.objects.filter(country='JP'))])
FUND_ISSUERS_UK = tuple([(i.name, i.name) for i in list(FundIssuers.objects.filter(country='UK'))])
FUND_ISSUERS_HK = tuple([(i.name, i.name) for i in list(FundIssuers.objects.filter(country='HK'))])
FUND_ISSUERS_CH = tuple([(i.name, i.name) for i in list(FundIssuers.objects.filter(country='CH'))])
FUND_ISSUERS_CA = tuple([(i.name, i.name) for i in list(FundIssuers.objects.filter(country='CA'))])
FUND_ISSUERS_GE = tuple([(i.name, i.name) for i in list(FundIssuers.objects.filter(country='GE'))])
FUND_ISSUERS_AU = tuple([(i.name, i.name) for i in list(FundIssuers.objects.filter(country='AU'))])

# *********************** Funds
class USFundStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='fnd')
    short_name = models.CharField(max_length=10)
    long_name = models.CharField(max_length=78)
    country = models.CharField(choices=COUNTRIES, default='US', max_length=2)
    market = models.CharField(choices=MARKETS_US, max_length=11)
    currency = models.CharField(choices=CURRENCIES, default='USD', max_length=3)
    link = models.URLField()
    issuer = models.CharField(choices=FUND_ISSUERS_US, max_length=100)
    isin = models.CharField(max_length=12)
    min_investment = models.CharField(null=True, max_length=12)
    category = models.CharField(max_length=40)
    category_descrptn = models.TextField(null=True)
    inception_date = models.DateField(default=None, null=True)

    def __str__(self):
        return self.long_name

    class Meta:
        verbose_name = '(Static Info) United States Funds\''
        verbose_name_plural = '(Static Info) United States Funds\''

class JapanFundStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='fnd')
    short_name = models.CharField(max_length=10)
    long_name = models.CharField(max_length=70)
    country = models.CharField(choices=COUNTRIES, default='JP', max_length=2)
    market = models.CharField(choices=MARKETS_JP, max_length=7)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='JPY', max_length=3)
    issuer = models.CharField(choices=FUND_ISSUERS_JP, max_length=100)
    isin = models.CharField(max_length=12)
    min_investment = models.CharField(null=True, max_length=12)
    category = models.CharField(max_length=40)
    category_descrptn = models.TextField(null=True)
    inception_date = models.DateField(default=None, null=True)

    def __str__(self):
        return self.long_name

    class Meta:
        verbose_name = '(Static Info) Japan Funds\''
        verbose_name_plural = '(Static Info) Japan Funds\''

class UKFundStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='fnd')
    short_name = models.CharField(max_length=10)
    long_name = models.CharField(max_length=91)
    country = models.CharField(choices=COUNTRIES, default='UK', max_length=2)
    market = models.CharField(choices=MARKETS_UK, default='London', max_length=20)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='GBP', max_length=3)
    issuer = models.CharField(choices=FUND_ISSUERS_UK, max_length=100)
    isin = models.CharField(max_length=12)
    min_investment = models.CharField(null=True, max_length=12)
    category = models.CharField(max_length=40)
    category_descrptn = models.TextField(null=True)
    inception_date = models.DateField(default=None, null=True)

    def __str__(self): 
        return self.long_name

    class Meta:
        verbose_name = '(Static Info) United Kingdom Funds\''
        verbose_name_plural = '(Static Info) United Kingdom Funds\''

class HKFundStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='fnd')
    short_name = models.CharField(max_length=10)
    long_name = models.CharField(max_length=93)
    country = models.CharField(choices=COUNTRIES, default='HK', max_length=2)
    market = models.CharField(choices=MARKETS_HK, default='HKG', max_length=3)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='HKD', max_length=3)
    issuer = models.CharField(choices=FUND_ISSUERS_HK, max_length=100)
    isin = models.CharField(max_length=12, null=True)
    min_investment = models.CharField(null=True, max_length=12)
    category = models.CharField(max_length=45)
    category_descrptn = models.TextField(null=True)
    inception_date = models.DateField(default=None, null=True)

    def __str__(self):
        return self.long_name

    class Meta:
        verbose_name = '(Static Info) Hong Kong Funds\''
        verbose_name_plural = '(Static Info) Hong Kong Funds\''

class ChinaFundStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='fnd')
    short_name = models.CharField(max_length=10)
    long_name = models.CharField(max_length=47)
    country = models.CharField(choices=COUNTRIES, default='CH', max_length=2)
    market = models.CharField(choices=MARKETS_CH, max_length=20)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='CNY', max_length=3)
    issuer = models.CharField(choices=FUND_ISSUERS_CH, max_length=100)
    min_investment = models.CharField(null=True, max_length=12)
    category = models.CharField(max_length=40)
    category_descrptn = models.TextField(null=True)
    inception_date = models.DateField(default=None, null=True)

    def __str__(self):
        return self.long_name

    class Meta:
        verbose_name = '(Static Info) China Funds\''
        verbose_name_plural = '(Static Info) China Funds\''

class CanadaFundStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='fnd')
    short_name = models.CharField(max_length=10)
    long_name = models.CharField(max_length=57)
    country = models.CharField(choices=COUNTRIES, default='CA', max_length=2)
    market = models.CharField(choices=MARKETS_CA, max_length=7)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='CAD', max_length=3)
    issuer = models.CharField(choices=FUND_ISSUERS_CA, max_length=100)
    min_investment = models.CharField(null=True, max_length=12)
    category = models.CharField(max_length=40)
    category_descrptn = models.TextField(null=True)
    inception_date = models.DateField(default=None, null=True)

    def __str__(self):
        return self.long_name

    class Meta:
        verbose_name = '(Static Info) Canada Funds\''
        verbose_name_plural = '(Static Info) Canada Funds\''

class GermanyFundStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='fnd')
    short_name = models.CharField(max_length=10)
    long_name = models.CharField(max_length=63)
    country = models.CharField(choices=COUNTRIES, default='GE', max_length=2)
    market = models.CharField(choices=MARKETS_GE, max_length=20)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='EUR', max_length=3)
    issuer = models.CharField(choices=FUND_ISSUERS_GE, max_length=100)
    isin = models.CharField(max_length=12)
    min_investment = models.CharField(null=True, max_length=12)
    category = models.CharField(max_length=70)
    category_descrptn = models.TextField(null=True)
    inception_date = models.DateField(default=None, null=True)

    def __str__(self):
        return self.long_name

    class Meta:
        verbose_name = '(Static Info) Germany Funds\''
        verbose_name_plural = '(Static Info) Germany Funds\''

class AustraliaFundStaticInfo(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9, default='fnd')
    short_name = models.CharField(max_length=10)
    long_name = models.CharField(max_length=62)
    country = models.CharField(choices=COUNTRIES, default='AU', max_length=2)
    market = models.CharField(choices=MARKETS_AU, max_length=3, default='ASX')
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='AUD', max_length=3)
    issuer = models.CharField(choices=FUND_ISSUERS_AU, max_length=100)
    min_investment = models.CharField(null=True, max_length=12)
    category = models.CharField(max_length=40)
    category_descrptn = models.TextField(null=True)
    inception_date = models.DateField(default=None, null=True)

    def __str__(self):
        return self.long_name

    class Meta:
        verbose_name = '(Static Info) Australia Funds\''
        verbose_name_plural = '(Static Info) Australia Funds\''


# Historical Data
class AllAssetsHistoricalMax(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9)
    short_name = models.CharField(max_length=18)
    link = models.URLField(null=True)

    date = models.DateField(default=None, null=True)
    price = models.CharField(max_length=12, default=None, null=True)
    Open = models.CharField(max_length=12, default=None, null=True)
    high = models.CharField(max_length=12, default=None, null=True)
    low = models.CharField(max_length=12, default=None, null=True)
    volume = models.CharField(max_length=12, default=None, null=True)

    def __str__(self):
        return f'({Types[Types.index(self.Type)+1]}) {self.short_name} in {self.date.year} {self.date.strftime("%B")}'

    class Meta:
        ordering = ['date',]
        verbose_name = '(Historical Max Years) All Assets'
        verbose_name_plural = '(Historical Max Years) All Assets'

class AllAssetsHistorical5Y(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9)
    short_name = models.CharField(max_length=18)
    link = models.URLField(null=True)
    
    date = models.DateField(default=None, null=True)
    price = models.CharField(max_length=12, default=None, null=True)
    Open = models.CharField(max_length=12, default=None, null=True)
    high = models.CharField(max_length=12, default=None, null=True)
    low = models.CharField(max_length=12, default=None, null=True)
    volume = models.CharField(max_length=12, default=None, null=True)
    
    def __str__(self):
        return f'({Types[Types.index(self.Type)+1]}) {self.short_name} in {self.date.year} {self.date.strftime("%B")}'

    class Meta:
        ordering = ['date',]
        verbose_name = '(Historical 5 Years) All Assets'
        verbose_name_plural = '(Historical 5 Years) All Assets'

class AllAssetsHistorical1Y(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9)
    short_name = models.CharField(max_length=18)
    link = models.URLField(null=True)
    
    date = models.DateField(default=None, null=True)
    price = models.CharField(max_length=12, default=None, null=True)
    Open = models.CharField(max_length=12, default=None, null=True)
    high = models.CharField(max_length=12, default=None, null=True)
    low = models.CharField(max_length=12, default=None, null=True)
    volume = models.CharField(max_length=12, default=None, null=True)
    
    def __str__(self):
        return f'({Types[Types.index(self.Type)+1]}) {self.short_name} in {self.date.year} {self.date.strftime("%B")}'

    class Meta:
        ordering = ['date',]
        verbose_name = '(Historical 1 Year) All Assets'
        verbose_name_plural = '(Historical 1 Year) All Assets'

class AllAssetsHistorical6M1M(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9)
    short_name = models.CharField(max_length=18)
    link = models.URLField(null=True)
    
    date = models.DateField(default=None, null=True)
    price = models.CharField(max_length=12, default=None, null=True)
    Open = models.CharField(max_length=12, default=None, null=True)
    high = models.CharField(max_length=12, default=None, null=True)
    low = models.CharField(max_length=12, default=None, null=True)
    volume = models.CharField(max_length=12, default=None, null=True)
    
    def __str__(self):
        return f'({Types[Types.index(self.Type)+1]}) {self.short_name} in {self.date.year} {self.date.strftime("%B")}'

    class Meta:
        ordering = ['date',]
        verbose_name = '(Historical 6M-1M) All Assets'
        verbose_name_plural = '(Historical 6M-1M) All Assets'

class AllAssetsHistorical5D(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9)
    link = models.URLField(null=True)

    date = models.DateTimeField(default=None, null=True)
    price = models.CharField(max_length=12, default=None, null=True)
    Open = models.CharField(max_length=12, default=None, null=True)
    high = models.CharField(max_length=12, default=None, null=True)
    low = models.CharField(max_length=12, default=None, null=True)
    volume = models.CharField(max_length=12, default=None, null=True)

    def __str__(self):
        return f'({Types[Types.index(self.Type)+1]}) in {self.date.year} {self.date.strftime("%B")}'

    class Meta:
        ordering = ['date',]
        verbose_name = '(Historical 5 Days) All Assets'
        verbose_name_plural = '(Historical 5 Days) All Assets'

class AllAssetsHistorical1D(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9)
    link = models.URLField(null=True)

    date = models.DateTimeField(default=None, null=True)
    price = models.CharField(max_length=12, default=None, null=True)
    Open = models.CharField(max_length=12, default=None, null=True)
    high = models.CharField(max_length=12, default=None, null=True)
    low = models.CharField(max_length=12, default=None, null=True)
    volume = models.CharField(max_length=12, default=None, null=True)

    def __str__(self):
        return f'({Types[Types.index(self.Type)+1]}) in {self.date.year} {self.date.strftime("%B")}'

    class Meta:
        ordering = ['date',]
        verbose_name = '(Historical 1 Day) All Assets'
        verbose_name_plural = '(Historical 1 Day) All Assets'

class AllAssetsLive(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9)
    link = models.URLField(null=True)
    
    prev_close = models.CharField(max_length=15, null=True)

    last_price = models.CharField(max_length=15, null=True)
    month = models.DateField(default=None, null=True)
    Open = models.CharField(default=None, null=True, max_length=15)
    high = models.CharField(max_length=15, null=True)
    low = models.CharField(max_length=15, null=True)
    change = models.CharField(max_length=15, null=True)
    change_7d = models.CharField(default=None, null=True, max_length=15)
    change_perc = models.CharField(max_length=12, null=True)
    volume = models.CharField(max_length=12, default=None, null=True)
    market_cap = models.CharField(default=None, null=True, max_length=15) # for crypto
    Yield = models.CharField(default=None, null=True, max_length=15)
    total_vol = models.CharField(default=None, null=True, max_length=15)
    total_assets = models.CharField(default=None, null=True, max_length=15)
    
    time = models.DateTimeField(default=None, null=True)

    # def __str__(self):
    #     return f'({Types[Types.index(self.Type)+1]}) {self.time}'
    
    class Meta:
        verbose_name = '(Live All) Assets'
        verbose_name_plural = '(Live) All Assets'

class AllAssetsAfterLive(models.Model):
    Type = models.CharField(choices=TYPES, max_length=9)
    link = models.URLField(null=True)
    
    date = models.DateField(default=None, null=True)
    
    pe_ratio = models.CharField(default=None, null=True, max_length=15)
    coupon = models.CharField(default=None, null=True, max_length=15)
    div_yield = models.CharField(default=None, null=True, max_length=15)
    shrs_outstndng = models.CharField(default=None, null=True, max_length=15)
    avg_vol_3m = models.CharField(default=None, null=True, max_length=15)
    beta = models.CharField(default=None, null=True, max_length=15)
    next_earn_date = models.DateField(default=None, null=True)
    max_supply = models.CharField(default=None, null=True, max_length=15)
    volume = models.CharField(default=None, null=True, max_length=15)
    div_ttm = models.CharField(default=None, null=True, max_length=15)
    price_rng = models.CharField(default=None, null=True, max_length=30) # for bonds
    roe = models.CharField(default=None, null=True, max_length=15)
    market_cap = models.CharField(default=None, null=True, max_length=15)
    rating = models.CharField(default=None, null=True, max_length=5)
    maturity_date = models.DateField(default=None, null=True)
    total_assets = models.CharField(default=None, null=True, max_length=15)
    ttm_yield = models.CharField(default=None, null=True, max_length=15)
    rng_52_wk = models.CharField(default=None, null=True, max_length=15)
    revenue = models.CharField(default=None, null=True, max_length=15)
    div_and_yield = models.CharField(default=None, null=True, max_length=15)
    one_year_chg = models.CharField(default=None, null=True, max_length=15)
    price_opn = models.CharField(default=None, null=True, max_length=15) #bonds
    roa = models.CharField(default=None, null=True, max_length=15)
    price = models.CharField(default=None, null=True, max_length=15) # bonds
    turnover = models.CharField(default=None, null=True, max_length=15)
    days_rng = models.CharField(default=None, null=True, max_length=30)
    expenses = models.CharField(default=None, null=True, max_length=15)
    roi_ttm = models.CharField(default=None, null=True, max_length=15)
    circ_supply = models.CharField(default=None, null=True, max_length=15)
    risk_rating = models.CharField(default=None, null=True, max_length=5)
    last_roll_day = models.DateField(default=None, null=True)
    months = models.CharField(default=None, null=True, max_length=15)
    settlement_day = models.DateField(default=None, null=True)
    asset_class = models.CharField(default=None, null=True, max_length=15)
    eps = models.CharField(default=None, null=True, max_length=15)

    def __str__(self):
        return f'({Types[Types.index(self.Type)+1]}) in {self.date.year} {self.date.strftime("%B")}'
    
    class Meta:
        verbose_name = '(After Live) All Assets'
        verbose_name_plural = '(After Live) All Assets'

