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
admin.site.register(models.GermanyStockStaticInfo)
admin.site.register(models.AustraliaStockStaticInfo)

admin.site.register(models.USIndexStaticInfo)
admin.site.register(models.JapanIndexStaticInfo)
admin.site.register(models.UKIndexStaticInfo)
admin.site.register(models.HKIndexStaticInfo)
admin.site.register(models.ChinaIndexStaticInfo)
admin.site.register(models.CanadaIndexStaticInfo)