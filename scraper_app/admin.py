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
# Bonds
admin.site.register(models.USBondStaticInfo)
admin.site.register(models.JapanBondStaticInfo)
admin.site.register(models.UKBondStaticInfo)
admin.site.register(models.HKBondStaticInfo)
admin.site.register(models.ChinaBondStaticInfo)
admin.site.register(models.CanadaBondStaticInfo)
admin.site.register(models.GermanyBondStaticInfo)
admin.site.register(models.AustraliaBondStaticInfo)
# Funds
admin.site.register(models.FundIssuers)
admin.site.register(models.USFundStaticInfo)
admin.site.register(models.JapanFundStaticInfo)
admin.site.register(models.UKFundStaticInfo)
admin.site.register(models.HKFundStaticInfo)
admin.site.register(models.ChinaFundStaticInfo)
admin.site.register(models.CanadaFundStaticInfo)
admin.site.register(models.GermanyFundStaticInfo)
admin.site.register(models.AustraliaFundStaticInfo)
# Historical
admin.site.register(models.AllAssetsHistoricalMax) # All Assets Max Date Range (1step=1month)
admin.site.register(models.AllAssetsHistorical5Y) # All Assets 5 Years Date Range (1step=1week)
admin.site.register(models.AllAssetsHistorical1Y)
admin.site.register(models.AllAssetsHistorical6M1M)
admin.site.register(models.AllAssetsHistorical5D)
admin.site.register(models.AllAssetsHistorical1D)

# Live
admin.site.register(models.AllAssetsAfterLive)
admin.site.register(models.AllAssetsLive)