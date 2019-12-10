from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.CommodityStaticInfo)
admin.site.register(models.CurrencyStaticInfo)
admin.site.register(models.CryptocurrencyStaticInfo)
admin.site.register(models.USStockStaticInfo)
admin.site.register(models.JapanStockStaticInfo)
admin.site.register(models.UKStockStaticInfo)
admin.site.register(models.HKStockStaticInfo)
admin.site.register(models.ChinaStockStaticInfo)
admin.site.register(models.CanadaStockStaticInfo)