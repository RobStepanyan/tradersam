from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.CommodityStaticInfo)
admin.site.register(models.CurrencyStaticInfo)
admin.site.register(models.CryptoCurrencyStaticInfo)