from django.db import models
import datetime

# Create your models here.
COUNTRIES = (
    ('G', 'Global'), ('US', 'United States of America'), ('UK', 'United Kingdom'),
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


class CommodityStaticInfo(models.Model):
    fields_to_scrape = (
        'Contract Size', 'Tick Size', 'Tick Value', 'Base Symbol', 'Point Value', 'Months')
    
    short_name = models.CharField(max_length=16)
    
    @property
    def long_name(self):
        return self.short_name + ' Futures Contract'

    country = models.CharField(choices=COUNTRIES, max_length=2)
    
    base_symbol = models.CharField(max_length=6)
    contract_size = models.CharField(max_length=30)
    settlement_type = models.CharField(default='Physical', max_length=30)
    tick_size = models.CharField(max_length=30)
    tick_value = models.CharField(max_length=30)
    months = models.CharField(max_length=30)
    point_value = models.CharField(max_length=20)
    link = models.URLField()

    def __str__(self):
        return self.country + ' ' + self.long_name + ' (' + self.base_symbol + ')'

    class Meta:
        verbose_name = "Commodities' Static Info"
        verbose_name_plural = "Commodities' Static Info"


class CurrencyStaticInfo(models.Model):
    short_name = models.CharField(max_length=10)
    long_name = models.CharField(max_length=50)
    link = models.URLField()

    def __str__(self):
        return self.short_name + ' - ' + self.long_name

    class Meta:
        verbose_name = "Currencies' Static Info"
        verbose_name_plural = "Currencies' Static Info"

class CryptocurrencyStaticInfo(models.Model):
    short_name = models.CharField(max_length=10)
    long_name = models.CharField(max_length=50)
    link = models.URLField()

    def __str__(self):
        return self.short_name + ' - ' + self.long_name

    class Meta:
        verbose_name = "Cryptocurrencies' Static Info"
        verbose_name_plural = "Cryptocurrencies' Static Info"

class USStockStaticInfo(models.Model):
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
        verbose_name = "United States Stocks Static Info"
        verbose_name_plural = "United States Stocks Static Info"

class JapanStockStaticInfo(models.Model):
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
        verbose_name = "Japan Stocks Static Info"
        verbose_name_plural = "Japan Stocks Static Info"

class UKStockStaticInfo(models.Model):
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
        verbose_name = "United Kingdom Stocks Static Info"
        verbose_name_plural = "United Kingdom Stocks Static Info"

class HKStockStaticInfo(models.Model):
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
        verbose_name = "Hong Kong Stocks Static Info"
        verbose_name_plural = "Hong Kong Stocks Static Info"

class ChinaStockStaticInfo(models.Model):
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
        verbose_name = "China Stocks Static Info"
        verbose_name_plural = "China Stocks Static Info"

class CanadaStockStaticInfo(models.Model):
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
        verbose_name = "Canada Stocks Static Info"
        verbose_name_plural = "Canada Stocks Static Info"

class GermanyStockStaticInfo(models.Model):
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
        verbose_name = "Germany Stocks Static Info"
        verbose_name_plural = "Germany Stocks Static Info"

class AustraliaStockStaticInfo(models.Model):
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
        verbose_name = "Australia Stocks Static Info"
        verbose_name_plural = "Australia Stocks Static Info"

class USIndexStaticInfo(models.Model):
    short_name = models.CharField(max_length=12)
    long_name = models.CharField(max_length=63)
    country = models.CharField(choices=COUNTRIES, default='US', max_length=2)
    market = models.CharField(choices=MARKETS_US, max_length=11)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='USD', max_length=3)

    def __str__(self):
        return self.long_name + f' - ({self.short_name})'

    class Meta:
        verbose_name = "United States Indices Static Info"
        verbose_name_plural = "United States Indices Static Info"

class JapanIndexStaticInfo(models.Model):
    short_name = models.CharField(max_length=12)
    long_name = models.CharField(max_length=49)
    country = models.CharField(choices=COUNTRIES, default='JP', max_length=2)
    market = models.CharField(choices=MARKETS_JP, max_length=7)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='JPY', max_length=3)

    def __str__(self):
        return self.long_name + f' - ({self.short_name})'

    class Meta:
        verbose_name = "Japan Indices Static Info"
        verbose_name_plural = "Japan Indices Static Info"

class UKIndexStaticInfo(models.Model):
    short_name = models.CharField(max_length=12)
    long_name = models.CharField(max_length=49)
    country = models.CharField(choices=COUNTRIES, default='UK', max_length=2)
    market = models.CharField(choices=MARKETS_UK, default='London', max_length=20)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='GBP', max_length=3)

    def __str__(self):
        return self.long_name + f' - ({self.short_name})'

    class Meta:
        verbose_name = "United Kingdom Indices Static Info"
        verbose_name_plural = "United Kingdom Indices Static Info"

class HKIndexStaticInfo(models.Model):
    short_name = models.CharField(max_length=12)
    long_name = models.CharField(max_length=56)
    country = models.CharField(choices=COUNTRIES, default='HK', max_length=2)
    market = models.CharField(choices=MARKETS_HK, default='HKG', max_length=3)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='HKD', max_length=3)

    def __str__(self):
        return self.long_name + f' - ({self.short_name})'

    class Meta:
        verbose_name = "Hong Kong Indices Static Info"
        verbose_name_plural = "Hong Kong Indices Static Info"

class ChinaIndexStaticInfo(models.Model):
    short_name = models.CharField(max_length=12)
    long_name = models.CharField(max_length=56)
    country = models.CharField(choices=COUNTRIES, default='CH', max_length=2)
    market = models.CharField(choices=MARKETS_CH, max_length=8)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='CNY', max_length=3)

    def __str__(self):
        return self.long_name + f' - ({self.short_name})'

    class Meta:
        verbose_name = "China Indices Static Info"
        verbose_name_plural = "China Indices Static Info"

class CanadaIndexStaticInfo(models.Model):
    short_name = models.CharField(max_length=12)
    long_name = models.CharField(max_length=44)
    country = models.CharField(choices=COUNTRIES, default='CA', max_length=2)
    market = models.CharField(choices=MARKETS_CA, max_length=7)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='CAD', max_length=3)

    def __str__(self):
        return self.long_name + f' - ({self.short_name})'

    class Meta:
        verbose_name = "Canada Indices Static Info"
        verbose_name_plural = "Canada Indices Static Info"

class GermanyIndexStaticInfo(models.Model):
    short_name = models.CharField(max_length=12)
    long_name = models.CharField(max_length=46)
    country = models.CharField(choices=COUNTRIES, default='GE', max_length=2)
    market = models.CharField(choices=MARKETS_GE, max_length=10)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='EUR', max_length=3)

    def __str__(self):
        return self.long_name + f' - ({self.short_name})'

    class Meta:
        verbose_name = "Germany Indices Static Info"
        verbose_name_plural = "Germany Indices Static Info"

class AustraliaIndexStaticInfo(models.Model):
    short_name = models.CharField(max_length=12)
    long_name = models.CharField(max_length=47)
    country = models.CharField(choices=COUNTRIES, default='AU', max_length=2)
    market = models.CharField(choices=MARKETS_AU, max_length=3, default='ASX')
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='AUD', max_length=3)

    def __str__(self):
        return self.long_name + f' - ({self.short_name})'

    class Meta:
        verbose_name = "Australia Indices Static Info"
        verbose_name_plural = "Australia Indices Static Info"

class ETFIssuers(models.Model):
    name = models.CharField(max_length=45)
    country = models.CharField(choices=COUNTRIES, max_length=2)

    def __str__(self):
        return f'{self.country}' + self.long_name

    class Meta:
        verbose_name = 'ETF Issuers'
        verbose_name_plural = 'ETF Issuers'

ETF_ISSUERS_US = tuple([(i.name, i.name) for i in list(ETFIssuers.objects.filter(country='US'))])
ETF_ISSUERS_JP = tuple([(i.name, i.name) for i in list(ETFIssuers.objects.filter(country='JP'))])
ETF_ISSUERS_UK = tuple([(i.name, i.name) for i in list(ETFIssuers.objects.filter(country='UK'))])
ETF_ISSUERS_HK = tuple([(i.name, i.name) for i in list(ETFIssuers.objects.filter(country='HK'))])
ETF_ISSUERS_CH = tuple([(i.name, i.name) for i in list(ETFIssuers.objects.filter(country='CH'))])
ETF_ISSUERS_CA = tuple([(i.name, i.name) for i in list(ETFIssuers.objects.filter(country='CA'))])
ETF_ISSUERS_GE = tuple([(i.name, i.name) for i in list(ETFIssuers.objects.filter(country='GE'))])
ETF_ISSUERS_AU = tuple([(i.name, i.name) for i in list(ETFIssuers.objects.filter(country='AU'))])

class USETFStaticInfo(models.Model):
    short_name = models.CharField(max_length=12)
    long_name = models.CharField(max_length=98)
    country = models.CharField(choices=COUNTRIES, default='US', max_length=2)
    issuer = models.CharField(choices=ETF_ISSUERS_US, max_length=32)
    market = models.CharField(choices=MARKETS_US, max_length=11)
    currency = models.CharField(choices=CURRENCIES, default='USD', max_length=3)
    isin = models.CharField(max_length=12)
    link = models.URLField()

    def __str__(self):
        return f'{self.country}' + self.long_name

    class Meta:
        verbose_name = 'United States ETFs\' Static Info'
        verbose_name_plural = 'United States ETFs\' Static Info'

class JapanETFStaticInfo(models.Model):
    short_name = models.CharField(max_length=12)
    long_name = models.CharField(max_length=75)
    country = models.CharField(choices=COUNTRIES, default='JP', max_length=2)
    issuer = models.CharField(choices=ETF_ISSUERS_JP, max_length=40)
    market = models.CharField(choices=MARKETS_JP, max_length=7)
    isin = models.CharField(max_length=12)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='JPY', max_length=3)

    def __str__(self):
        return f'{self.country}' + self.long_name

    class Meta:
        verbose_name = 'Japan ETFs\' Static Info'
        verbose_name_plural = 'Japan ETFs\' Static Info'

class UKETFStaticInfo(models.Model):
    short_name = models.CharField(max_length=12)
    long_name = models.CharField(max_length=84)
    country = models.CharField(choices=COUNTRIES, default='UK', max_length=2)
    issuer = models.CharField(choices=ETF_ISSUERS_UK, max_length=40)
    market = models.CharField(choices=MARKETS_UK, default='London', max_length=20)
    isin = models.CharField(max_length=12)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='GBP', max_length=3)

    def __str__(self):
        return f'{self.country}' + self.long_name

    class Meta:
        verbose_name = 'United Kingdom ETFs\' Static Info'
        verbose_name_plural = 'United Kingdom ETFs\' Static Info'

class HKETFStaticInfo(models.Model):
    short_name = models.CharField(max_length=12)
    long_name = models.CharField(max_length=79)
    country = models.CharField(choices=COUNTRIES, default='HK', max_length=2)
    issuer = models.CharField(choices=ETF_ISSUERS_HK, max_length=45)
    market = models.CharField(choices=MARKETS_HK, default='HKG', max_length=3)
    isin = models.CharField(max_length=12)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='HKD', max_length=3)

    def __str__(self):
        return f'{self.country}' + self.long_name

    class Meta:
        verbose_name = 'Hong Kong ETFs\' Static Info'
        verbose_name_plural = 'Hong Kong ETFs\' Static Info'

class ChinaETFStaticInfo(models.Model):
    short_name = models.CharField(max_length=12)
    long_name = models.CharField(max_length=51)
    country = models.CharField(choices=COUNTRIES, default='CH', max_length=2)
    issuer = models.CharField(choices=ETF_ISSUERS_CH, max_length=40)
    market = models.CharField(choices=MARKETS_CH, max_length=20)
    isin = models.CharField(max_length=12)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='CNY', max_length=3)

    def __str__(self):
        return f'{self.country}' + self.long_name

    class Meta:
        verbose_name = 'China ETFs\' Static Info'
        verbose_name_plural = 'China ETFs\' Static Info'

class CanadaETFStaticInfo(models.Model):
    short_name = models.CharField(max_length=12)
    long_name = models.CharField(max_length=74)
    country = models.CharField(choices=COUNTRIES, default='CA', max_length=2)
    issuer = models.CharField(choices=ETF_ISSUERS_CA, max_length=37)
    market = models.CharField(choices=MARKETS_CA, max_length=7)
    isin = models.CharField(max_length=12)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='CAD', max_length=3)

    def __str__(self):
        return f'{self.country}' + self.long_name

    class Meta:
        verbose_name = 'Canada ETFs\' Static Info'
        verbose_name_plural = 'Canada ETFs\' Static Info'

class GermanyETFStaticInfo(models.Model):
    short_name = models.CharField(max_length=12)
    long_name = models.CharField(max_length=84)
    country = models.CharField(choices=COUNTRIES, default='GE', max_length=2)
    issuer = models.CharField(choices=ETF_ISSUERS_GE, max_length=40)
    market = models.CharField(choices=MARKETS_GE, max_length=20)
    isin = models.CharField(max_length=12)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='EUR', max_length=3)

    def __str__(self):
        return f'{self.country}' + self.long_name

    class Meta:
        verbose_name = 'Germany ETFs\' Static Info'
        verbose_name_plural = 'Germany ETFs\' Static Info'

class AustraliaETFStaticInfo(models.Model):
    short_name = models.CharField(max_length=12)
    long_name = models.CharField(max_length=61)
    country = models.CharField(choices=COUNTRIES, default='AU', max_length=2)
    issuer = models.CharField(choices=ETF_ISSUERS_AU, max_length=38)
    market = models.CharField(choices=MARKETS_AU, max_length=3, default='ASX')
    isin = models.CharField(max_length=12)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='AUD', max_length=3)

    def __str__(self):
        return f'{self.country}' + self.long_name

    class Meta:
        verbose_name = 'Australia ETFs\' Static Info'
        verbose_name_plural = 'Australia ETFs\' Static Info'
# *********************** Bonds
class USBondStaticInfo(models.Model):
    short_name = models.CharField(max_length=18)
    long_name = models.CharField(max_length=32)
    country = models.CharField(choices=COUNTRIES, default='US', max_length=2)
    market = models.CharField(choices=MARKETS_US, max_length=11)
    currency = models.CharField(choices=CURRENCIES, default='USD', max_length=3)
    link = models.URLField()

    def __str__(self):
        return self.long_name

    class Meta:
        verbose_name = 'United States Bonds\' Static Info'
        verbose_name_plural = 'United States Bonds\' Static Info'

class JapanBondStaticInfo(models.Model):
    short_name = models.CharField(max_length=10)
    long_name = models.CharField(max_length=24)
    country = models.CharField(choices=COUNTRIES, default='JP', max_length=2)
    market = models.CharField(choices=MARKETS_JP, max_length=7)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='JPY', max_length=3)

    def __str__(self):
        return self.long_name

    class Meta:
        verbose_name = 'Japan Bonds\' Static Info'
        verbose_name_plural = 'Japan Bonds\' Static Info'

class UKBondStaticInfo(models.Model):
    short_name = models.CharField(max_length=8)
    long_name = models.CharField(max_length=33)
    country = models.CharField(choices=COUNTRIES, default='UK', max_length=2)
    market = models.CharField(choices=MARKETS_UK, default='London', max_length=20)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='GBP', max_length=3)

    def __str__(self):
        return self.long_name

    class Meta:
        verbose_name = 'United Kingdom Bonds\' Static Info'
        verbose_name_plural = 'United Kingdom Bonds\' Static Info'

class HKBondStaticInfo(models.Model):
    short_name = models.CharField(max_length=13)
    long_name = models.CharField(max_length=28)
    country = models.CharField(choices=COUNTRIES, default='HK', max_length=2)
    market = models.CharField(choices=MARKETS_HK, default='HKG', max_length=3)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='HKD', max_length=3)

    def __str__(self):
        return self.long_name

    class Meta:
        verbose_name = 'Hong Kong Bonds\' Static Info'
        verbose_name_plural = 'Hong Kong Bonds\' Static Info'

class ChinaBondStaticInfo(models.Model):
    short_name = models.CharField(max_length=9)
    long_name = models.CharField(max_length=24)
    country = models.CharField(choices=COUNTRIES, default='CH', max_length=2)
    market = models.CharField(choices=MARKETS_CH, max_length=20)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='CNY', max_length=3)

    def __str__(self):
        return self.long_name

    class Meta:
        verbose_name = 'China Bonds\' Static Info'
        verbose_name_plural = 'China Bonds\' Static Info'

class CanadaBondStaticInfo(models.Model):
    short_name = models.CharField(max_length=10)
    long_name = models.CharField(max_length=25)
    country = models.CharField(choices=COUNTRIES, default='CA', max_length=2)
    market = models.CharField(choices=MARKETS_CA, max_length=7)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='CAD', max_length=3)

    def __str__(self):
        return self.long_name

    class Meta:
        verbose_name = 'Canada Bonds\' Static Info'
        verbose_name_plural = 'Canada Bonds\' Static Info'

class GermanyBondStaticInfo(models.Model):
    short_name = models.CharField(max_length=11)
    long_name = models.CharField(max_length=26)
    country = models.CharField(choices=COUNTRIES, default='GE', max_length=2)
    market = models.CharField(choices=MARKETS_GE, max_length=20)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='EUR', max_length=3)

    def __str__(self):
        return self.long_name

    class Meta:
        verbose_name = 'Germany Bonds\' Static Info'
        verbose_name_plural = 'Germany Bonds\' Static Info'

class AustraliaBondStaticInfo(models.Model):
    short_name = models.CharField(max_length=13)
    long_name = models.CharField(max_length=28)
    country = models.CharField(choices=COUNTRIES, default='AU', max_length=2)
    market = models.CharField(choices=MARKETS_AU, max_length=3, default='ASX')
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='AUD', max_length=3)

    def __str__(self):
        return self.long_name

    class Meta:
        verbose_name = 'Australia Bonds\' Static Info'
        verbose_name_plural = 'Australia Bonds\' Static Info'

class FundIssuers(models.Model):
    name = models.CharField(max_length=55)
    country = models.CharField(choices=COUNTRIES, max_length=2)

    def __str__(self):
        return f'{self.country}' + self.long_name

    class Meta:
        verbose_name = 'Fund Issuers'
        verbose_name_plural = 'Fund Issuers'

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
    short_name = models.CharField(max_length=18) #determine
    long_name = models.CharField(max_length=32) #determine
    country = models.CharField(choices=COUNTRIES, default='US', max_length=2)
    market = models.CharField(choices=MARKETS_US, max_length=11)
    currency = models.CharField(choices=CURRENCIES, default='USD', max_length=3)
    link = models.URLField()
    issuer = models.CharField(choices=FUND_ISSUERS_US, max_length=30)
    isin = models.CharField(max_length=12)
    min_investment = models.IntegerField()
    category = models.CharField(max_length=30)
    inception_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.long_name

    class Meta:
        verbose_name = 'United States Funds\' Static Info'
        verbose_name_plural = 'United States Funds\' Static Info'

class JapanFundStaticInfo(models.Model):
    short_name = models.CharField(max_length=10)
    long_name = models.CharField(max_length=24)
    country = models.CharField(choices=COUNTRIES, default='JP', max_length=2)
    market = models.CharField(choices=MARKETS_JP, max_length=7)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='JPY', max_length=3)
    issuer = models.CharField(choices=FUND_ISSUERS_JP, max_length=48)
    isin = models.CharField(max_length=12)
    min_investment = models.IntegerField()
    category = models.CharField(max_length=30)
    inception_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.long_name

    class Meta:
        verbose_name = 'Japan Funds\' Static Info'
        verbose_name_plural = 'Japan Funds\' Static Info'

class UKFundStaticInfo(models.Model):
    short_name = models.CharField(max_length=8)
    long_name = models.CharField(max_length=33)
    country = models.CharField(choices=COUNTRIES, default='UK', max_length=2)
    market = models.CharField(choices=MARKETS_UK, default='London', max_length=20)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='GBP', max_length=3)
    issuer = models.CharField(choices=FUND_ISSUERS_UK, max_length=50)
    isin = models.CharField(max_length=12)
    min_investment = models.IntegerField()
    category = models.CharField(max_length=30)
    inception_date = models.DateField(default=datetime.date.today)

    def __str__(self): 
        return self.long_name

    class Meta:
        verbose_name = 'United Kingdom Funds\' Static Info'
        verbose_name_plural = 'United Kingdom Funds\' Static Info'

class HKFundStaticInfo(models.Model):
    short_name = models.CharField(max_length=13)
    long_name = models.CharField(max_length=28)
    country = models.CharField(choices=COUNTRIES, default='HK', max_length=2)
    market = models.CharField(choices=MARKETS_HK, default='HKG', max_length=3)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='HKD', max_length=3)
    issuer = models.CharField(choices=FUND_ISSUERS_HK, max_length=50)
    isin = models.CharField(max_length=12)
    min_investment = models.IntegerField()
    category = models.CharField(max_length=30)
    inception_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.long_name

    class Meta:
        verbose_name = 'Hong Kong Funds\' Static Info'
        verbose_name_plural = 'Hong Kong Funds\' Static Info'

class ChinaFundStaticInfo(models.Model):
    short_name = models.CharField(max_length=9)
    long_name = models.CharField(max_length=24)
    country = models.CharField(choices=COUNTRIES, default='CH', max_length=2)
    market = models.CharField(choices=MARKETS_CH, max_length=20)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='CNY', max_length=3)
    issuer = models.CharField(choices=FUND_ISSUERS_CH, max_length=39)
    isin = models.CharField(max_length=12)
    min_investment = models.IntegerField()
    category = models.CharField(max_length=30)
    inception_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.long_name

    class Meta:
        verbose_name = 'China Funds\' Static Info'
        verbose_name_plural = 'China Funds\' Static Info'

class CanadaFundStaticInfo(models.Model):
    short_name = models.CharField(max_length=10)
    long_name = models.CharField(max_length=25)
    country = models.CharField(choices=COUNTRIES, default='CA', max_length=2)
    market = models.CharField(choices=MARKETS_CA, max_length=7)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='CAD', max_length=3)
    issuer = models.CharField(choices=FUND_ISSUERS_CA, max_length=33)
    isin = models.CharField(max_length=12)
    min_investment = models.IntegerField()
    category = models.CharField(max_length=30)
    inception_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.long_name

    class Meta:
        verbose_name = 'Canada Funds\' Static Info'
        verbose_name_plural = 'Canada Funds\' Static Info'

class GermanyFundStaticInfo(models.Model):
    short_name = models.CharField(max_length=11)
    long_name = models.CharField(max_length=26)
    country = models.CharField(choices=COUNTRIES, default='GE', max_length=2)
    market = models.CharField(choices=MARKETS_GE, max_length=20)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='EUR', max_length=3)
    issuer = models.CharField(choices=FUND_ISSUERS_GE, max_length=41)
    isin = models.CharField(max_length=12)
    min_investment = models.IntegerField()
    category = models.CharField(max_length=30)
    inception_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.long_name

    class Meta:
        verbose_name = 'Germany Funds\' Static Info'
        verbose_name_plural = 'Germany Funds\' Static Info'

class AustraliaFundStaticInfo(models.Model):
    short_name = models.CharField(max_length=13)
    long_name = models.CharField(max_length=28)
    country = models.CharField(choices=COUNTRIES, default='AU', max_length=2)
    market = models.CharField(choices=MARKETS_AU, max_length=3, default='ASX')
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='AUD', max_length=3)
    issuer = models.CharField(choices=FUND_ISSUERS_AU, max_length=39)
    isin = models.CharField(max_length=12)
    min_investment = models.IntegerField()
    category = models.CharField(max_length=30)
    inception_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.long_name

    class Meta:
        verbose_name = 'Australia Funds\' Static Info'
        verbose_name_plural = 'Australia Funds\' Static Info'
