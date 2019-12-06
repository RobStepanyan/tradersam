from django.db import models

# Create your models here.
COUNTRIES = (
    ('G', 'Global'), ('USA', 'United States of America'), ('UK', 'United Kingdom'),
    ('JP', 'Japan'), ('HK', 'Honk Kong'), ('CH', 'China'), ('CA', 'Canada'),
    ('GE', 'Germany'), ('AU', 'Australia')
)

MARKETS = (
    ('NYSE', 'New York Stock Exchange'), ('NASDAQ', 'NASDAQ Stock Market'), ('OTC Markets', 'Over-The-Counter Markets')
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
    market = models.CharField(choices=MARKETS, max_length=11)
    isin = models.CharField(max_length=12)
    link = models.URLField()

    def __str__(self):
        return self.long_name + f' - ({self.short_name})'

    class Meta:
        verbose_name = "US's Stocks Static Info"
        verbose_name_plural = "US's Stocks Static Info"