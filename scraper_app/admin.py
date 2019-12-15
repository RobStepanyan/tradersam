from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.CommodityStaticInfo)
admin.site.register(models.CurrencyStaticInfo)
admin.site.register(models.CryptocurrencyStaticInfo)
# Stocks
admin.site.register(models.USStockStaticInfo)
admin.site.register(models.JapanStockStaticInfo)
admin.site.register(models.UKStockStaticInfo)
admin.site.register(models.HKStockStaticInfo)
admin.site.register(models.ChinaStockStaticInfo)
admin.site.register(models.CanadaStockStaticInfo)
admin.site.register(models.GermanyStockStaticInfo)
admin.site.register(models.AustraliaStockStaticInfo)
# Indices
admin.site.register(models.USIndexStaticInfo)
admin.site.register(models.JapanIndexStaticInfo)
admin.site.register(models.UKIndexStaticInfo)
admin.site.register(models.HKIndexStaticInfo)
admin.site.register(models.ChinaIndexStaticInfo)
admin.site.register(models.CanadaIndexStaticInfo)
admin.site.register(models.GermanyIndexStaticInfo)
admin.site.register(models.AustraliaIndexStaticInfo)
# ETFs
admin.site.register(models.ETFIssuers)
admin.site.register(models.USETFStaticInfo)
admin.site.register(models.JapanETFStaticInfo)
admin.site.register(models.UKETFStaticInfo)
admin.site.register(models.HKETFStaticInfo)
admin.site.register(models.ChinaETFStaticInfo)
admin.site.register(models.CanadaETFStaticInfo)
admin.site.register(models.GermanyETFStaticInfo)
admin.site.register(models.AustraliaETFStaticInfo)