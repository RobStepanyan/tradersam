from django.db import models

# Create your models here.
COUNTRIES = (
    ('G', 'Global'), ('USA', 'United States of America'), ('UK', 'United Kingdom'),
    ('JPN', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'),
    ('GE', 'Germany'), ('AU', 'Australia')
)


CURRENCIES = (
    ('USD', 'US Dollar'), ('JPY', 'Japanese Yen'), ('GBP', 'Pound Sterling'), ('HKD', 'Hong Kong Dollar'),
    ('CNY', 'Chinese Yuan'), ('CAD', 'Canadian Dollar'), ('EUR', 'Euro'), ('AUD', 'Australian Dollar')
)

MARKETS_USA = (
    ('NYSE', 'New York Stock Exchange (NYSE)'), ('NASDAQ', 'NASDAQ Stock Market'), ('OTC Markets', 'Over-The-Counter Markets (OTC)'),
    ('AMEX', 'American Stock Exchange (AMEX)'), ('BSE', 'Boston Stock Exchange (BSE)'), ('CBOE', 'Chicago Board Options Exchange (CBOE)'),
    ('CBOT', 'Chicago Board of Trade (CBOT)'), ('CME', 'Chicago Mercantile Exchange (CME)'), ('CHX', 'Chicago Stock Exchange (CHX)'),
    ('ISE', 'International Securities Exchange (ISE)'), ('MS4X', 'Miami Stock Exchange (MS4X)'), ('NSX', 'National Stock Exchange (NSX)'),
    ('PHLX', 'Philadelphia Stock Exchange (PHLX)'), ('NYSE Arca', 'NYSE Arca')
)

MARKETS_JPN = (
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
    ('CSE', 'Canadian Securities Exchange (CSE)'), ('NASDAQ', 'NASDAQ Canada')
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

    country = models.CharField(choices=COUNTRIES, max_length=3)
    
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
    country = models.CharField(choices=COUNTRIES, default='USA', max_length=3)
    market = models.CharField(choices=MARKETS_USA, max_length=11)
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
    country = models.CharField(choices=COUNTRIES, default='JPN', max_length=3)
    market = models.CharField(choices=MARKETS_JPN, max_length=7)
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
    country = models.CharField(choices=COUNTRIES, default='UK', max_length=3)
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
    country = models.CharField(choices=COUNTRIES, default='HK', max_length=3)
    market = models.CharField(choices=MARKETS_HK, default='HKG', max_length=20)
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
    country = models.CharField(choices=COUNTRIES, default='CH', max_length=3)
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
    country = models.CharField(choices=COUNTRIES, default='CA', max_length=3)
    market = models.CharField(choices=MARKETS_CA, max_length=20)
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
    country = models.CharField(choices=COUNTRIES, default='GE', max_length=3)
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
    country = models.CharField(choices=COUNTRIES, default='AU', max_length=3)
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
    country = models.CharField(choices=COUNTRIES, default='USA', max_length=3)
    market = models.CharField(choices=MARKETS_USA, max_length=11)
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
    country = models.CharField(choices=COUNTRIES, default='JPN', max_length=3)
    market = models.CharField(choices=MARKETS_JPN, max_length=7)
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
    country = models.CharField(choices=COUNTRIES, default='UK', max_length=3)
    market = models.CharField(choices=MARKETS_UK, default='London', max_length=20)
    link = models.URLField()
    currency = models.CharField(choices=CURRENCIES, default='GBP', max_length=3)

    def __str__(self):
        return self.long_name + f' - ({self.short_name})'

    class Meta:
        verbose_name = "United Kingdom Indices Static Info"
        verbose_name_plural = "United Kingdom Indices Static Info"