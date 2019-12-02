from django.db import models

# Create your models here.
class CommodityStaticInfo(models.Model):
    fields_to_scrape = (
        'Contract Size', 'Tick Size', 'Tick Value', 'Base Symbol', 'Point Value', 'Months')
    
    short_name = models.CharField(max_length=16)
    
    @property
    def long_name(self):
        return self.short_name + ' Futures Contract'

    COUNTRIES = (('G', 'Global'), ('USA', 'United States'), ('UK', 'United Kingdom'))    
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


class CurrencyStaticInfo(models.Model):
    short_name = models.CharField(max_length=10)
    long_name = models.CharField(max_length=30)
    link = models.URLField()

    def __str__(self):
        return self.short_name + ' - ' + self.long_name

class CryptoCurrencyStaticInfo(models.Model):
    short_name = models.CharField(max_length=10)
    long_name = models.CharField(max_length=30)
    link = models.URLField()

    def __str__(self):
        return self.short_name + ' - ' + self.long_name